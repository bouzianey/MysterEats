import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Set environment variables
username = os.environ['EMAIL_USER']
password = os.environ['EMAIL_PASS']

# administrator list
ADMINS = ['yacinebouziane2@gmail.com']

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": username,
    "MAIL_PASSWORD": password
}

POSTS_PER_PAGE = 6
