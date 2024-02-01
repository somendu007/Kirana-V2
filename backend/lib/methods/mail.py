from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# from jinja2 import Template

SMTP_SERVER_HOST = 'smtp.gmail.com'
SMTP_SERVER_PORT = 465
SENDER_ADDRESS = "somendubug@gmail.com"
SENDER_PASSWORD = "kqaxlbtiuzwhuswt"


def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg['From'] = "Kirana Grocery Store"
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    s = smtplib.SMTP_SSL(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg=msg)
    s.quit()
    return True
