from flask import render_template, flash, redirect, request
from app import app
from app.forms import QuestionForm

posts = ['How can I help you today?']

terms = {'integer': {'def': 'a whole number value.', 'ex': ['42', '-7']}, 'algorithm': {'def': 'a step by step list of instructions that will solve a problem if executed', 'ex': ['ex1', 'ex2']}}

understood = 'Is there anything else I can do for you today?'
misunderstood = 'Sorry, I do not understand your question.'	

#make constants for whether the response is the definition, example 1, example 2, or ending (state machine)
#keep track of whatever word is being asked


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
		statement = response(form.question.data)
		posts.append(statement)
		return redirect('/')
	return render_template('question.html', posts=posts, form=form)


def response(question):

#use exception handling to help!
	split_question = question.split()

	try:
		first_word = split_question[0].lower() == "what"
		second_word = split_question[1].lower() == "is"
		third_word = split_question[2].lower() == "a" or split_question[2].lower() == "an"
		fourth_word = split_question[3].lower() in terms
		
	except IndexError:
		return misunderstood


	if first_word and second_word and third_word and fourth_word:
		return "Sentence is in correct format!"
	else:
		return misunderstood






