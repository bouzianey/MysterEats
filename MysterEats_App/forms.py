from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from MysterEats_App.models import User


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')

class CommentPost(FlaskForm):

    content = TextAreaField('Post Content', validators=[DataRequired(), Length(max=100)])
    comment_pic = FileField('Post Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Submit!")

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=30)])
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up!")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login!")


class DisplayForm(FlaskForm):
    adventureName = StringField('What is the adventure name ?', validators=[Optional(), Length(min=5, max=20)])
    city = StringField('What is the city?', validators=[DataRequired()])

    preference = SelectField('Food Preferences',
                              choices=[('select', 'Select a choice...'), ('vegan+vegetarian', 'Vegetarian/Vegan'),
                                       ('bar+restaurants', 'Bar'), ('group', 'Group Setting'),
                                       ('family', 'Family Friendly')], default='select')
    # TODO Implementation
    # price = SelectField('Select a price range',
    #                     choices=[('select', 'Select a choice...'), ('maxprice1', '$'), ('maxprice2', '$$'),
    #                              ('maxprice3', '$$$'), ('maxprice4', '$$$$')], default='select')

    radius = SelectField('What is the radius', choices = [('16000', '10 mi'),('24000','15 mi') ,( '32000','20 mi') ,
                                                          ( '40000','25 mi')],default='15000')
    email_address = StringField('Email addresses', validators=[Optional()], render_kw={"placeholder": "test@email.com;test2@email"})
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login!")


class SettingsForm(FlaskForm):

    email = StringField('Email', validators=[Optional(), Email(), Length(max=30)])
    fname = StringField('First Name', validators=[Optional(), Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[Optional(), Length(min=2, max=20)])
    profile_pic = FileField('Profile Picture', validators=[Optional(), FileAllowed(['jpg', 'png'])])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Update!")

    def validate_email(self, email):

        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email Taken.')

    def validate(self):
        if not super(SettingsForm, self).validate():
            return False
        if not self.email.data and not self.fname.data and not self.lname.data and not self.profile_pic:
            msg = 'At least one of the field must be set'
            self.email.errors.append(msg)
            self.fname.errors.append(msg)
            self.lname.errors.append(msg)
            self.profile_pic.errors.append(msg)
            return False
        return True

class RequestResetForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

