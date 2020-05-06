#flask mail
from flask_mail import Message
from . import app
from .decorators import async_
from flask_mail import Mail
from MysterEats_App.config import *
from flask import render_template



app.config.update(mail_settings)
mail = Mail(app)



@async_
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(sender, recipients, restaurant_details, adv_id):
    subject = 'Invitation to join a meeting'
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = render_template('invitation.html', restaurant = restaurant_details, adv_id = adv_id )
    send_async_email(app, msg)