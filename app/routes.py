from flask import render_template, flash, redirect, request, url_for, session
from app import app, db
from app.forms import QuestionForm, LoginForm, RegistrationForm, DictionaryForm, HowToForm
import app.response as rt
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, Post, Terms, UnknownTerms, UnknownHowQuestions, HowTo, UnknownQuestions
from werkzeug.urls import url_parse

#list to keep track of the messages
posts = [('chatbot', 'How can I help you today?')]

rfile = open("dictionary.txt", "r")
for line in rfile:
    term = line.strip()
    definition = rfile.readline().strip()
    example = rfile.readline().strip()

    term_info = Terms(term=term, definition=definition, example=example)
    db.session.add(term_info)

db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		try:
			if (user is None) or (not user.check_password(form.password.data)): 
				flash('Invalid username or password. Please try again.')
				return redirect(url_for('login'))
		except AttributeError:
			flash('Invalid username or password. Please try again.')
			return redirect(url_for('login'))
		
		if user.prof_status():
			print("Hello professor!")
			return redirect(url_for('professorhome'))
			
		login_user(user)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index', username=form.username.data)
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@login_required
@app.route('/chatbot/<username>', methods=['GET', 'POST'])
def index(username):
	user = User.query.filter_by(username=username).first()
	form = QuestionForm()
	posts=user.posts.all()
	if form.validate_on_submit():
		user_post = Post(body=form.question.data, user_talking=username, author=user)
		db.session.add(user_post)
		if user.get_response_status():
			if form.question.data == "Y":
				chatbot_post = Post(body="Sounds good!", user_talking="chatbot", author=user)
				user.follow_false()
			elif form.question.data == "N":
				chatbot_post = Post(body="What other questions do you have?", user_talking="chatbot", author=user)
				user.follow_false()
			else:
				chatbot_post = Post(body="Please type Y or N", user_talking="chatbot", author=user)
			db.session.add(chatbot_post)
		else:
			statement, answer_given = rt.response(form.question.data)
			chatbot_post = Post(body=statement, user_talking="chatbot", author=user)
			db.session.add(chatbot_post)
			if answer_given == "True":
				chatbot_follow = Post(body="Was this what you were looking for? (Type Y or N)", user_talking="chatbot", author=user)
				user.follow_true()
				db.session.add(chatbot_follow)
			elif answer_given == "False":
				chatbot_follow = Post(body="Here is the link to your textbbok: 'https://runestone.academy/ns/books/published/pythonds/index.html'", user_talking="chatbot", author=user)
				db.session.add(chatbot_follow)
		db.session.commit()
		return redirect(url_for('.index', username=username))
	return render_template('question.html', form=form, posts=posts)

@login_required
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		if form.professor_status.data == True:
			if form.professor_invite_code.data != "A1B2C3D4":
				flash('Invalid invite code. Please try again.')
				return redirect(url_for('register'))
		user = User(username=form.username.data, email=form.email.data, follow_up=False, professor_status=form.professor_status.data)
		user.set_password(form.password.data)
		db.session.add(user)
		if form.professor_status.data == False:
			chatbot_post = Post(body="What can I do for you?", user_talking="chatbot", author=user)
			db.session.add(chatbot_post)

		db.session.commit()
		flash('Congratulations! You are now registered!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@login_required
@app.route('/professorhome', methods=['GET', 'POST'])
def professorhome():
	return render_template('profhome.html', title='Pytheybuddy Admin Home')

@login_required
@app.route('/terms', methods=['GET', 'POST'])
def add_terms():
	form = DictionaryForm()
	unknown_terms = UnknownTerms.query.all()
	if form.validate_on_submit():
		#delete from unknown term db
		term = Terms(term=form.term.data, definition=form.definition.data, example=form.example.data)
		db.session.add(term)
		db.session.commit()
		return redirect(url_for('add_terms'))
	return render_template('addterms.html', title='Add Terms to PytheyBuddy', form=form, terms=unknown_terms)

@login_required
@app.route('/dates', methods=['GET', 'POST'])
def add_dates():
	return render_template('adddates.html', title='Add Dates to PytheyBuddy')

@login_required
@app.route('/howto', methods=['GET', 'POST'])
def add_how_to():
	form = HowToForm()
	unknown_questions = UnknownHowQuestions.query.all()
	if form.validate_on_submit():
		#delete from unknown term db
		question = HowTo(verb=form.verb.data, term=form.term.data, instruction=form.instruction.data)
		db.session.add(question)
		db.session.commit()
		return redirect(url_for('add_how_to'))
	return render_template('addhowto.html', title='Add Instructions to PytheyBuddy', form=form, questions=unknown_questions)

@login_required
@app.route('/unknownquestions', methods=['GET', 'POST'])
def view_questions():
	unknown_questions = UnknownQuestions.query.all()
	return render_template('unknownquestions.html', title='Questions Unanswered', questions=unknown_questions)

@login_required
@app.route('/studentsmessages', methods=['GET', 'POST'])
def view_messages():
	users = User.query.filter_by(professor_status=False).all()
	return render_template('viewmessages.html', users=users)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))