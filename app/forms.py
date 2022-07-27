from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    question = StringField(validators=[DataRequired()], render_kw={'autofocus': True, 'placeholder': "What is your question?"})
    submit = SubmitField('Send!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
