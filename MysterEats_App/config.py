import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Set environment variables
os.environ['EMAIL_USERNAME'] = ''#'testing.paulo@gmail.com'
os.environ['EMAIL_PASSWORD'] = ''#'oisffloohzgomkc'

# administrator list
ADMINS = ['yacinebouziane2@gmail.com']

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USERNAME'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

POSTS_PER_PAGE = 6
