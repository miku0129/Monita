#memo: curl, cmdやpowerchellだとダメだけど、git Bash だと上手くいった。

# -*- coding: utf-8 -*-
# fitbit autholization
import fitbit
from ast import literal_eval
from datetime import datetime, timedelta, timezone

# google spread sheet 
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 


CLIENT_ID     = "22C2HT"
CLIENT_SECRET = "cd36c066c7dd5191eadf89ff466c5ea5" 
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

# 直近7日間の日付リストを作成する
def build_date_list():
    date_array = []    
    # タイムゾーンの生成
    JST = timezone(timedelta(hours=+9),'JST')
    for i in range(0,7):
        date = datetime.now(JST).date() - timedelta(days = i)
        date_array.append(str(date))
    return date_array

# google spreadsheet 
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('bigminiconf-nov2020-f59c478cf5b4.json', scope)

gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '1PoZAzkhmf1dRxCsNAAnrWWBRwlSYkcq_6UJaB_laFUY'

worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1


dates_list = build_date_list()

def get_activities():
    activities_dict={}
    for DATE in dates_list:
        # steps 
        value = authed_client.intraday_time_series('activities/steps', base_date=DATE, detail_level='1min', start_time="07:00", end_time="22:00") 
        activities_dict[value["activities-steps"][0]["dateTime"]]=value["activities-steps"][0]["value"]
        print("value",value)

        # sleep
        # sleep = authed_client.sleep(date=DATE)
        # print("sleep",sleep["sleep"][0]['minutesAsleep'])
        # activities_dict["totalMinutesAsleep"]=sleep["summary"]

    return activities_dict

get_activities()
# activities_dict = get_activities()

# google spreadsheetに書き込み「
# def print_activities(dict):
#     for key in dict: 
#         column = []
#         column.append(key)
#         column.append(dict[key])
#         worksheet.append_row(column)

# print_activities(activities_dict) 



