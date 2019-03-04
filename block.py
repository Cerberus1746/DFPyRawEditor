from collections import OrderedDict

from tags import TagGroup, Tag
from raw_logger import logInfo


class Block(OrderedDict):
	def __init__(self, tag, father, block_level = -1, *args, **kwargs):
		assert isinstance(tag, Tag), "Name is invalid"
		assert isinstance(father, Block), "Block is invalid"

		block_level += 1
		self.block_level = block_level


		self.tags = TagGroup(owner=self)

		self.parent_block = father
		self.tag = tag

		logInfo("block level {}".format(self.block_level, self.tag))

		super().__init__(*args, **kwargs)

	def __str__(self):
		return str(self.tag)

	def __repr__(self):
		return self.__str__()

	def __setitem__(self, key, value):
		assert (isinstance(key, Tag) or issubclass(type(key), Tag)), "Key needs to be a tag"
		assert isinstance(value, Block), "Value needs to be a block"

		return super().__setitem__(key, value)

	@property
	def last_class(self):
		return list(self.keys())[-1]

	@property
	def last_block(self):
		return self[self.last_class]

	def create_block(self, tag:Tag):
		assert (isinstance(tag, Tag) or issubclass(type(tag), Tag)), "Tag needs to be a subclass of tag or a tag"

		created_block = Block(tag, self, self.block_level)
		self[tag] = created_block
		return created_block

	def to_raw(self, auto_join):
		lines = [("\t" * (self.block_level - 1)) + self.tag.to_raw_line(),]

		before_tabs = self.tags.to_raw(False)
		after_tabs = map(lambda x: ("\t" * self.block_level) + x, before_tabs)

		lines.append("\n".join(after_tabs))

		for child_class in self.values():
			lines.append(child_class.to_raw(True))

		if auto_join:
			return "\n".join(lines)

		else:
			return lines

	def add_tag(self, tag):
		self.tags.add(tag)
