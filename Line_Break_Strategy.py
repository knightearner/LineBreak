from py5paisa import *
from datetime import *
import pytz
import easyimap as e
import time

def email_login():
    _email_='mondaldebojit21@outlook.com'

    _password='Rintu!1995'

    server_=e.connect('outlook.office365.com',_email_,_password)

    return server_

def Line_Break(server_):

   
    email_=server_.mail(server_.listids()[0])

    time_now=datetime.now(pytz.timezone('Asia/Kolkata'))
    print('TIME NOW : ',time_now)
    
    flag=''
    if int(email_.title[-2:])==-1:
        flag='SELL'
    elif int(email_.title[-2:])==1:
        flag='BUY'
    else:
        flag=''

    Nifty_Future_Code=52309
    Nifty_Future_Lot=300
    
    print('Flag Status: ',flag)
    
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
    server_=email_login()
    
    while True:
        if datetime.now(pytz.timezone('Asia/Kolkata')).hour==9 and datetime.now(pytz.timezone('Asia/Kolkata')).minute>=15:
                Line_Break(server_)
                time.sleep(10)
        elif datetime.now(pytz.timezone('Asia/Kolkata')).hour>9 and datetime.now(pytz.timezone('Asia/Kolkata')).hour<16:
                Line_Break(server_)
                time.sleep(10)
