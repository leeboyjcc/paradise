class Lab(object):
	"""docstring for Lab"""
	def __init__(self, name, tags=None):
		self.name = name

		if tags is None:
			tags = []
		self._tags = tags

	def insert_tag(self, tag):
		if tag not in self._tags:
			self._tags.append(tag)

	@property
	def tags(self):
		return self._tags[:]

	def can_be_started(self, user):
		if user.is_authenticated and user.is_member:
			return True
		else:
			return False
	
		