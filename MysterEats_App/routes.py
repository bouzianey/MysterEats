from flask import render_template, url_for, flash, redirect, request
from MysterEats_App import app, db, bcrypt
from MysterEats_App.forms import *
from MysterEats_App.models import *
from MysterEats_App.PlaceSearch import *
from flask_login import login_user, current_user, logout_user, login_required
import os


@app.route('/')
@app.route('/adventure', methods=['GET', 'POST'])
def adventure():
    return render_template('adventure.html')


@app.route('/adventure/inputs', methods=['GET', 'POST'])
def adv_inputs():
    form = DisplayForm()

    # Pass adventure parameters into directions page
    if form.validate_on_submit():

        location = form.city.data
        preference = form.preference.data
        radius = form.radius.data
        if not radius:
            # Needing Testing
            radius = "15000"

        # emails = form.email_addresses.data

        # for email in emails:
        #     # send email to recipient
        #     # ADMINS[0] contains sender email address, So before you send an invitation you must set up config.py
        #     RECIPIENTS = [email]
        #     send_email(ADMINS[0], RECIPIENTS)

        # Returns a list of restaurants
        restaurant_obj = SearchRestaurant(location, preference, radius)

        # Returns a restaurant
        restaurant_details = restaurant_obj.get_best_restaurant()

        destination = str(restaurant_details['geometry']['location']['lat']) + ',' + str(
            restaurant_details['geometry']['location']['lng'])

        # Creates a Direction Object
        direction_obj = Directions(" ", destination)
        route = direction_obj.get_directions()

        address_dest = str(restaurant_details['formatted_address']).replace(' ', '+')
        current_address = str(restaurant_obj.get_current_location()).replace(' ', '+')

        uber_obj = Uber(" ", " ", " ", restaurant_details['geometry']['location']['lat'],
                        restaurant_details['geometry']['location']['lng'], restaurant_details['formatted_address'])
        uber_link = uber_obj.get_uber_link()

        return render_template('directions.html', form=form, restaurant=restaurant_details, route=route,
                               address_dest=address_dest, current_address=current_address, uber_link=uber_link)
    else:
        return render_template('adv_inputs.html', form=form)


@app.route('/adventure/directions', methods=['GET', 'POST'])
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
    # q = db.session.query(User)\
    #     .filter(User.id == UserAdventure.userID)\
    #     .filter(UserAdventure.adventureID == Adventure.adventureID)\
    #     .filter(Adventure.adventureID == AdventureRestaurant.adventureID)\
    #     .filter(AdventureRestaurant.restaurantID == Restaurant.restaurantID)\
    #     .filter_by(User.id == current_user).all()

    q = db.session.query(User, UserAdventure, Adventure)\
        .filter(User.id == UserAdventure.userID)\
        .filter(UserAdventure.adventureID == Adventure.adventureID)\
        .filter(User.id == current_user.id).all()

    return render_template('profile.html', query=q)


@app.route('/profile/settings')
def settings():
    return render_template('settings.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('adventure'))