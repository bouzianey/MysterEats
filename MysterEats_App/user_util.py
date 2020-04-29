import secrets
from PIL import Image
from flask import url_for, current_app
from MysterEats_App.Email import *

from flask_mail import Message

# turns picture filenames into hashes to prevent duplicate filenames and saves it
def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # saves picture into the profile_pics folder and resize image
    picture_path = os.path.join(current_app.root_path, 'static\profile_pics', picture_fn)
    output_size = (125, 125)
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