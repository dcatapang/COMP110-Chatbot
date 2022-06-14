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


words_asked = []
status = [False]


final_message = 'Have a nice day!'
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


	if finished:
		return final_message
	elif question:
		add_word(split_question[3])
		status[0] = True
		return split_question[2] + " " + split_question[3] + " " + split_question[1] + " " + terms[split_question[3]][0] 
	elif needs_example and get_word_status():
		response_list = terms[get_term()]
		return response_list[1]
	elif needs_second_example and get_word_status():
		response_list = terms[get_term()]
		return response_list[2]
	else:
		return misunderstood

def add_word(term):
	words_asked.append(term)

def get_term():
	return words_asked[-1]

def get_word_status():
	return status[0]



