# -*- coding: utf-8 -*-
# fitbit autholization
import fitbit
from ast import literal_eval

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

def pound_to_kg(pound):
    kg = pound * 0.454
    return kg

#test - get body weight 
#TODAY = datetime.date.today()
TODAY = "2020-10-31"
bodyweight = authed_client.get_bodyweight(base_date=TODAY)
weight = bodyweight["weight"][0]["weight"]
print(pound_to_kg(weight), "kg")

#test - sleep 
# sleep = authed_client.sleep(date="2020-10-29")
# print("sleep",sleep)

# 歩数を取得（1分単位...はできない）
steps = authed_client.intraday_time_series('activities/steps', base_date=TODAY, detail_level='15min', start_time=None, end_time=None) 
print("steps",steps)

# 歩数を取得（1分単位...はできない）
excercise = authed_client.intraday_time_series('activities/minutesLightlyActive	', base_date=TODAY, detail_level='15min', start_time=None, end_time=None) 
print("excercise", excercise)