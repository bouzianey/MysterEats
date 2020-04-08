from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import googlemaps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@app.route('/')
@app.route('/adventure', methods=['GET', 'POST'])
def adventure():
    return render_template('adventure.html')


@app.route('/adventure/inputs')
def adv_inputs():
    return render_template('adv_inputs.html')


@app.route('/adventure/directions')
def directions():
    return render_template('directions.html')


@app.route('/adventure/following')
def following():
    return render_template('following.html')


@app.route('/adventure/summary')
def summary():
    return render_template('summary.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/profile/settings')
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run()
