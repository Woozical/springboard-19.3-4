from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.wrappers import response
from surveys import *

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'lofthousesugarcookies'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = {}
active_survey = satisfaction_survey

@app.route('/')
def home_view():
    title = active_survey.title
    instruct = active_survey.instructions
    return render_template('survey.html', survey_title = title, survey_instruct = instruct)

@app.route('/questions/<int:num>')
def question_view(num):
    # Redirect if user manually enters url to try and jump questions
    if num > len(responses):
        endpoint = get_redirect(num)
        return redirect(endpoint)
    
    question = active_survey.questions[num]
    return render_template('question.html', question=question, num=num)

@app.route('/answer', methods=['POST'])
def answer_response():
    q_num = int(request.form['question'])
    a_num = int(request.form['answer'])
    question = active_survey.questions[q_num]
    answer = question.choices[a_num]
    responses[question.question] = answer
    if q_num + 1 == len(active_survey.questions):
        return redirect("/results")
    else:
        return redirect(f"/questions/{q_num + 1}")

@app.route('/results')
def results_view():
    if len(responses) != len(active_survey.questions):
        endpoint = get_redirect()
        return redirect(endpoint)
    else:
        return render_template('results.html', title=active_survey.title, results=responses)


def get_redirect(num=None):
    """Given an attempted jump to a specific question or the end results, return the page
    that the user should be redirected to.
    
    If unfinished with survey:
    Tries to skip ahead questions
    Tries to go out of bounds
    >
    Return to currently unanswered question

    If finished with survey:
    User can jump to any question in-bounds to amend their answer
    Trying to go out of bounds will redirect to survey results
    """

    num_of_qs = len(active_survey.questions)
    num_of_as = len(responses)

    finished = num_of_as == num_of_qs

    if not finished:
        if not num:
            flash("Please complete the survey first!")
            current_q = num_of_as
            return f"/questions/{current_q}"
        elif num > num_of_qs:
            flash("That is not a valid question.")
            current_q = num_of_as
            return f"/questions/{current_q}"
        elif num > num_of_as:
            flash("Please complete the survey in order.")
            current_q = num_of_as
            return f"/questions/{current_q}"

    else:
        if num > num_of_qs:
            flash("That is not a valid question.")
            return "/results"