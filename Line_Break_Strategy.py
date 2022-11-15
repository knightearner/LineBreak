from py5paisa import *
from datetime import *
import pytz
import easyimap as e
import time
import pandas as pd

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

def email_login():
    _email_ = 'mondaldebojit21@outlook.com'

    _password = 'Rintu!1995'

    server_ = e.connect('outlook.office365.com', _email_, _password)

    return server_

def closest_index(lst, K):
    return min(range(len(lst)), key=lambda i: abs(lst[i] - K))


def Line_Break(server_,broker):
    email_ = server_.mail(server_.listids()[0])

    time_now = datetime.now(pytz.timezone('Asia/Kolkata'))
    print('TIME NOW : ', time_now)
    option=''
    flag = ''
    if 'SELL' in email_.body:
        flag = 'SELL'
        option='CE'
    elif 'BUY' in email_.body:
        flag = 'BUY'
        option='PE'
    elif 'CLOSE' in email_.body:
        flag = 'CLOSE'
    else:
        flag = ''
    print(flag)

    df = pd.read_csv("scripmaster-csv-format.csv")


    date_='17-Nov-22'
    print('Flag Status: ', flag)

    monthly_date='24 Nov 2022'
    
    a = [{"Exchange": "N", "ExchangeType": "D", "Symbol": "NIFTY "+monthly_date}]
    nifty_ltp = (broker.fetch_market_depth_by_symbol(a)['Data'][0]['LastTradedPrice'])

    if broker.positions() == [] :
        if flag == 'BUY' :
            l = list(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Underlyer'] == date_)]['Strikerate'])
            Strikerate = l[closest_index(l, nifty_ltp)]
            Scripcode = int(df[
                                (df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Strikerate'] == Strikerate) & (
                                        df['Underlyer'] == date_)]['Scripcode'])
            broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Scripcode, Qty=50,
                               Price=0)
            print('PE Order Placed')
        elif flag == 'SELL' :
            l = list(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Underlyer'] == date_)]['Strikerate'])
            Strikerate = l[closest_index(l, nifty_ltp)]
            Scripcode = int(df[
                                (df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Strikerate'] == Strikerate) & (
                                        df['Underlyer'] == date_)]['Scripcode'])
            broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Scripcode, Qty=50,
                               Price=0)
            print('CE Order Placed')





    for i in broker.positions():
        if i['NetQty'] < 0:
            print(i['NetQty'])
            Strikerate = df.loc[df['Scripcode'] == i['ScripCode']]['Strikerate']
            option_type = df.loc[df['Scripcode'] == i['ScripCode'], 'CpType']
            Strikerate=(int(Strikerate))
            option_type=option_type.values[0]
            
            if nifty_ltp > (Strikerate + 25):
                print('First If')
                if option_type == 'PE':
                    broker.squareoff_all()
#                     l = list(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Underlyer'] == date_)]['Strikerate'])
                    Strikerate = Strikerate + 50
                    Scripcode = int(df[
                        (df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Strikerate'] == Strikerate) & (
                                    df['Underlyer'] == date_)]['Scripcode'])
                    broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Scripcode, Qty=50,
                                       Price=0)
                    print('PE Order Placed')
                elif option_type == 'CE':
                    broker.squareoff_all()
#                     l = list(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Underlyer'] == date_)]['Strikerate'])
                    Strikerate = Strikerate + 50
                    Scripcode = int(df[
                        (df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Strikerate'] == Strikerate) & (
                                    df['Underlyer'] == date_)]['Scripcode'])
                    broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Scripcode, Qty=50,
                                       Price=0)
                    print('CE Order Placed')
            elif nifty_ltp < (Strikerate - 25):
                print('Second If')
                if option_type == 'PE':
                    broker.squareoff_all()
#                     l = list(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Underlyer'] == date_)]['Strikerate'])
                    Strikerate = Strikerate - 50
                    Scripcode = int(df[
                        (df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Strikerate'] == Strikerate) & (
                                    df['Underlyer'] == date_)]['Scripcode'])
                    broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Scripcode, Qty=50,
                                       Price=0)
                    print('PE Order Placed')
                elif option_type == 'CE':
                    broker.squareoff_all()
#                     l = list(df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Underlyer'] == date_)]['Strikerate'])
                    Strikerate = Strikerate - 50
                    Scripcode = int(df[
                        (df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Strikerate'] == Strikerate) & (
                                    df['Underlyer'] == date_)]['Scripcode'])
                    broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Scripcode, Qty=50,
                                       Price=0)
                    print('CE Order Placed')
            elif flag == 'BUY' and option_type == 'CE':
                print('Third If')
                broker.squareoff_all()
                l = list(
                    df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Underlyer'] == date_)]['Strikerate'])
                Strikerate = l[closest_index(l, nifty_ltp)]
                Scripcode = int(df[
                    (df['ISIN'] == 'NIFTY') & (df['CpType'] == 'PE') & (df['Strikerate'] == Strikerate) & (
                            df['Underlyer'] == date_)]['Scripcode'])
                broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Scripcode, Qty=50,
                                   Price=0)
                print('PE Order Placed')
            elif flag == 'SELL' and option_type == 'PE':
                print('Forth If')
                broker.squareoff_all()
                l = list(
                    df[(df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Underlyer'] == date_)]['Strikerate'])
                Strikerate = l[closest_index(l, nifty_ltp)]
                Scripcode = int(df[
                    (df['ISIN'] == 'NIFTY') & (df['CpType'] == 'CE') & (df['Strikerate'] == Strikerate) & (
                            df['Underlyer'] == date_)]['Scripcode'])
                broker.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Scripcode, Qty=50,
                                   Price=0)
                print('CE Order Placed')
            elif flag == 'CLOSE' :
                print('Fifth If')
                broker.squareoff_all()
                print('All Squared OFF')



if __name__ == '__main__':
    server_ = email_login()
    broker=broker_login()

    while True:
        if datetime.now(pytz.timezone('Asia/Kolkata')).hour == 9 and datetime.now(
                pytz.timezone('Asia/Kolkata')).minute >= 31:
            Line_Break(server_,broker)
            time.sleep(10)
        elif datetime.now(pytz.timezone('Asia/Kolkata')).hour > 9 and datetime.now(
                pytz.timezone('Asia/Kolkata')).hour < 16:
            Line_Break(server_,broker)
            time.sleep(10)
