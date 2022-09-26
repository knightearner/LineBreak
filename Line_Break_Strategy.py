from py5paisa import *
from datetime import *
from stocktrends import indicators
import pandas as pd
import time
import pytz

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
    
    tz_Ind = pytz.timezone('Asia/Kolkata')
    today = datetime.now(tz_Ind).date()

    end = str(today)
    start = str(today - timedelta(days=5))

    df = client.historical_data('N', 'C', 999920000, '5m', start, end)

    df.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Datetime': 'date'
    }, inplace=True)

    lb = indicators.LineBreak(df)
    lb.line_number = 3
    data = lb.get_ohlc_data()
    df = pd.merge(df, data[['date', 'uptrend']], on='date', how='outer')
    for i in range(len(df)):
        if df['uptrend'][i] not in [True, False]:
            df['uptrend'][i] = df['uptrend'][i - 1]

    Nifty_Future_Code=51951
    Nifty_Future_Lot=50

    try:
        print(str(datetime.now(tz_Ind)))

        if (df['uptrend'][len(df) - 1] != df['uptrend'][len(df) - 2]) and df['uptrend'][len(df) - 1] == True:
            client.place_order(OrderType='B', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            print(str(datetime.now(tz_Ind)), ' BUY @ ')

        elif (df['uptrend'][len(df) - 1] != df['uptrend'][len(df) - 2]) and df['uptrend'][len(df) - 1] == False:
            client.place_order(OrderType='S', Exchange='N', ExchangeType='D', ScripCode=Nifty_Future_Code, Qty=Nifty_Future_Lot, Price=0)
            print(str(datetime.now(tz_Ind)), 'SELL @ ')

        else:
            print('NO order Placed')

    except Exception as e:
        print(str(e))




if __name__=='__main__':
    while True:
        if datetime.now(pytz.timezone('Asia/Kolkata')).minute%5==0:
            Line_Break()
            time.sleep(280)
