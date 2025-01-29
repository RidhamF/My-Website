from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Email


class Register(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class Login(FlaskForm):
    email = StringField("Email or Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Sign in")

