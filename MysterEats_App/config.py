import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Set environment variables
username = os.environ['EMAIL_USERNAME']
password = os.environ['EMAIL_PASSWORD']

# administrator list
ADMINS = ['testing.paulo@gmail.com']

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": username,
    "MAIL_PASSWORD": password
}

POSTS_PER_PAGE = 3