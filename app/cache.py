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
		return self.db.topstories.find({}, self.get_default_opt_kwargs())

	def get_story(self, story_id):
		return self.db.topstories.find_one({"id": story_id}, self.get_default_opt_kwargs())

	def delete_stories(self):
		return self.db.topstories.remove({})

	def delete_story(self, story_id):
		return self.db.topstories.remove({"id": story_id})

	def get_translation(self, request_translation_id, target_lang):
		return self.db.translations.find_one({"uid": request_translation_id, "target_language": target_lang}, self.get_default_opt_kwargs())

	def get_translations(self, texts, target_lang):
		return self.db.translations.find({"target_language": target_lang, "text": {"$in": list(texts)} }, self.get_default_opt_kwargs())

	def bulk_persist_translations(self, translations):
		return self.db.translations.insert_many(translations)

	def persist_translation(self, translation):
		return self.db.translations.insert(translation)

	def delete_translation(self, request_translation_id):
		return self.db.topstories.remove({"uid": request_translation_id, "target_language": target_lang})

	def get_default_opt_kwargs(self):
		return {'_id': 0}
