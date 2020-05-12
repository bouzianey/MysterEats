from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from MysterEats_App import app, db, login_manager
from flask_login import UserMixin
from time import time
import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    user_adventure = db.relationship('UserAdventure', backref='users')

    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):

        return f"User('{self.id}','{self.email}','{self.password}')"

    def get_reset_token(self, expires_sec=1800):

        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):

        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

class Adventure(db.Model):

    adventureID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    host = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    comments = db.relationship('Comment', backref='adventure')
    adventure_restaurant = db.relationship('AdventureRestaurant', backref='adventure_restaurants')

    def __repr__(self):
        return f"Adventure('{self.adventureID}','{self.name}','{self.date}')"


class UserAdventure(db.Model):

    ua_key = db.Column(db.Integer, autoincrement=True, primary_key=True)
    adventureID = db.Column(db.Integer, db.ForeignKey('adventure.adventureID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    adventure = db.relationship('Adventure', backref='user_adventure')

    def __repr__(self):
        return f"UserAdventure('{self.ua_key}','{self.adventureID}','{self.userID}')"

class Restaurant(db.Model):

    restaurantID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String(50), nullable=True)
    restaurant_name = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(20), nullable=True)
    street = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=True)
    phone = db.Column(db.String(11), nullable=True)
    photo = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(50), nullable=True)

    def __repr__(self):

        return f"Restaurant('{self.restaurantID}','{self.restaurant_name}','{self.description}','{self.type}','" \
 \
        f"{self.street}','{self.city}','{self.country}','{self.zipcode}','{self.zipcode}','{self.phone}','" \
 \
        f"{self.photo}','{self.url}')"


class AdventureRestaurant(db.Model):

    ar_key = db.Column(db.Integer, autoincrement=True, primary_key=True)
    adventureID = db.Column(db.Integer, db.ForeignKey('adventure.adventureID'), nullable=False)
    restaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.restaurantID'), nullable=False)
    restaurant = db.relationship('Restaurant', backref='adventure_restaurants')

    def __repr__(self):
        return f"AdventureRestaurant('{self.ar_key}','{self.adventureID}','{self.restaurantID}')"


class Comment(db.Model):

    commentID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    adventureID = db.Column(db.Integer, db.ForeignKey('adventure.adventureID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    photo = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"Comment('{self.commentID}','{self.userID}','{self.comment}','{self.date}','"

class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    sender_first_name = db.Column(db.String(20), nullable=False)
    sender_last_name = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '{}'.format(self.body)

    def get_sender_fname(self):
        return '{}'.format(self.sender_first_name)

    def get_sender_lname(self):
        return '{}'.format(self.sender_last_name)

    def get_msg_timestamp(self):
        return '{}'.format(self.timestamp)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))