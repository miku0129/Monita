# -*- coding: utf-8 -*-
# fitbit autholization
import fitbit
from ast import literal_eval

# google spread sheet 
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 
import datetime


CLIENT_ID     = "22C2BM"
CLIENT_SECRET = "0d0a664b49593f88e297a7f24c2c8157"
TOKEN_FILE    = "token.txt" #同一ディレクトリに.txtを作る

tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
ACCESS_TOKEN = token_dict['access_token']
REFRESH_TOKEN = token_dict['refresh_token']

def updateToken(token):
    f = open(TOKEN_FILE, 'w')
    f.write(str(token))
    f.close()
    return

authed_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, refresh_cb=updateToken)

# def pound_to_kg(pound):
#     kg = pound * 0.454
#     return kg

#test - get body weight 
TODAY = datetime.date.today()
# TODAY = "2020-10-31"
# bodyweight = authed_client.get_bodyweight(base_date=TODAY)
# weight = bodyweight["weight"][0]["weight"]
# print(pound_to_kg(weight), "kg")

#test - sleep 
# sleep = authed_client.sleep(date="2020-10-29")
# print("sleep",sleep)

# 歩数を取得（1分単位...はできない）
steps = authed_client.intraday_time_series('activities/steps', base_date=TODAY, detail_level='1min', start_time="02:00", end_time="04:00") 
print("steps!!",steps)

def get_steps_data(date):
    steps_data = authed_client.intraday_time_series('activities/steps', 'YYYY-MM-DD', detail_level='15min') 
    # for data in steps_data:
    #     datetime = date + " " + data['time'] 
    #     data['datetime'] = datetime
    #     del data['time']
    #     print("steps_data",steps_data)
    return steps_data


# 運動量を取得（1分単位...はできない）
# excercise = authed_client.intraday_time_series('activities/minutesLightlyActive	', base_date=TODAY, detail_level='15min', start_time=None, end_time=None) 
# print("excercise", excercise)

# google spread sheet 
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('bigminiconf-nov2020-f59c478cf5b4.json', scope)

gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '1PoZAzkhmf1dRxCsNAAnrWWBRwlSYkcq_6UJaB_laFUY'

worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

# sheetへの書き込み
headers = ['value', 'datetime'] # keys

def set_data_to_sheet(datas):
    print("datas",datas)
    for data in datas:
        column = []
        for header in headers:
            print("headers",headers)
            column.append(data[header])

        worksheet.append_row(column)

# 定期実行のための関数
# def get_latest_data(data):
#     list_num = len(data)
#     print("list_num",list_num)
#     new_list = []
#     for i in range(list_num-30, list_num):
#         new_list.append(data[i])
#     print("new_list",new_list)
#     return new_list

def job():
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')

    data = get_steps_data(date)
    # latest_data = get_latest_data(data)
    # print("latest_data",latest_data)
    set_data_to_sheet(data)

job()