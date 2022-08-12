from transformers import DebertaForTokenClassification
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    follow_up = db.Column(db.Boolean)
    professor_status = db.Column(db.Boolean)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    
    def follow_true(self):
        self.follow_up = True

    def follow_false(self):
        self.follow_up = False

    def get_response_status(self):
        return self.follow_up

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def prof_status(self):
        return self.professor_status

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    user_talking = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #add timestamp

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Terms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(140))
    definition = db.Column(db.String(250))
    example = db.Column(db.String(250))

    def get_definition(self):
        return self.definition

    def get_example(self):
        return self.example

class HowTo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    instruction = db.Column(db.String(250))

    def get_question(self):
        return self.term

    def get_instruction(self):
        return self.instruction
    
class UnknownTerms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(140))

    def get_term(self):
        return self.term

class UnknownHowQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(250))

    def get_question(self):
        return self.question

class UnknownQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(250))

    def get_question(self):
        return self.question
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

db.create_all()