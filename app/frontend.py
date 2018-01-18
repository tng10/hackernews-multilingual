from flask import Blueprint, render_template
from hackernews_api import HackerNewsAPI


# create frontend blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route("/")
def home():
	return render_template('index.html')


@frontend.route("/fullstories")
def fullstories():
	hn_api = HackerNewsAPI()
	topstories = hn_api.get_topstories_with_comments()
	return render_template('index.html', context={'topstories': topstories})
