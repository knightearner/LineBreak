import requests
import json
import math
import mibian
from dateutil.parser import parse
from py5paisa import *
from datetime import *
import pytz
import easyimap as e
import time
import ast
import pandas as pd
import smtplib


# Method to get nearest strikes
def round_nearest(x, num=50): return int(math.ceil(float(x) / num) * num)


def nearest_strike_bnf(x): return round_nearest(x, 100)


def nearest_strike_nf(x): return round_nearest(x, 50)


# Urls for fetching Data
url_oc = "https://www.nseindia.com/option-chain"
url_bnf = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'accept-language': 'en,gu;q=0.9,hi;q=0.8',
    'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()


# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)


def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if (response.status_code == 401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if (response.status_code == 200):
        return response.text
    return ""


def set_header():
    global bnf_ul
    global nf_ul
    global bnf_nearest
    global nf_nearest
    response_text = get_data(url_indices)
    data = json.loads(response_text)
    for index in data["data"]:
        if index["index"] == "NIFTY 50":
            nf_ul = index["last"]
        if index["index"] == "NIFTY BANK":
            bnf_ul = index["last"]
    bnf_nearest = nearest_strike_bnf(bnf_ul)
    nf_nearest = nearest_strike_nf(nf_ul)

df_oi = pd.DataFrame()

# Fetching CE and PE data based on Nearest Expiry Date
def print_oi(num, step, nearest, url,weekly_date):
    strike = nearest - (step * num)
    start_strike = nearest - (step * num)
    response_text = get_data(url)
    data = json.loads(response_text)
    strikePrice = []
    callDelta = []
    putDelta = []
    callLTP = []
    putLTP = []

#     currExpiryDate = data["records"]["expiryDates"][0]
    currExpiryDate=weekly_date
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike + (step * num * 2):
#                 date_time_obj = parse((data["records"]["expiryDates"][0]))
                date_time_obj=parse(currExpiryDate)

                c = mibian.BS([nf_ul, item["strikePrice"], 10, ((date_time_obj.date() - date.today()).days) + 1],volatility=item["CE"]["impliedVolatility"])
                p = mibian.BS([nf_ul, item["strikePrice"], 10, ((date_time_obj.date() - date.today()).days) + 1],volatility=item["PE"]["impliedVolatility"])

                strikePrice.append(item["strikePrice"])
                callDelta.append(c.callDelta)
                putDelta.append(p.putDelta)
                callLTP.append(item["CE"]["lastPrice"])
                putLTP.append(item["PE"]["lastPrice"])
                # print(item["strikePrice"],c.callDelta,p.putDelta)
                strike = strike + step
    # print(strikePrice,callDelta,putDelta)
    df_oi['strikePrice'] = strikePrice
    df_oi['callDelta'] = callDelta
    df_oi['callLTP'] = callLTP
    df_oi['putDelta'] = putDelta
    df_oi['putLTP'] = putLTP


def oi(weekly_date):
    set_header()
    print_oi(10, 50, nf_nearest, url_nf,weekly_date)
    df_oi.set_index('strikePrice', inplace=True)
    return df_oi
  
  
  
  
  

def broker_login():
    cred = {
        "APP_NAME": "5P51419361",
        "APP_SOURCE": "11179",
        "USER_ID": "FKTvPb6GrxX",
        "PASSWORD": "Rf7SoLvxXcj",
        "USER_KEY": "LCHhAHfRrkeDwQkjHyGtQGFmBkl1h50T",
        "ENCRYPTION_KEY": "c5yN3Ny1k4zj272fI40YDzHrF4Q1dics"
    }

    client = FivePaisaClient(email="mondaldebojit21@gmail.com", passwd="Rintu!1995", dob="19951021", cred=cred)
    client.login()
    return client

def email_read():
    _email_ = 'mondaldebojit21@outlook.com'

    _password = 'Rintu!1995'

    server_read = e.connect('outlook.office365.com', _email_, _password)

    return server_read

def email_send():
    
    server = smtplib.SMTP('smtp-mail.outlook.com',587)
    server.starttls()
    server.login("mondaldebojit21@outlook.com", "Rintu!1995")
    
    return server
    
    
def closest_index(lst, K):
    return min(range(len(lst)), key=lambda i: abs(lst[i] - K))

def option_sell(server_read,server_send,broker):
    df = pd.read_csv("scripmaster-csv-format.csv")
    
    lot=50

    weekly_date = '15-Dec-22'
    weekly_date_ = '15-Dec-2022'
    monthly_date = '29 Dec 2022'
    

#     a = [{"Exchange": "N", "ExchangeType": "D", "Symbol": "NIFTY " + monthly_date}]
    a = [{"Exchange": "N", "ExchangeType": "C", "Symbol": "NIFTY"}]
    nifty_ltp = (broker.fetch_market_depth_by_symbol(a)['Data'][0]['LastTradedPrice'])

    count=0
    for i in broker.positions():
        if i['NetQty']<0:
            count+=1

    
    if broker.positions()== [] or count==0:
        l = list(df[(df['ISIN'] == 'NIFTY')  & (df['Underlyer'] == weekly_date)]['Strikerate'])
        l=(list(set(l)))
        Strikerate = (l[closest_index(l, nifty_ltp)])
        CE_Scripcode = int(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Strikerate'] == Strikerate) & (df['Underlyer'] == weekly_date)]['Scripcode'])
        PE_Scripcode = int(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Strikerate'] == Strikerate) & (df['Underlyer'] == weekly_date)]['Scripcode'])
        
        broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=CE_Scripcode, Qty=lot,Price=0)
        broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=PE_Scripcode, Qty=lot,Price=0)
        time.sleep(10)
        
        margin=0
        for i in broker.positions():
            if i['NetQty']<0: 
                margin+=int(i['LTP'])
        upper_margin=Strikerate+margin
        lower_margin=Strikerate-margin
        
        message = """\
Subject: Nifty BreakEven Margin

{'Upper':"""+str(nifty_ltp+(abs(upper_margin-nifty_ltp)/3))+""",'Lower':"""+str(nifty_ltp-(abs(lower_margin-nifty_ltp)/3))+""",'Upper_Breakeven':"""+str(upper_margin)+""",'Lower_Breakeven':"""+str(lower_margin)+"""}"""
        server_send.sendmail("mondaldebojit21@outlook.com", "mondaldebojit21@outlook.com", message)
        
        upper_Strikerate = (l[closest_index(l, upper_margin)])
        lower_Strikerate = (l[closest_index(l, lower_margin)])
        
        CE_Scripcode = int(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Strikerate'] == upper_Strikerate) & (df['Underlyer'] == weekly_date)]['Scripcode'])
        PE_Scripcode = int(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Strikerate'] == lower_Strikerate) & (df['Underlyer'] == weekly_date)]['Scripcode'])
        
        broker.place_order(OrderType='B', Exchange='N', ExchangeType='D', ScripCode=CE_Scripcode, Qty=lot,Price=0)
        broker.place_order(OrderType='B', Exchange='N', ExchangeType='D', ScripCode=PE_Scripcode, Qty=lot,Price=0)
        
    elif count==2:

        email_ = server_read.mail(server_read.listids()[0])

        upper_margin=(ast.literal_eval(email_.body))['Upper']
        lower_margin=(ast.literal_eval(email_.body))['Lower']
        ce_strike_list=0
        pe_strike_list=0
        delta=0
        df_oi=oi(weekly_date_)

        if nifty_ltp>upper_margin or nifty_ltp<lower_margin:
            
            for i in broker.positions():

                if i['NetQty']<0 and (df[df['Scripcode'] == i['ScripCode']]['CpType'].values[0])=='CE':
                    ce_strike_list=(int(df[df['Scripcode'] == i['ScripCode']]['Strikerate']))
                    delta+=df_oi[df_oi.index==(ce_strike_list)]['callDelta']

                elif i['NetQty']<0 and (df[df['Scripcode'] == i['ScripCode']]['CpType'].values[0])=='PE':
                    pe_strike_list=(int(df[df['Scripcode'] == i['ScripCode']]['Strikerate']))
                    delta+=df_oi[df_oi.index==(pe_strike_list)]['putDelta']

            delta=delta.values[0]
            # When falling market need to increase lower BreakEven
            if delta<0:
                delta=delta*-1
                l=list(df_oi['callDelta'])
                Strikerate=list(df_oi.index)[closest_index(l, delta)]
                CE_Scripcode = int(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Strikerate'] == Strikerate) & (df['Underlyer'] == weekly_date)]['Scripcode'])
                broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=CE_Scripcode, Qty=lot,Price=0)
                for i in broker.positions():
                    if i['ScripCode']==CE_Scripcode:
                        lower_margin-=i['LTP']
                        break
                
            # When Rising market need to increase Upper BreakEven
            elif delta>0:
                delta=delta*-1
                l=list(df_oi['putDelta'])
                Strikerate=list(df_oi.index)[closest_index(l, delta)]
                PE_Scripcode = int(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Strikerate'] == Strikerate) & (df['Underlyer'] == weekly_date)]['Scripcode'])
                broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=PE_Scripcode, Qty=lot,Price=0)
                for i in broker.positions():
                    if i['ScripCode']==PE_Scripcode:
                        upper_margin+=i['LTP']
                        break

                       
            message = """\
Subject: Nifty BreakEven Margin

{'Upper':"""+str(nifty_ltp+(abs(upper_margin-nifty_ltp)/3))+""",'Lower':"""+str(nifty_ltp-(abs(lower_margin-nifty_ltp)/3))+""",'Upper_Breakeven':"""+str(upper_margin)+""",'Lower_Breakeven':"""+str(lower_margin)+"""}"""
            server_send.sendmail("mondaldebojit21@outlook.com", "mondaldebojit21@outlook.com", message)
    
    
    elif count==3:
        email_ = server_read.mail(server_read.listids()[0])

        upper_margin=(ast.literal_eval(email_.body))['Upper']
        lower_margin=(ast.literal_eval(email_.body))['Lower']
        ce_strike_list=0
        pe_strike_list=0
        delta=0
        df_oi=oi(weekly_date_)
        
        if nifty_ltp>upper_margin or nifty_ltp<lower_margin:
            min_=10000
            min_script=0
            for i in broker.positions():
                if i['LTP']<min_ and i['NetQty']<0:
                    min_=i['LTP']
                    min_script=i['ScripCode']
            
            broker.place_order(OrderType='B', Exchange='N', ExchangeType='D', ScripCode=min_script, Qty=lot,Price=0)
            
            for i in broker.positions():

                if i['NetQty']<0 and (df[df['Scripcode'] == i['ScripCode']]['CpType'].values[0])=='CE':
                    ce_strike_list=(int(df[df['Scripcode'] == i['ScripCode']]['Strikerate']))
                    delta+=df_oi[df_oi.index==(ce_strike_list)]['callDelta']

                elif i['NetQty']<0 and (df[df['Scripcode'] == i['ScripCode']]['CpType'].values[0])=='PE':
                    pe_strike_list=(int(df[df['Scripcode'] == i['ScripCode']]['Strikerate']))
                    delta+=df_oi[df_oi.index==(pe_strike_list)]['putDelta']

            delta=delta.values[0]
            # When falling market need to increase lower BreakEven
            if delta<0:
                delta=delta*-1
                l=list(df_oi['callDelta'])
                Strikerate=list(df_oi.index)[closest_index(l, delta)]
                CE_Scripcode = int(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Strikerate'] == Strikerate) & (df['Underlyer'] == weekly_date)]['Scripcode'])
                broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=CE_Scripcode, Qty=lot,Price=0)
                for i in broker.positions():
                    if i['ScripCode']==CE_Scripcode:
                        lower_margin-=i['LTP']
                        break
                
            # When Rising market need to increase Upper BreakEven
            elif delta>0:
                delta=delta*-1
                l=list(df_oi['putDelta'])
                Strikerate=list(df_oi.index)[closest_index(l, delta)]
                PE_Scripcode = int(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Strikerate'] == Strikerate) & (df['Underlyer'] == weekly_date)]['Scripcode'])
                broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=PE_Scripcode, Qty=lot,Price=0)
                for i in broker.positions():
                    if i['ScripCode']==PE_Scripcode:
                        upper_margin+=i['LTP']
                        break

                       
            message = """\
Subject: Nifty BreakEven Margin

{'Upper':"""+str(nifty_ltp+(abs(upper_margin-nifty_ltp)/3))+""",'Lower':"""+str(nifty_ltp-(abs(lower_margin-nifty_ltp)/3))+""",'Upper_Breakeven':"""+str(upper_margin)+""",'Lower_Breakeven':"""+str(lower_margin)+"""}"""
            server_send.sendmail("mondaldebojit21@outlook.com", "mondaldebojit21@outlook.com", message)
        
        
        
        
        
        

if __name__ == '__main__':
    server_read = email_read()
    server_send = email_send()
    broker = broker_login()
    while True:
        
        if datetime.now(pytz.timezone('Asia/Kolkata')).hour == 9 and datetime.now(pytz.timezone('Asia/Kolkata')).minute >= 16:
            option_sell(server_read,server_send,broker)
            time.sleep(10)
        elif datetime.now(pytz.timezone('Asia/Kolkata')).hour > 9 and datetime.now(pytz.timezone('Asia/Kolkata')).hour < 16:
            option_sell(server_read,server_send,broker)
            time.sleep(10)  
