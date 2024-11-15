import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# Authorize the client
client = gspread.authorize(creds)

# Open the spreadsheet
sheet = client.open('all spells')

# Access a specific worksheet
worksheet = sheet.worksheet('Sheet1')

# Get all values from the worksheet
table = worksheet.get_all_values()

# Print the table
print(table)