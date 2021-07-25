from flask import Flask, render_template
from surveys import *

app = Flask(__name__)

responses = []

@app.route('/')
def home_view():
    title = satisfaction_survey.title
    instruct = satisfaction_survey.instructions
    return render_template('survey.html', survey_title = title, survey_instruct = instruct)

@app.route('/questions/<int: q_num>')
def question_view():
    pass