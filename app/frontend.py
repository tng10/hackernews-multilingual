from flask import Blueprint, render_template


# create frontend blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route("/")
def home():
	return render_template('index.html')
