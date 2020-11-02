import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 
import datetime
 

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('bigminiconf-nov2020-f59c478cf5b4.json', scope)

gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '1PoZAzkhmf1dRxCsNAAnrWWBRwlSYkcq_6UJaB_laFUY'

worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

# test 
import_value = int(worksheet.acell('A1').value)

export_value = import_value+100
worksheet.update_cell(1,2, export_value)