from flask import Blueprint, render_template
from hackernews_api import HackerNewsAPI


# create frontend blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route("/")
def home():
	hn_api = HackerNewsAPI()
	topstories = hn_api.get_detailed_topstories()
	return render_template('index.html', context={'topstories': topstories})


@frontend.route("/detail/<int:story_id>")
def story(story_id):
	hn_api = HackerNewsAPI()
	story = hn_api.get_story_with_comments(story_id)
	return render_template('detail.html', context=story)
