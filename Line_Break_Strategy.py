from py5paisa import *
from datetime import *
import pytz
import easyimap as e
import time


def buy_login():
    buy_email_='buy_knightearner@outlook.com'

    buy_password='Debojit@1995'

    server_buy=e.connect('outlook.office365.com',buy_email_,buy_password)

    return server_buy


def sell_login():
    sell_email_='mondaldebojit21@outlook.com'

    sell_password='Rintu!1995'

    server_sell=e.connect('outlook.office365.com',sell_email_,sell_password)

    return server_sell



def Line_Break(server_buy,server_sell):

    email_buy=server_buy.mail(server_buy.listids()[0])
    email_sell=server_sell.mail(server_sell.listids()[0])


    format = '%d %b %Y %H:%M'  # The format
    time_buy= datetime.strptime(email_buy.date[5:-9], format)
    time_sell= datetime.strptime(email_sell.date[5:-9], format)

    time_now=datetime.now(pytz.timezone('UTC'))
    format='%Y-%m-%d %H:%M'
    time_now = datetime.strptime(str(time_now)[:16], format)
    time_now_list=[time_now+timedelta(minutes=i) for i in [-2,-1,0,1,2]]
    
    print('TIME NOW : ',time_now)
    
    flag=''
    if time_sell in time_now_list and email_sell.title[7:]=='SELL':
        flag='SELL'
        print('TIME SELL : ',time_sell)
    elif time_buy in time_now_list and email_buy.title[7:]=='BUY':
        flag='BUY'
        print('TIME BUY : ',time_buy)
    else:
        flag=''

    Nifty_Future_Code=51951
    Nifty_Future_Lot=50
    print('Flag Status: ',flag)
    print(str(datetime.now(pytz.timezone('Asia/Kolkata'))))
    
    if flag in ['BUY','SELL']:
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
    
    if flag=='BUY':

        if client.positions()[0]['NetQty']<0:
            client.place_order(OrderType='B', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            time.sleep(2)
            client.place_order(OrderType='B', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            print(' BUY Order Placed')

    elif flag=='SELL':

        if client.positions()[0]['NetQty']>0:
            client.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            time.sleep(2)
            client.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            print(' SELL Order Placed')


if __name__=='__main__':
    server_buy_=buy_login()
    server_sell_=sell_login()
    while True:
        if datetime.now(pytz.timezone('Asia/Kolkata')).hour==9 and datetime.now(pytz.timezone('Asia/Kolkata')).minute>=15:
                Line_Break(server_buy_,server_sell_)
                time.sleep(60)
        elif datetime.now(pytz.timezone('Asia/Kolkata')).hour>9 and datetime.now(pytz.timezone('Asia/Kolkata')).hour<16:
                Line_Break(server_buy_,server_sell_)
                time.sleep(60)
