from flask import render_template, flash, redirect, request
from app import app
from app.forms import QuestionForm


#make constants for whether the response is the definition, example 1, example 2, or ending (state machine)
#keep track of whatever word is being asked

terms = {}
rdfile = open("dictionary.txt", "r")
for line in rdfile:
	term = line.strip()
	definition = rdfile.readline().strip()
	first_example = rdfile.readline().strip()
	second_example = rdfile.readline().strip()
	terms[term] = [definition, first_example, second_example]



finished = 'Have a nice day!'
misunderstood = 'Sorry, I do not understand your question.'
global current_term
current_term = ""

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
		statement = response(form.question.data)
		posts.append(statement)
		return redirect('/')
	return render_template('question.html', posts=posts, form=form)


def response(question):

#use exception handling to help!
	split_question = question.split()
	full_question = question.lower()

	try:
		question = split_question[0].lower() == "what" and split_question[1].lower() == "is" and (split_question[2].lower() == "a" or split_question[2].lower() == "an") and split_question[3].lower() in terms
	except IndexError:
		return misunderstood

	needs_example = full_question == "i don't understand" or full_question == "can you give me an example?"
	needs_second_example = full_question == "i still don't understand" or "can you give me another example?"
	finished = full_question == "thanks!"
	word_given = current_term != ""


	if question:
		current_term = split_question[3]
		return split_question[2] + " " + split_question[3] + " " + split_question[1] + " " + terms[current_term][0] 
	elif needs_example and word_given:
		response_list = terms[current_term]
		return response_list[1]
	elif needs_second_example and word_given:
		response_list = terms[current_term]
		return response_list[2]
	elif finished:
		response_list = terms[current_term]
		return response_list[3]
	else:
		return misunderstood






