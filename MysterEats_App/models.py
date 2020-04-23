from datetime import datetime
from MysterEats_App import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#    first_name = db.Column(db.String(20), nullable=False)
#    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
#    profile_pic = db.Column(db.String(60), nullable=False, default='default.jpg')
    user_adventure = db.relationship('UserAdventure', backref='users')

    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.password}')"


class Adventure(db.Model):
    adventureID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Adventure('{self.adventureID}','{self.name}','{self.date}')"


class UserAdventure(db.Model):
    ua_key = db.Column(db.Integer, autoincrement=True, primary_key=True)
    adventureID = db.Column(db.Integer, db.ForeignKey('adventure.adventureID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    adventure = db.relationship('Adventure', backref='user_adventure')

    def __repr__(self):
        return f"UserAdventure('{self.ua_key}','{self.adventureID}','{self.userID}')"


# class Restaurant(db.Model):
#     restaurantID = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(50), nullable=False)
#     restaurant_name = db.Column(db.String(30), nullable=False)
#     type = db.Column(db.String(20), nullable=False)
#     street = db.Column(db.String(30), nullable=False)
#     city = db.Column(db.String(30), nullable=False)
#     state = db.Column(db.String(30), nullable=False)
#     country = db.Column(db.String(2), nullable=False)
#     zipcode = db.Column(db.String(5), nullable=False)
#     phone = db.Column(db.String(10), nullable=False)
#     photo = db.Column(db.String(50), nullable=False)
#     url = db.Column(db.String(50), nullable=False)
#
#
# class AdventureRestaurant(db.Model):
#     ar_key = db.Column(db.Integer, primary_key=True)
#     adventureID = db.Column(db.Integer, db.ForeignKey('adventure.adventureID'), nullable=False)
#     restaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.restaurantID'), nullable=False)
#
#
# class Comment(db.Model):
#     commentID = db.Column(db.String(10), primary_key=True)
#     adventureID = db.Column(db.Integer, db.ForeignKey('adventure.adventureID'), nullable=False)
#     userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
#     comment = db.Column(db.String(100), nullable=False)
#     date = db.Column(db.DateTime, default=datetime.now, nullable=False)
#     photo = db.Column(db.String(50), nullable=False)