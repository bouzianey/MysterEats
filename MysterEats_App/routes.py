from MysterEats_App.Email import *
from MysterEats_App.config import *
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, jsonify
from MysterEats_App import app, db, bcrypt
from MysterEats_App.forms import *
from MysterEats_App.models import *
from MysterEats_App.PlaceSearch import *
from MysterEats_App.notify_user import send_message
from MysterEats_App.user_util import *
import json
from MysterEats_App.forms import MessageForm
from MysterEats_App.models import Message
from MysterEats_App.config import *




@app.route('/')
@app.route('/adventure', methods=['GET', 'POST'])
def adventure():
    return render_template('adventure.html')



@app.route('/adventure/inputs/<int:adv_id>', methods=['GET', 'POST'])
@login_required
def adv_inputs(adv_id):

    form = DisplayForm()

    if form.validate_on_submit():

        location= form.city.data
        preference= form.preference.data
        radius= form.radius.data
        email_ad = form.email_address.data
        adventureName = form.adventureName.data
        RECIPIENTS = [email_ad]


        restaurant_obj = SearchRestaurant(location,preference,radius)
        restaurant_details = restaurant_obj.get_best_restaurant()

        destination = str(restaurant_details['geometry']['location']['lat']) +','+ str(restaurant_details['geometry']['location']['lng'])


        direction_obj = Directions(" ",destination)
        route = direction_obj.get_directions()

        address_dest = str(restaurant_details['formatted_address']).replace(' ','+')
        current_address = str(restaurant_obj.get_current_location()).replace(' ','+')

        uber_obj = Uber(" "," "," ",restaurant_details['geometry']['location']['lat'],restaurant_details['geometry']['location']['lng'],restaurant_details['formatted_address'])
        uber_link = uber_obj.get_uber_link()

        if adv_id == 0:
            adv_id = addAdventure(current_user.id, adventureName )
        else:
            adv_id = int(adv_id)
            q = db.session.query(User).filter(UserAdventure.adventureID == adv_id).all()
            if q:
                RECIPIENTS = [q[1].email]
                email_ad = q[1].email

        res_id = addRestaurant(restaurant_details)
        addAdventureRestaurant(adv_id, res_id)
        restaurant_details['formatted_address'] = restaurant_details['formatted_address'].replace(',',' ')
        restaurant_details['name'] = restaurant_details['name'].replace('\'',' ')

        if RECIPIENTS:
            send_email(ADMINS[0], RECIPIENTS, restaurant_details, adv_id)
            send_message(email_ad, restaurant_details,adv_id)

        return render_template('directions.html',adv_id=adv_id,  host = "yes", form=form, restaurant = restaurant_details , route=route, address_dest = address_dest, current_address = current_address , uber_link = uber_link, email=email_ad)
    else:
        return render_template('adv_inputs.html',adv_id=adv_id, form=form)


@app.route('/adventure/following/<host>/<restaurant>/<int:adv_id>', methods=['GET', 'POST'])
@login_required
def following( host,restaurant, adv_id):

    #convert restaurant details from a string to a dict
    restaurant_format = restaurant.replace('\'','\"')
    restaurant_dict = json.loads(restaurant_format)

    return render_template('following.html', host = host, restaurant = restaurant_dict, adv_id = adv_id )



@app.route('/adventure/directions/<restaurant>/<int:adv_id>', methods=['GET', 'POST'])
@login_required
def directions(restaurant,adv_id):

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

    #assign adventure ID
    q = db.session.query(UserAdventure).filter(UserAdventure.adventureID == adv_id)\
        .filter(UserAdventure.userID == current_user.id).first()
    if q is None:
        ua = UserAdventure(userID=current_user.id, adventureID=adv_id)
        db.session.add(ua)
        db.session.commit()

    return render_template('directions.html', adv_id = adv_id, host = "no", restaurant = restaurant_dict, route = route, address_dest = address_dest, current_address = current_address ,uber_link =uber_link)


@app.route('/adventure/summary/<int:adv_id>', methods=['GET', 'POST'])
def summary(adv_id):

    form = CommentPost()
    adv = Adventure.query.get_or_404(adv_id)
    dic = get_summary(adv_id)

    if form.validate_on_submit():

        picture_file = None
        if form.comment_pic.data:
            picture_file = save_picture(form.comment_pic.data)

        comment = Comment(adventureID=adv.adventureID, userID=current_user.id, comment=form.content.data, photo=picture_file)
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('summary', adv_id=adv.adventureID))

    return render_template('summary.html', adv=adv, dic=dic, form=form)


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

@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@app.route('/user/<email_ad>')
@login_required
def user(email_ad):
    user = User.query.filter_by(email=email_ad).first_or_404()
    return render_template('user.html', user=user)

@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)



