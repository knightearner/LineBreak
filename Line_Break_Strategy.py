from py5paisa import *
from datetime import *
import pytz
import easyimap as e
import time


def Line_Break():

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
    time.sleep(5)

    buy_email_='buy_knightearner@outlook.com'
    sell_email_='mondaldebojit21@outlook.com'

    buy_password='Debojit@1995'
    sell_password='Rintu!1995'

    server_buy=e.connect('outlook.office365.com',buy_email_,buy_password)
    server_sell=e.connect('outlook.office365.com',sell_email_,sell_password)

    email_buy=server_buy.mail(server_buy.listids()[0])
    email_sell=server_sell.mail(server_sell.listids()[0])


    format = '%d %b %Y %H:%M'  # The format
    time_buy= datetime.strptime(email_buy.date[5:22], format)
    time_sell= datetime.strptime(email_sell.date[5:22], format)

    time_now=datetime.now(pytz.timezone('UTC'))

    flag=''
    if time_now.date()==time_sell.date() and time_now.minute==time_sell.minute and time_now.hour==time_sell.hour and email_sell.title[7:]=='SELL':
        flag='SELL'
    elif time_now.date()==time_buy.date() and time_now.minute==time_buy.minute and time_now.hour==time_buy.hour and email_buy.title[7:]=='BUY':
        flag='BUY'
    else:
        flag=''

    Nifty_Future_Code=51419361
    Nifty_Future_Lot=50

    print(str(datetime.now(pytz.timezone('Asia/Kolkata'))))

    if flag=='BUY':

        if client.positions()[0]['BodQty']<0:
            client.place_order(OrderType='B', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            time.sleep(2)
            client.place_order(OrderType='B', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            print(' BUY ')

    elif flag=='SELL':

        if client.positions()[0]['BodQty']>0:
            client.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            time.sleep(2)
            client.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            print(' SELL ')


if __name__=='__main__':
    while True:
        if datetime.now(pytz.timezone('Asia/Kolkata')).minute%5==0:
            if datetime.now(pytz.timezone('Asia/Kolkata')).hour==9 and datetime.now(pytz.timezone('Asia/Kolkata')).minute>=15:
                Line_Break()
                time.sleep(280)
            elif datetime.now(pytz.timezone('Asia/Kolkata')).hour>9 and datetime.now(pytz.timezone('Asia/Kolkata')).hour<16:
                Line_Break()
                time.sleep(280)
