# 🚀 Fiber Ops Dashboard

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)](https://www.docker.com/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

A comprehensive construction operations dashboard for fiber optic ISP projects with real-time Google Sheets integration, cost tracking, and productivity monitoring.

## ✨ Features

- 📊 **Real-time Dashboard** - Live metrics and project status updates
- 🔄 **Google Sheets Integration** - Automatic data synchronization
- 💰 **Cost Tracking** - Monitor material and labor expenses
- 📈 **Progress Monitoring** - Track footage completion across projects
- 🐳 **Docker Deployment** - Easy setup with containerization
- 📱 **Mobile Responsive** - Works on all devices
- 🔒 **Secure** - Service account authentication
- 📝 **SQLite Database** - Historical data storage

## 🎯 Quick Start

### Prerequisites

- Docker & Docker Compose
- Google Cloud Service Account with Sheets API access
- Google Sheet with project data

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/CamoRageaholic1/fiber-ops-dashboard.git
cd fiber-ops-dashboard
```

2. **Run the installer** (Ubuntu/Linux)
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

3. **Configure environment**
```bash
# Edit .env with your settings
cp .env.example .env
nano .env
```

4. **Add Google credentials**
```bash
# Place your service account JSON in credentials/
cp /path/to/your/credentials.json credentials/credentials.json
```

5. **Start the application**
```bash
docker-compose up -d
```

6. **Access the dashboard**
```
http://localhost:5000
```

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [API Documentation](docs/API.md)
- [Google Sheets Setup](docs/GOOGLE_SHEETS_SETUP.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🏗️ Architecture

```
fiber-ops-dashboard/
├── app/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── templates/
│       └── index.html      # Dashboard UI
├── scripts/
│   ├── install.sh          # Automated installer
│   ├── start.sh            # Start script
│   ├── stop.sh             # Stop script
│   └── backup.sh           # Backup script
├── docs/                   # Documentation
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## 🔧 Configuration

### Environment Variables

```env
GOOGLE_SHEET_ID=your_sheet_id_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=production
PROJECT_NAME=Your-Project-Name
```

### Google Sheets Format

Your Google Sheet should have these columns:

| Project Name | Total Footage | Completed Footage | Material Cost | Labor Cost | Total Cost | Date |
|--------------|---------------|-------------------|---------------|------------|------------|------|

## 📊 API Endpoints

- `GET /` - Main dashboard
- `GET /api/health` - Health check
- `POST /api/sync` - Trigger data sync
- `GET /api/stats` - Get statistics
- `GET /api/projects` - Get all projects
- `GET /api/history` - Get sync history

## 🚀 Deployment

### Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Manual Deployment

```bash
cd app
pip install -r requirements.txt
python app.py
```

## 🛠️ Development

### Development Mode

```bash
docker-compose -f docker-compose.dev.yml up
```

### Running Tests

```bash
# Tests coming soon
```

## 📝 License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

**For Individual Use Only** - Commercial use is prohibited.

See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📧 Contact

- GitHub: [@CamoRageaholic1](https://github.com/CamoRageaholic1)
- Issues: [GitHub Issues](https://github.com/CamoRageaholic1/fiber-ops-dashboard/issues)

## 🙏 Acknowledgments

- Built with Flask and Bootstrap
- Google Sheets API integration
- Docker for containerization

---

**⭐ If you find this project helpful, please star it!**
