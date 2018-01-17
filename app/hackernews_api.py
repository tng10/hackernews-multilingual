import requests


class HackerNewsAPI(object):
	BASE_URL = "https://hacker-news.firebaseio.com/v0/"
	TOPSTORIES_ENDPOINT = 'topstories.json'
	ITEM_ENDPOINT = 'item/{0}.json'

	def __init__(self, *args, **kwargs):
		pass

	def build_url(self, endpoint=''):
		return '%s%s' % (self.BASE_URL, endpoint)

	def get_topstories(self):
		"""
		Get a list of top stories: [16169236,16169649,16167594, ...]
		"""
		response = requests.get(self.build_url(self.TOPSTORIES_ENDPOINT))
		return response.json()

	def get_item(self, pk):
		"""
		Get an item: it can be expressed in different types (e.g. Story, Comment, Poll, ...)
		"""
		response = requests.get(self.build_url(self.ITEM_ENDPOINT.format(pk)))
		return response.json()

	def get_topstories_with_comments(self):
		"""
		They don't have an endpoint resource that can do this all at once.
		Therefore we need to iterate over these endpoints and put it altogether
		"""
		topstories = self.get_topstories()
		
