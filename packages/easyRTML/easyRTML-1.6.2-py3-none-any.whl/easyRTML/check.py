import gspread
from google.oauth2.service_account import Credentials

def is_access_granted(email, key):
    # Define the scope and authorize the credentials
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    # Open the Google Sheet using the sheet ID
    sheet_id = "1T2GQT5l_OhSR2g2ZkuOUHLcpK7MeXdRov50ETnmOCn4"
    sheet = client.open_by_key(sheet_id)

    # Get all records from the Google Sheet
    records = sheet.sheet1.get_all_records()

    # Verify email and key
    for record in records:
        if record['email'] == email and record['keys'] == key and record['Status'] == "Active":
            return True
    return False
