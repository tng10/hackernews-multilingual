from flask import Blueprint, render_template, jsonify, request
from service import HackerNewsService
from hackernews_api import HackerNewsAPI
from unbabel_api import UnbabelAPI

hn_api = HackerNewsAPI()
ub_api = UnbabelAPI()
hn_service = HackerNewsService()

# create frontend blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route("/", methods=['GET'])
def home():
	topstories = hn_service.get_detailed_topstories()
	return render_template('index.html', context={'topstories': topstories})


@frontend.route("/detail/<int:story_id>", methods=['GET'])
def story(story_id):
	story = hn_api.get_story_with_comments(story_id)
	return render_template('detail.html', context=story)


@frontend.route("/api/request-translation", methods=['POST'])
def request_translation():
	data = request.json
	request_translation_response = hn_service.bulk_translate(data['texts'], data['source_lang'], data['target_lang'])
	if not request_translation_response['is_translated']:
		request_translation_response['results'] = [t.uid for t in request_translation_response['results']]
	return jsonify(request_translation_response)


# @frontend.route("/api/request-story-translation/<int:story_id>", methods=['GET'])
# def request_story_translation(story_id):
# 	story = hn_api.get_story_with_comments(story_id)
# 	texts = [story['story']['title'], [comment['text'] for comment in story['comments']]]
# 	request_translation_response = ub_api.bulk_translate(texts)
# 	return jsonify([t.uid for t in request_translation_response])


@frontend.route("/api/get-translations/<request_list>", methods=['GET'])
def get_translations(request_list):
	translation_response = hn_service.get_translations(request_list)
	return jsonify(translation_response)


@frontend.route("/api/cache-translations", methods=['POST'])
def cache_translations():
	data = request.json
	hn_service.cache_translations(data)
	return jsonify({})
