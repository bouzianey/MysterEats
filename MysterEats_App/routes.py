from flask import render_template, url_for, flash, redirect, request
from MysterEats_App import app, db, bcrypt
from MysterEats_App.forms import LoginForm, RegistrationForm
from MysterEats_App.models import User
from flask_login import login_user, current_user, logout_user, login_required
import os


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    # checks if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('adventure'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # checks if user exists
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('adventure'))
        else:
            flash('Login Failed. Check password is correct', 'danger')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # checks if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('adventure'))
    form = RegistrationForm()

    # adds new user to the database
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now create an adventure!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/profile/settings')
def settings():
    return render_template('settings.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('adventure'))