import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 
import datetime
 

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('bigminiconf-nov2020-f59c478cf5b4.json', scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = '1PoZAzkhmf1dRxCsNAAnrWWBRwlSYkcq_6UJaB_laFUY'
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

# 歩数を取得（1分単位）
def steps_data(date):
    data_min = authed_client.intraday_time_series('activities/steps', base_date="2020-10-29", detail_level='1min', start_time="09:00", end_time="20:00")
    print("data_min",data_min)
    return data_min

#writing data into spread sheet 
headers = ['value', 'datetime'] # keys

def set_data_to_sheet(datas):
    for data in datas:
        column = []
        for header in headers:
            column.append(data[header])

        worksheet.append_row(column)

# 定期実行のための関数
def get_latest_data(data):
    list_num = len(data)
    new_list = []
    for i in range(list_num-30, list_num):
        new_list.append(data[i])
    return new_list

def job():
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')

    data = steps_data(date)
    latest_data = get_latest_data(data)
    set_data_to_sheet(latest_data)

job()