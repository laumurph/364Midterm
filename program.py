from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import Required, NumberRange

import requests
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'awfhufiwIOAfHUFjA2RF3E122RXQafwf843Rafw'

#global variables
doggo_photos = ["static/paloma", "static/choco", "static/gir"]
aesthetic_photos = ["static/water", "static/sunset", "static/moon"]
travel_photos = ["static/south_haven", "static/midland", "static/pittsburgh"]

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
	choice = RadioField("Pick one of the following: ", choices=[(doggo_photos[0], "Cookies"),(doggo_photos[1], "Chocolate"),(doggo_photos[2], "Carrots")], validators=[Required()])
	send = SubmitField("See Results")

class SecondClickbait(FlaskForm):
	number = IntegerField("What's your favorite number? Enter here: ", validators=[Required(), NumberRange()])
	choice = RadioField("Pick one of the following: ", choices=[(aesthetic_photos[0], "Option"),(aesthetic_photos[1], "Sec"),(aesthetic_photos[2], "Reap"), ("random", "I don't care, give me a random word")], validators=[Required()])
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
			pos = random.randint(0,2)
			choice = aesthetic_photos[pos]
		return render_template("response.html", data = ("Second Form", number, choice)) 
	flash('All fields are required!')
	return redirect(url_for('second_question'))

@app.route("/full-images")
def full_images():
	answer = request.args.get("response")
	if answer == "No":
		return render_template("index.html")
	answer_lst = answer.split(',')
	if answer_lst[1] == "First Form":
		new_photos = doggo_photos
		new_photos.remove(answer_lst[2])
	else:
		new_photos = aesthetic_photos
		new_photos.remove(answer_lst[2])


	return render_template('other_photos.html', resp = new_photos)

@app.route("/third-question")
def third_question():
	return render_template("third_form.html")


@app.route("/results-third")
def results_third():
	option = int(request.args.get("destination"))
	return render_template("results_third.html", photo_data=(travel_photos[option], travel_photos[option].split("/")[1].replace("_"," ").title()))

@app.route("/cookie-monster")
def cookie_setter():
	response = make_response("<p>Here's the cookie monster! Here's a secret gift! <a href='http://localhost:5000/'>Home</a></p>")
	response.set_cookie('monster', 'here')
	return response
