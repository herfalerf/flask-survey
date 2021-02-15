from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "password"

debug = DebugToolbarExtension(app)


RESPONSES_KEY = "responses"

@app.route('/')
def index():
    """Return to homepage"""
    return render_template('home.html')

@app.route('/survey1')
def customer_survey():
    """Go to customer service survey page"""
    title = survey.title
    instructions = survey.instructions

    return render_template('survey-1.html', title=title, instructions=instructions)

@app.route('/start', methods=["POST"])
def start_survey():
    """Clear responses and go to first question"""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def next_question():
    """Save response data and redirect to next question"""

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:id>')
def show_question(id):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/survey1")

    if(len(responses) == len(survey.questions)):
        return redirect("/complete")

    if(len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[id]
    return render_template("question.html", question_num=id, question=question)

@app.route('/complete')
def complete():
    """Go to completion page"""

    return render_template('complete.html')