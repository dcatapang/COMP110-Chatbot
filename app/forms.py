from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class QuestionForm(FlaskForm):
    question = StringField(validators=[DataRequired()], render_kw={'autofocus': True, 'placeholder': "What is your question?"})
    submit = SubmitField('Send!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In!')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    professor_status = BooleanField("I am a professor.")
    professor_invite_code = StringField('INVITE CODE')
    terms_and_conditions = BooleanField("terms and conditions", validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already in use.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already in use.')


class DictionaryForm(FlaskForm):
    term = StringField('Term', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    example = StringField('Example', validators=[DataRequired()])
    submit = SubmitField("Add definition")

class HowToForm(FlaskForm):
    question = StringField('How To Questions', validators=[DataRequired()])
    instruction = StringField('Instruction', validators=[DataRequired()])
    submit = SubmitField("Add definition")