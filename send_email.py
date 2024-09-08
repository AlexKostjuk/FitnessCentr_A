import os
import smtplib, ssl
from dotenv import load_dotenv
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery
# from app_test import password_email
load_dotenv()
app = Celery('send_email', broker='pyamqp://guest:guest@rabbit:5672//')



@app.task
def send_email(data, time, t_name, s_name, email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_username = os.getenv('EMAIL_USERNAME')
    email_password = os.getenv("EMAIL_PASSWORD")

    from_email = "alkost198333@gmail.com"
    to_email = str(email)
    subject = "запис до тренування"
    body = f"ви записалися до трейнера - {t_name}  на тренування з - {s_name}. {data}  числа, о {time} годині."

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