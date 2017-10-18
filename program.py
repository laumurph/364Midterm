from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import Required, NumberRange

import requests
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'awfhufiwIOAfHUFjA2RF3E122RXQafwf843Rafw'

#404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# 500 error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')

class FirstClickbait(FlaskForm):
	username = StringField("Create a username for yourself: ", validators=[Required()])
	choice = RadioField("Pick one of the following: ", choices=[("static/paloma", "Cookies"),("static/choco", "Chocolate"),("static/gir", "Carrots")], validators=[Required()])
	send = SubmitField("See Results")

class SecondClickbait(FlaskForm):
	number = IntegerField("What's your favorite number? Enter here: ", validators=[Required(), NumberRange()])
	choice = RadioField("Pick one of the following: ", choices=[("static/water", "Option"),("static/sunset", "Sec"),("static/moon", "Reap"), ("random", "I don't care, give me a random word")], validators=[Required()])
	send = SubmitField("See Results")

@app.route('/')
def index():
	return render_template("index.html")

@app.route("/first-question")
def first_question():
	qForm = FirstClickbait()
	return render_template('first-form.html', form=qForm)

@app.route("/results-first", methods = ['GET', "POST"])
def results_first():
	fForm = FirstClickbait(request.form)
	if request.method == 'POST' and fForm.validate_on_submit():
		username = fForm.username.data
		choice = fForm.choice.data
		return render_template("response.html", data = ("First Form", username, choice)) 
	flash('All fields are required!')
	return redirect(url_for('first_question'))

@app.route("/second-question")
def second_question():
	qForm = SecondClickbait()
	return render_template('second-form.html', form=qForm)

@app.route("/results-second", methods = ['GET', "POST"])
def results_second():
	sForm = SecondClickbait(request.form)
	if request.method == 'POST' and sForm.validate_on_submit():
		number = sForm.number.data
		choice = sForm.choice.data
		if choice == "random":
			lst = ["static/water", "static/sunset", "static/moon"]
			pos = random.randint(0,2)
			choice = lst[pos]
		return render_template("response.html", data = ("Second Form", number, choice)) 
	flash('All fields are required!')
	return redirect(url_for('second_question'))

# @app.route("/third-question")
# def third_question():
# 	pass

