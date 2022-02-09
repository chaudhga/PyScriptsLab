import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port_number =1025
msg = MIMEMultipart()
msg['From'] = '084008421@protonmail.com'
msg['To'] = '67733543@protonmail.com'
msg['Subject'] = 'My Test Mail '
message = 'This is the body of the mail'
msg.attach(MIMEText(message))
mailserver = smtplib.SMTP('127.0.0.1',port_number)
mailserver.login("084008421@protonmail.com", "JAWAxvP293lT7rvLnwPe1w")
mailserver.sendmail('084008421@protonmail.com','67733543@protonmail.com',msg.as_string())
mailserver.quit()