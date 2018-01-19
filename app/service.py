from hackernews_api import HackerNewsAPI
from unbabel_api import UnbabelAPI
from cache import HackerNewsCacheAPI


class HackerNewsService(object):
	
	cache = HackerNewsCacheAPI()
	hn_api = HackerNewsAPI()
	ub_api = UnbabelAPI()

	def get_detailed_topstories(self):
		topstories = list(self.cache.get_topstories())
		if not topstories:
			topstories = self.hn_api.get_detailed_topstories()
			self.cache.bulk_persist_topstories(topstories)
		else:
			print 'Getting cached topstories'
		return topstories

	def bulk_translate(self, texts, source_lang, target_lang):
		query_cursor = self.cache.get_translations(texts=texts, target_lang=target_lang)
		translations_or_requests = list(query_cursor)
		is_translated = True
		if not (translations_or_requests):
			translations_or_requests = self.ub_api.bulk_translate(texts, source_lang, target_lang)
			is_translated = False
		else:
			print 'Getting cached translations'
		return {'is_translated': is_translated, 'results': list(translations_or_requests)}

	def get_translations(self, request_list):
		request_list = map(str, request_list.rstrip(',').split(','))
		translation_response = self.ub_api.get_translations(request_list)
		return translation_response

	def cache_translations(self, translations):
		self.cache.bulk_persist_translations(translations)

