from flask_login import current_user
from . import db
from flask import url_for
from MysterEats_App.models import Message, User


def send_message(RECIPIENTS, restaurant_details, adv_id):

    for email_ad in RECIPIENTS:

        user = User.query.filter_by(email=email_ad).all()

        if user:
            invitation = url_for('directions', restaurant=restaurant_details, adv_id=adv_id, _external=True)

            msg = Message(author=current_user, recipient=user, body=invitation)
            db.session.add(msg)
            db.session.commit()

