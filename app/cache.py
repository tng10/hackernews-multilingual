from pymongo import MongoClient # Database connector


class HackerNewsCacheAPI(object):

	client = MongoClient('localhost', 27017)	# Configure the connection to the database
	db = client.fakehackernews	# Select the database
	topstories_collection = db.topstories # Select the collection
	translations_collection = db.translations # Select the collection

	def bulk_persist_topstories(self, topstories):
		return self.db.topstories.insert_many(topstories)

	def persist_story(self, story):
		return self.db.topstories.insert(story)

	def get_topstories(self):
		return self.db.topstories.find()

	def get_story(self, story_id):
		return self.db.topstories.find({"id": story_id})

	def delete_stories(self):
		return self.db.topstories.remove({})

	def delete_story(self, story_id):
		return self.db.topstories.remove({"id": story_id})

	def get_translation(self, story_id, target_lang):
		return self.db.translations.find({"id": story_id, "target_lang": target_lang})

	def persist_translation(self, translation):
		return self.db.translations.insert(translation)

	def delete_translation(self, story_id):
		return self.db.topstories.remove({"id": story_id, "target_lang": target_lang})
