from MysterEats_App import db
import secrets
from PIL import Image
from flask import url_for, current_app
from MysterEats_App.Email import *
from MysterEats_App.models import *

from flask_mail import Message

# turns picture filenames into hashes to prevent duplicate filenames and saves it
def save_picture(form_picture, filepath, width=125, height=125):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # saves picture into a folder and resize image
    picture_path = os.path.join(current_app.root_path, filepath, picture_fn)
    output_size = (width, height)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):

    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:

    {url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email.
Token will expire in 30 minutes...
A Black Spoons Production Application.
'''
    mail.send(msg)


def get_summary(adventureID, page):

    dic = {'attendees': [], 'host': {}, 'adventure': {}, 'restaurants': [], 'comments': [], 'pages': [], 'curr_page': 1}

    q = db.session.query(User, UserAdventure, Adventure).filter(User.id == UserAdventure.userID)\
        .filter(UserAdventure.adventureID == Adventure.adventureID)\
        .filter(Adventure.adventureID == AdventureRestaurant.adventureID)\
        .filter(AdventureRestaurant.restaurantID == Restaurant.restaurantID)\
        .filter(Adventure.adventureID == adventureID).all()

# Adding Adventure id, name and date object
    dic['adventure']['id'] = q[0][2].adventureID
    dic['adventure']['name'] = q[0][2].name
    dic['adventure']['date'] = q[0][2].date
    dic['adventure']['host_id'] = q[0][2].host

# Adding Attendees
    for i in q:
        dic['attendees'].append(
            {'id': i[0].id, 'first_name': i[0].first_name, 'last_name': i[0].last_name, 'email': i[0].email,
            'profile_pic': i[0].profile_pic})

    # Adding Host
    for i in dic['attendees']:
        if i['id'] == dic['adventure']['host_id']:
            dic['host']['user_id'] = i['id']
            dic['host']['first_name'] = i['first_name']
            dic['host']['last_name'] = i['last_name']
            dic['host']['email'] = i['email']
            dic['host']['profile_pic'] = i['profile_pic']

    # Adding Restaurants
    for i in q[0][2].adventure_restaurant:
        dic['restaurants'].append({'restaurantID': i.restaurant.restaurantID, 'desc': i.restaurant.description,
                                   'name': i.restaurant.restaurant_name, 'type': i.restaurant.type,
                                   'street': i.restaurant.street, 'city': i.restaurant.city,
                                   'state': i.restaurant.state, 'country': i.restaurant.country,
                                   'zipcode': i.restaurant.zipcode, 'phone': i.restaurant.phone,
                                   'url': i.restaurant.url})

    c = db.session.query(User, Adventure, Comment) \
     \
    .filter(Adventure.adventureID == Comment.adventureID) \
     \
    .filter(Comment.userID == User.id) \
     \
    .filter(Adventure.adventureID == adventureID) \
     \
    .order_by(Comment.date.desc()).paginate(page=page, per_page=5)

    # Adding Comments
    for i in c.items:
        dic['comments'].append({'user_id': i[0].id, 'first_name': i[0].first_name, 'last_name': i[0].last_name,
                                'date': i[2].date, 'profile_pic': i[0].profile_pic, 'content': i[2].comment,
                                'content_photo': i[2].photo})

    # Adding pages
    for i in c.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2):
        dic['pages'].append(i)

    # Adding current page
    dic['curr_page'] = c.page

    return dic

def addAdventure(hostID, adventureName ):

    adv = Adventure(name = adventureName , host= hostID)
    db.session.add(adv)
    db.session.commit()

    #ua = UserAdventure(adventureID = db.session.query(adv.adventureID).filter(adventureName == adv.name).filter(hostID == adv.host), userID= hostID)
    q = db.session.query(Adventure).filter(Adventure.host == hostID).filter(Adventure.name == adventureName).first()
    ua = UserAdventure(adventureID = q.adventureID ,  userID= hostID)
    db.session.add(ua)
    db.session.commit()
    return q.adventureID

def addRestaurant(restaurant):

    restaurantList = restaurant['formatted_address'].split(", ")
    zipState =  restaurantList[2].split(" ")
    zipCode = zipState[0]
    state = zipState[1]
    res = Restaurant(restaurant_name= restaurant['name'], street= restaurantList[0], city = restaurantList[1], state = state, country= restaurantList[3], zipcode= zipCode)
    db.session.add(res)
    db.session.commit()
    q = db.session.query(Restaurant).filter(Restaurant.street == restaurantList[0]).filter(Restaurant.city == restaurantList[1]).filter(Restaurant.restaurant_name == restaurant["name"]).first()
    return q.restaurantID

def addAdventureRestaurant(adventureID, restautantID):

    ar = AdventureRestaurant(adventureID= adventureID, restaurantID= restautantID)
    db.session.add(ar)
    db.session.commit()


