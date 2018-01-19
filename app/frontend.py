from flask import Blueprint, render_template, jsonify, request
from hackernews_api import HackerNewsAPI
from unbabel_api import UnbabelAPI
from cache import HackerNewsCacheAPI


hn_api = HackerNewsAPI()
ub_api = UnbabelAPI()

# create frontend blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route("/", methods=['GET'])
def home():
	topstories = hn_api.get_detailed_topstories()
	result = topstories_collection.insert_many(topstories)
	print result
	return render_template('index.html', context={'topstories': topstories})


@frontend.route("/detail/<int:story_id>", methods=['GET'])
def story(story_id):
	story = hn_api.get_story_with_comments(story_id)
	return render_template('detail.html', context=story)


@frontend.route("/api/request-translation", methods=['POST'])
def request_translation():
	data = request.json
	request_translation_response = ub_api.bulk_translate(data['texts'], data['source_lang'], data['target_lang'])
	return jsonify([t.uid for t in request_translation_response])


@frontend.route("/api/request-story-translation/<int:story_id>", methods=['GET'])
def request_story_translation(story_id):
	story = hn_api.get_story_with_comments(story_id)
	texts = [story['story']['title'], [comment['text'] for comment in story['comments']]]
	request_translation_response = ub_api.bulk_translate(texts)
	return jsonify([t.uid for t in request_translation_response])


@frontend.route("/api/get-translations/<request_list>", methods=['GET'])
def get_translations(request_list):
	request_list = map(str, request_list.rstrip(',').split(','))
	translation_response = ub_api.get_translations(request_list)
	return jsonify(translation_response)

