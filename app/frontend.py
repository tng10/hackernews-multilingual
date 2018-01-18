from flask import Blueprint, render_template, jsonify
from hackernews_api import HackerNewsAPI
from unbabel_api import UnbabelAPI

hn_api = HackerNewsAPI()
ub_api = UnbabelAPI()

# create frontend blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route("/")
def home():
	topstories = hn_api.get_detailed_topstories()
	return render_template('index.html', context={'topstories': topstories})


@frontend.route("/detail/<int:story_id>")
def story(story_id):
	story = hn_api.get_story_with_comments(story_id)
	return render_template('detail.html', context=story)


@frontend.route("/request-story-translation/<int:story_id>")
def request_translation(story_id):
	story = hn_api.get_story_with_comments(story_id)
	texts = [story['story']['title'], [comment['text'] for comment in story['comments']]]
	request_translation_response = ub_api.bulk_translate(texts)
	return jsonify([t.uid for t in request_translation_response])


@frontend.route("/get-translation/<request_list>")
def get_translations(request_list):
	request_list = map(str, request_list.rstrip(',').split(','))
	translation_response = ub_api.get_translations(request_list)
	return jsonify(translation_response)

