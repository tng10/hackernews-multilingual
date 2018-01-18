import requests
import grequests
from unbabel.api import UnbabelApi


def get_translations_exception_handler(request, exception):
	print 'Response failed'


class UnbabelAPI(object):
	USERNAME = 'fullstack-challenge'
	API_KEY = "9db71b322d43a6ac0f681784ebdcc6409bb83359"
	GET_TRANSLATION_ENDPOINT = 'translation/{0}'

	def __init__(self, *args, **kwargs):
		self.api = UnbabelApi(username=self.USERNAME, api_key=self.API_KEY, sandbox=True)

	def build_url(self, endpoint=''):
		return '%s%s' % (self.api.api_url, endpoint)

	def bulk_translate(self, texts, source_lang="en", target_lang="pt"):
		translations = []
		for t in texts:
			translations.append({
			    "text": t,
			    "source_language": source_lang,
			    "target_language": target_lang
			})

		return self.api.post_bulk_translations(translations)

	def translate(self, text, source_lang="en", target_lang="pt"):
		return self.api.post_translations(text, source_lang, target_lang)

	def get_translations(self, request_list):

		# comment urls
		translation_urls = [self.build_url(self.GET_TRANSLATION_ENDPOINT.format(pk)) for pk in request_list]
		print translation_urls
		# prepare the async translation requests
		set_of_translation_requests = (grequests.get(u, headers=self.api.headers) for u in translation_urls)

		# fetch them all!
		full_translations = grequests.map(set_of_translation_requests, exception_handler=get_translations_exception_handler)
		
		full_translations_data = []
		if all(map(lambda x: True if x.status_code == 200 else False, full_translations)):
			full_translations_data = [t.json() for t in full_translations if t is not None and t.json()['status'] == 'completed']
		return full_translations_data
