from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

# creating 2 forms

# form to request user to input their email

class EmailForm(Form): 
    email = StringField('Email', validators=[DataRequired(), Email()])

# this is the form the user will get when they click on the password reset link
# user resets password here - only inputs new password in once so only 1 password field for twice add another password field

class PasswordForm(Form):
    password = PasswordField('Email', validators=[DataRequired()])

    