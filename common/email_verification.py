import random
import re
import smtplib
import ssl
from email.message import EmailMessage

from config import constants

MAX_TRY_REPLY = 10
context = ssl.create_default_context()


def generate():
    checkcode = ""

    for i in range(6):
        current = random.randrange(0, 9, 2)
        if current != i:
            temp = chr(random.randint(65, 90))
        else:
            temp = random.randint(0, 9)
        checkcode += str(temp)

    return checkcode


def is_mit_harvard_email(email):
    return re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@(.*\.mit\.edu|mit\.edu|harvard\.edu|.*\.harvard\.edu|hbs\.edu)$', email.lower())


def send_mail(addr, token, subject = constants.email_subject):
    msg = EmailMessage()
    msg['From'] = constants.default_email
    msg['To'] = addr
    msg['Subject'] = subject
    msg.set_content(constants.email_content % (addr, token))

    with smtplib.SMTP_SSL("smtp.dreamhost.com", constants.SMTP_PORT, context=context) as server:
        server.login(constants.USERNAME, constants.PASSWORD)
        server.send_message(msg)