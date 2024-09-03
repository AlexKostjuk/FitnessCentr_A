import os
import smtplib, ssl
from dotenv import load_dotenv
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery
# from app_test import password_email
load_dotenv()
app = Celery('send_email', broker='pyamqp://guest@localhost//')

@app.task
def sum_test(a, b):
    c = a+b
    print(c)
    return c

@app.task
def send_email(data, time):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_username = os.getenv('EMAIL_USERNAME')
    email_password = os.getenv("EMAIL_PASSWORD")

    from_email = "alkost198333@gmail.com"
    to_email = "alkost198333@gmail.com"
    subject = "alarm Temp"
    body = f"temp CP = {data}, {time}."

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_username, email_password)
        server.send_message(msg)
        print(f"Лист успішно відправлений!  {to_email}")
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        server.quit()