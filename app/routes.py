from flask import render_template, flash, redirect, request, url_for, session
from app import app, db
from app.forms import QuestionForm, LoginForm
import app.response as rt
from flask_login import current_user, login_required, login_user
from app.models import User, Post


#list to keep track of the messages
posts = [('chatbot', 'How can I help you today?')]

@app.route('/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			user = User(username=form.username.data)
			chatbot_post = Post(body="What can I do for you?", user_talking="chatbot", author=user)
			db.session.add(user)
			db.session.add(chatbot_post)
			db.session.commit()
		return redirect(url_for('.index', username=form.username.data))
	return render_template('login.html', title='Sign In', form=form)


@app.route('/chatbot/<username>', methods=['GET', 'POST'])
def index(username):
	user = User.query.filter_by(username=username).first()
	form = QuestionForm()
	posts=user.posts.all()
	if form.validate_on_submit():
		user_post = Post(body=form.question.data, user_talking=username, author=user)
		db.session.add(user_post)
		statement = rt.response(form.question.data)
		chatbot_post = Post(body=statement, user_talking="chatbot", author=user)
		db.session.add(chatbot_post)
		db.session.commit()
		return redirect(url_for('.index', username=username))
	return render_template('question.html', form=form, posts=posts)