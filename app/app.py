from flask import Flask, render_template, jsonify, request
import gspread
from google.oauth2.service_account import Credentials
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-key-change-in-production")

# Google Sheets Configuration
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_FILE = "credentials/credentials.json"

# Database Configuration
DB_PATH = "data/fiber_ops.db"


def init_db():
    """Initialize SQLite database"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sync_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sync_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            records_synced INTEGER,
            status TEXT
        )
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS project_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sync_id INTEGER,
            project_name TEXT,
            total_footage REAL,
            completed_footage REAL,
            material_cost REAL,
            labor_cost REAL,
            total_cost REAL,
            recorded_date DATE,
            FOREIGN KEY (sync_id) REFERENCES sync_history(id)
        )
    """
    )

    conn.commit()
    conn.close()


def get_sheets_client():
    """Get authenticated Google Sheets client"""
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return None


def sync_from_sheets():
    """Sync data from Google Sheets to local database"""
    try:
        client = get_sheets_client()
        if not client:
            return False, "Failed to connect to Google Sheets"

        sheet = client.open_by_key(SHEET_ID).sheet1
        records = sheet.get_all_records()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create sync record
        c.execute(
            "INSERT INTO sync_history (records_synced, status) VALUES (?, ?)",
            (len(records), "success"),
        )
        sync_id = c.lastrowid

        # Insert project data
        for record in records:
            c.execute(
                """
                INSERT INTO project_data
                (sync_id, project_name, total_footage, completed_footage,
                 material_cost, labor_cost, total_cost, recorded_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    sync_id,
                    record.get("Project Name", ""),
                    float(record.get("Total Footage", 0)),
                    float(record.get("Completed Footage", 0)),
                    float(record.get("Material Cost", 0)),
                    float(record.get("Labor Cost", 0)),
                    float(record.get("Total Cost", 0)),
                    record.get("Date", datetime.now().strftime("%Y-%m-%d")),
                ),
            )

        conn.commit()
        conn.close()

        return True, f"Successfully synced {len(records)} records"

    except Exception as e:
        return False, f"Sync error: {str(e)}"


@app.route("/")
def index():
    """Main dashboard page"""
    return render_template("index.html")


@app.route("/api/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/api/sync", methods=["POST"])
def sync():
    """Trigger sync from Google Sheets"""
    success, message = sync_from_sheets()
    return jsonify({"success": success, "message": message})


@app.route("/api/stats")
def stats():
    """Get current statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Get latest sync data
        c.execute(
            """
            SELECT
                SUM(total_footage) as total_footage,
                SUM(completed_footage) as completed_footage,
                SUM(material_cost) as material_cost,
                SUM(labor_cost) as labor_cost,
                SUM(total_cost) as total_cost,
                COUNT(DISTINCT project_name) as project_count
            FROM project_data
            WHERE sync_id = (SELECT MAX(id) FROM sync_history)
        """
        )

        stats = dict(c.fetchone())
        conn.close()

        # Calculate completion percentage
        if stats["total_footage"] and stats["total_footage"] > 0:
            stats["completion_percentage"] = round(
                (stats["completed_footage"] / stats["total_footage"]) * 100, 2
            )
        else:
            stats["completion_percentage"] = 0

        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/projects")
def projects():
    """Get all projects with their data"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            """
            SELECT
                project_name,
                total_footage,
                completed_footage,
                material_cost,
                labor_cost,
                total_cost,
                recorded_date,
                ROUND((completed_footage * 100.0 / NULLIF(total_footage, 0)), 2) as completion_pct
            FROM project_data
            WHERE sync_id = (SELECT MAX(id) FROM sync_history)
            ORDER BY project_name
        """
        )

        projects = [dict(row) for row in c.fetchall()]
        conn.close()

        return jsonify(projects)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/history")
def history():
    """Get sync history"""
    try:
        days = request.args.get("days", 30, type=int)

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            """
            SELECT
                id,
                sync_time,
                records_synced,
                status
            FROM sync_history
            WHERE sync_time >= datetime('now', '-' || ? || ' days')
            ORDER BY sync_time DESC
            LIMIT 100
        """,
            (days,),
        )

        history = [dict(row) for row in c.fetchall()]
        conn.close()

        return jsonify(history)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_ENV") == "development")
