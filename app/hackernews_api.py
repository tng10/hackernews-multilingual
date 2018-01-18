import requests
import grequests
import itertools


def topstories_with_comments_exception_handler(request, exception):
	print 'Request failed'


class HackerNewsAPI(object):
	BASE_URL = "https://hacker-news.firebaseio.com/v0/"
	TOPSTORIES_ENDPOINT = 'topstories.json'
	ITEM_ENDPOINT = 'item/{0}.json'
	MAX_TOP_STORIES = 10
	MAX_STORY_COMMENTS = 3

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

		# get topstories (ids) and build their urls
		topstories = self.get_topstories()
		story_urls = [self.build_url(self.ITEM_ENDPOINT.format(pk)) for pk in topstories[:self.MAX_TOP_STORIES]]

		# prepare the async story requests
		set_of_story_requests = (grequests.get(u) for u in story_urls)

		# fetch them all!
		full_stories = grequests.map(set_of_story_requests, exception_handler=topstories_with_comments_exception_handler)

		# variable to hold comments per story
		comments = {}
		full_stories_data = []
		
		# sanity check for http 200 ok responses
		if all(map(lambda x: True if x.status_code == 200 else False, full_stories)):
			for story in full_stories:
				story_data = story.json()
				story_data['comments'] = []

				full_stories_data.append(story_data)
				comments[story_data['id']] = story_data.get('kids')[:self.MAX_STORY_COMMENTS] if 'kids' in story_data else []
		else:
			print "Oops, something went wrong! Stories could not be loaded."
			return []

		# all comments
		all_comments = list(set(itertools.chain.from_iterable(comments.values())))

		# comment urls
		comment_urls = [self.build_url(self.ITEM_ENDPOINT.format(pk)) for pk in all_comments]

		# prepare the async comment requests
		set_of_comment_requests = (grequests.get(u) for u in comment_urls)

		# fetch them all!
		full_comments = grequests.map(set_of_comment_requests, exception_handler=topstories_with_comments_exception_handler)

		if all(map(lambda x: True if x.status_code == 200 else False, full_comments)):
			for story_data in full_stories_data:
				for comment in full_comments:
					comment_data = comment.json()
					if comment_data['parent'] == story_data['id']:
						story_data['comments'].append(comment_data)

		return full_stories_data
