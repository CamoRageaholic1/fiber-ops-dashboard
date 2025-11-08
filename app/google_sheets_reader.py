import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

class GoogleSheetsReader:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        
        # Look for credentials in the credentials folder
        creds_path = '/app/credentials/credentials.json'
        if not os.path.exists(creds_path):
            creds_path = 'credentials/credentials.json'
        
        self.credentials = service_account.Credentials.from_service_account_file(
            creds_path, scopes=self.SCOPES)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet_id = os.environ.get('GOOGLE_SHEET_ID')
        
        if not self.sheet_id:
            raise ValueError("GOOGLE_SHEET_ID not found in environment variables")
    
    def read_sheet(self, sheet_name, range_name=None):
        """Read data from a specific sheet tab"""
        try:
            if range_name:
                range_notation = f"{sheet_name}!{range_name}"
            else:
                range_notation = sheet_name
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=range_notation
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                print(f"No data found in sheet: {sheet_name}")
                return pd.DataFrame()
            
            # Convert to DataFrame (first row as headers)
            df = pd.DataFrame(values[1:], columns=values[0])
            return df
        
        except Exception as e:
            print(f"Error reading sheet {sheet_name}: {str(e)}")
            return pd.DataFrame()
    
    def get_all_sheets(self):
        """Get list of all sheet tabs"""
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.sheet_id
            ).execute()
            
            sheets = sheet_metadata.get('sheets', [])
            return [sheet['properties']['title'] for sheet in sheets]
        
        except Exception as e:
            print(f"Error getting sheet list: {str(e)}")
            return []
    
    def get_productivity_data(self):
        """Get productivity data"""
        return self.read_sheet('Productivity')
    
    def get_materials_data(self):
        """Get materials data"""
        return self.read_sheet('Materials')
    
    def get_labor_data(self):
        """Get labor data"""
        return self.read_sheet('Labor')
    
    def get_splicing_data(self):
        """Get splicing data"""
        return self.read_sheet('Splicing')
    
    def get_flaggers_data(self):
        """Get flaggers data"""
        return self.read_sheet('Flaggers')
    
    def get_fuel_data(self):
        """Get fuel data"""
        return self.read_sheet('Fuel')
    
    def get_truck_maintenance_data(self):
        """Get truck maintenance data"""
        return self.read_sheet('Truck Maintenance')
    
    def get_summary_totals(self):
        """Get pre-calculated totals from specific cells"""
        try:
            # Read Cover Page B11 (Materials total)
            cover_result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Cover Page!B11'
            ).execute()
            materials_total = float(cover_result.get('values', [[0]])[0][0] or 0)
            
            # Read Labor tab F34 (Total hours)
            labor_f34_result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Labor!F34'
            ).execute()
            labor_hours = float(labor_f34_result.get('values', [[0]])[0][0] or 0)
            
            # Read Labor tab J43 (Labor cost total)
            labor_cost_result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Labor!J43'
            ).execute()
            labor_cost_total = float(labor_cost_result.get('values', [[0]])[0][0] or 0)
            
            return {
                'materials_total': materials_total,
                'labor_hours_total': labor_hours,
                'labor_cost_total': labor_cost_total
            }
            
        except Exception as e:
            print(f"Error reading summary totals: {str(e)}")
            return {
                'materials_total': 0,
                'labor_hours_total': 0,
                'labor_cost_total': 0
            }

# Test the connection
if __name__ == "__main__":
    try:
        reader = GoogleSheetsReader()
        print("✅ Google Sheets connection successful!")
        print("\nAvailable sheets:", reader.get_all_sheets())
        
        productivity = reader.get_productivity_data()
        print(f"\n✅ Productivity records found: {len(productivity)}")
        
        materials = reader.get_materials_data()
        print(f"✅ Materials records found: {len(materials)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")