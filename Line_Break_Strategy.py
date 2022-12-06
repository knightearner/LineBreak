#import the smtplib library
import smtplib
print('1')
# creating SMTP server
server = smtplib.SMTP('smtp-mail.outlook.com',587)
print('2')
# starting TLS for security
server.starttls()

# for Authentication
server.login("mondaldebojit21@outlook.com", "Rintu!1995")

# write a message
message = """\
Subject: Hi there

{'Upper':18900,'Lower':18000}"""

# sending the email
server.sendmail("mondaldebojit21@outlook.com", "mondaldebojit21@outlook.com", message)

print("Successfully sent email")
# terminate the session
server.quit()
