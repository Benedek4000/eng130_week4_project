from flask import render_template
from flask_mail import Message, Mail
#from app import mail
import os
import jwt
from time import time


def get_reset_token(self, expires=500):
    return jwt.encode({'reset_password': self.username, 'exp': time() + expires},
                        key=os.getenv('SECRET_KEY_FLASK'))

def send_email(user):

    token = user.get_reset_token()

    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender = os.getenv('MAIL_USERNAME')
    msg.recipients = [user.email]
    msg.html = render_template('reset_email.html', user=user, token=token)

    #mail.send(msg)




    mail.send(msg)