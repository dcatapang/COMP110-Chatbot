from flask import render_template, flash, redirect, request
from app import app
from app.forms import QuestionForm
import app.response as rt


#list to keep track of the messages
posts = ['How can I help you today?']

@app.route('/')
def home():
	#create the form
	form = QuestionForm()
	return render_template('question.html', posts=posts, form=form)


@app.route('/chatbot', methods=['GET', 'POST'])
def index():
	form = QuestionForm()
	if form.validate_on_submit():
		posts.append(form.question.data)
		statement = rt.response(form.question.data)
		posts.append(statement)
		return redirect('/')
	return render_template('question.html', posts=posts, form=form)




