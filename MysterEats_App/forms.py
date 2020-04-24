from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up!")

    # TODO Validate Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login!")


class DisplayForm(FlaskForm):
    city = StringField('What is the city?', validators=[DataRequired()])
    # TODO Implementation
    # preference = SelectField('Food Preferences',
    #                          choices=[('select', 'Select a choice...'), ('vegan', 'Vegetarian/Vegan'),
    #                                   ('bar-restaurants', 'Bar'), ('group', 'Group Setting'),
    #                                   ('family', 'Family Friendly')], default='select')
    # TODO Implementation
    # price = SelectField('Select a price range',
    #                     choices=[('select', 'Select a choice...'), ('maxprice1', '$'), ('maxprice2', '$$'),
    #                              ('maxprice3', '$$$'), ('maxprice4', '$$$$')], default='select')

    radius = SelectField('What is the radius', choices = [('16000', '10 mi'),('24000','15 mi') ,( '32000','20 mi') ,
                                                          ( '40000','25 mi')])

    # The email_addresses should contain the user's friend list from db here i just used my email addresses to test the code
    email_addresses = StringField('Email addresses')
    submit = SubmitField('Submit')


