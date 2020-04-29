from MysterEats_App.Email import *
from MysterEats_App.config import *
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from MysterEats_App import app, db, bcrypt
from MysterEats_App.forms import *
from MysterEats_App.models import *
from MysterEats_App.PlaceSearch import *
from MysterEats_App.user_util import *
import json

@login_required
@app.route('/')
@app.route('/adventure', methods=['GET', 'POST'])
def adventure():
    return render_template('adventure.html')

@login_required
@app.route('/adventure/inputs' , methods=['GET', 'POST'])
def adv_inputs():

    form = DisplayForm()


    if form.validate_on_submit():

        location= form.city.data
        preference= form.preference.data
        radius= form.radius.data
        email = form.email_address.data

        restaurant_obj = SearchRestaurant(location,preference,radius)
        restaurant_details = restaurant_obj.get_best_restaurant()

        destination = str(restaurant_details['geometry']['location']['lat']) +','+ str(restaurant_details['geometry']['location']['lng'])


        direction_obj = Directions(" ",destination)
        route = direction_obj.get_directions()

        address_dest = str(restaurant_details['formatted_address']).replace(' ','+')
        current_address = str(restaurant_obj.get_current_location()).replace(' ','+')

        uber_obj = Uber(" "," "," ",restaurant_details['geometry']['location']['lat'],restaurant_details['geometry']['location']['lng'],restaurant_details['formatted_address'])
        uber_link = uber_obj.get_uber_link()

        user = User.query.filter_by(email="yogataga@gmail.com").first()
        RECIPIENTS = [email]
        send_email(ADMINS[0],RECIPIENTS,restaurant_details, address_dest, current_address)

        return render_template('directions.html', form=form, restaurant = restaurant_details , route=route, address_dest = address_dest, current_address = current_address , uber_link = uber_link, email=email)
    else:
        return render_template('adv_inputs.html', form=form)

@login_required
@app.route('/adventure/directions/<restaurant>/<route>/<address_dest>/<current_address>', methods=['GET', 'POST'])
def directions( restaurant, route, address_dest, current_address):

    return render_template('directions.html', restaurant = restaurant, route = route,  address_dest = address_dest, current_address = current_address)



@app.route('/adventure/following/<restaurant>/<address_dest>/<current_address>', methods=['GET', 'POST'])
@login_required
def following(restaurant, address_dest, current_address):

    #convert restaurant details from a string to a dict
    restaurant_format = restaurant.replace('\'','\"')
    restaurant_dict = json.loads(restaurant_format)

    destination = str(restaurant_dict['geometry']['location']['lat']) +','+ str(restaurant_dict['geometry']['location']['lng'])


    direction_obj = Directions(" ",destination)
    route = direction_obj.get_directions()

    address_dest = str(restaurant_dict['formatted_address']).replace(' ','+')
    current_address = str(direction_obj.get_origin()).replace(' ','+')

    uber_obj = Uber(" "," "," ",restaurant_dict['geometry']['location']['lat'],restaurant_dict['geometry']['location']['lng'],restaurant_dict['formatted_address'])
    uber_link = uber_obj.get_uber_link()


    return render_template('directions.html', restaurant = restaurant_dict, route = route, address_dest = address_dest, current_address = current_address ,uber_link =uber_link)



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

    q = db.session.query(User, UserAdventure, Adventure).filter(User.id == UserAdventure.userID) .filter(UserAdventure.adventureID == Adventure.adventureID) .filter(User.id == current_user.id).all()
    image_file = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('profile.html', query=q, image_file=image_file)


@app.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def settings():

    form = SettingsForm()
    if form.validate_on_submit():

        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            current_user.profile_pic = picture_file

        if form.email.data:
            # checks if user exists
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email Already Exists', 'danger')
            else:
                current_user.email = form.email.data
        if form.fname.data != '':
            current_user.first_name = form.fname.data
        if form.lname.data != '':
            current_user.last_name = form.lname.data
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('settings.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('adventure'))

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('adventure'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been set with instructions to reset your password.', 'info')
        # return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # checks to see if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('adventure'))

    # calls user verify password token
    user = User.verify_reset_token(token)

    # checks the token for expiration or validness
    if user is None:
        flash('That is an invalid token or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    # uploads user's password into the database on submit
    if form.validate_on_submit():
        # encrypt the password into a string hash
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user.password = hashed_password
        db.session.commit()
        #TODO : implement flask template
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
