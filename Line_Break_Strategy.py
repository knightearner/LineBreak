from py5paisa import *
from datetime import *
import pytz
import easyimap as e

#buy_email_='buy_knightearner@outlook.com'
sell_email_='mondaldebojit21@outlook.com'

#buy_password='Debojit@1995'
sell_password='Rintu!1995'

#server_buy=e.connect('outlook.office365.com',buy_email_,buy_password)
server_sell=e.connect('outlook.office365.com',sell_email_,sell_password)

#email_buy=server_buy.mail(server_buy.listids()[0])
email_sell=server_sell.mail(server_sell.listids()[0])

#print(email_buy.date)
print(email_sell.date)
