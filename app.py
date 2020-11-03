# -*- coding: utf-8 -*-
# fitbit autholization
import fitbit
from ast import literal_eval
from datetime import datetime, timedelta, timezone

# google spread sheet 
# import gspread
# import json
# from oauth2client.service_account import ServiceAccountCredentials 


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

# 直近7日間の日付リストを作成する
def build_date_list():
    date_array = []    
    # タイムゾーンの生成
    JST = timezone(timedelta(hours=+9),'JST')
    for i in range(0,7):
        date = datetime.now(JST).date() - timedelta(days = i)
        date_array.append(str(date))
    return date_array

dates_list = build_date_list()

def get_activities():
    activities_dict={}
    for DATE in dates_list:
        value = authed_client.intraday_time_series('activities/steps', base_date=DATE, detail_level='1min', start_time=None, end_time=None) 
        activities_dict[DATE] = value
        print("value",value["activities-steps"][0])
    return activities_dict

result = get_activities()





