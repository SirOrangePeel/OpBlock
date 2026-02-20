from flask import Flask, Blueprint
from flask_mail import Message
from . import db, mail
import os 

mailer = Blueprint('mailer', __name__) #Create the blueprint

# message object mapped to a particular URL ‘/’
@mailer.route("/mail", methods=['POST']) 
def send_email(subject, recipient, body):
    msg = Message(
        subject=subject,
        recipients=[recipient],
        body=body
    )
    mail.send(msg)
    return "<p>Message Sent</p>"