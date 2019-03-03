from collections import OrderedDict

from tags import TagGroup, Tag


class Block(OrderedDict):
	def __init__(self, *args, **kwargs):
		self.tags = TagGroup(owner=self)
		self.parents = False

		self.parent_block = kwargs.get("father", False)
		self.name = kwargs.get("name", False)

		if self.name:
			del(kwargs["name"])

		if self.parent_block:
			del(kwargs["father"])

		assert(isinstance(self.name, Tag), "Name is invalid")

		super().__init__(*args, **kwargs)

	def __str__(self):
		return str(self.name)

	def __repr__(self):
		return self.__str__()

	@property
	def last_class(self):
		return list(self.keys())[-1]

	@property
	def last_block(self):
		return self[self.last_class]

	def create_block(self, tag:Tag):
		assert(isinstance(self.name, Tag), "Name is invalid")
		created_block = Block(father=self, name=tag)
		self[tag] = created_block
		return created_block

	def add_tag(self, tag):
		self.tags.add(tag)