'''
Module that handles tags

Authors:
	Leandro (Cerberus1746) Benedet Garcia
'''

from collections.abc import Iterable

from raw_logger import logDebug

class TagIndex(list):
	"""
	This class is a singleton, meaning that anything that tries to instantiate this class,
	will actually use the same instance as anything that instantiated it.

	This class is used to keep all the tags created by the parser. Inside, deep inside, in his hearth,
	is just a list object but with extra things. I did this so I don't need to set iters and stuff manually

	Attributes:
		_instance (TagIndex): Is the var that holds the unique instance

	Todo:
		* Create get_parent function
	"""
	_instance = None

	def __new__(cls, *args, **kwargs):
		"""
		This is what makes sure there's only one instance of this class

		Returns:
			TagIndex: return the instance before it goes to __init__, if the instance don't exist, it creates if not,
			it uses the instance already made
		"""
		if cls._instance is None:
			cls._instance = super().__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self, *args, **kwargs):
		pass

	def add_tag(self, tag):
		assert Tag.is_valid_tag_obj(tag), "Tag needs to be a subclass of tag or a tag"
		self.append(tag)

	def get_tags(self, tag_name, tag_args=False):
		"""
		This function is the father of all functions that search for a tag.

		The search can be made by supplying a DF tag, the tag name with a list of args
		or a Tag object

		Examples:
			Let's say that we created the tags [CREATURE:DWARF] and a couple others with
			literal blocks::
				from tags import Tag

				Tag("[CREATURE:DWARF]")
				Tag("[CREATURE:GOBLIN]")
				Tag("[INTERACTION:RAISE_CORPSE]")
				Tag("[INTELLIGENT]")

			We can now get all tags that are creatures with:
			literal blocks::
				Tag.tag_index.get_tags("creature")

			It will return the tags [CREATURE:DWARF] and [CREATURE:GOBLIN] inside a generator, which
			you can iter over with or convert into a list for example. If you want to just get the dwarf
			you can have some options:
			literal block::
				#via a normal tag
				Tag.tag_index.get_tags("[CREATURE:DWARF]")

				#using a tag object
				#IMPORTANT: if you create two times the tag, it will return TWO dwarf tags,
				#because the indexes indexes everything, so be careful
				dwarf_tag = Tag("[CREATURE:DWARF]")
				Tag.tag_index.get_tags(dwarf_tag)

				#with a list of args
				Tag.tag_index.get_tags("creature", ["goblin",])

		Args:
			tag_name (string or Tag): Tag to search for, can be a Tag obj or a DF raw tag.
			tag_args (Iter, bool): iter of args, if default false, it will lookup just for tag names and not compare args unless  set in a tag object in tag_args argument.

		Yields:
			returns a generator with the tags that matches the query
		"""
		if type(tag_name) == str:
			tag_name = tag_name.lower()

		if Tag.is_valid_tag(tag_name):
			tag_name, tag_args = Tag.extract_info(tag_name)

		elif Tag.is_valid_tag_obj(tag_name):
			tag_name = tag_name.tag_name
			tag_args = tag_name.tag_args

		print(self)

		for current_tag in self:
			if tag_args and len(tag_args) > 0:
				if current_tag.tag_name == tag_name and current_tag.tag_args == tag_args:
					yield current_tag
			else:
				if current_tag.tag_name == tag_name:
					yield current_tag

	def get_blocks(self, tag_name, tag_args=False):
		all_tags = self.get_tags(tag_name, tag_args)
		if not all_tags:
			return False
		else:
			return [current_tag.block for current_tag in all_tags if current_tag.block]

class Tag(object):
	def __init__(self, tag_name="", tag_args=False, owner_class=None):
		assert type(tag_name) == str, "tag_name has to be a str"
		assert isinstance(tag_args, Iterable) and type(tag_args) != str or not tag_args, "tag_args has to be a iter"

		self.tag_index = TagIndex()

		if Tag.is_valid_tag(tag_name):
			self.tag_name, self.tag_args = self.extract_info(tag_name)
		else:
			self.tag_name = tag_name
			self.tag_args = tag_args

		self.prefix = self.tag_name.split("_")[0]
		self.owner = owner_class
		self.need_prefix = False
		self.parents = False
		self.block = False

		self.tag_args = self.tag_args if type(self.tag_args) == list or not tag_args else list(self.tag_args)

		self.tag_index.add_tag(self)

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def __lt__(self, other):
		return str(self) < str(other)

	def __gt__(self, other):
		return str(self) > str(other)

	def __hash__(self):
		if self.tag_args:
			return hash(self.tag_name + str(self.tag_args))
		else:
			return hash(self.tag_name)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return self.to_raw_line()

	@staticmethod
	def extract_info(raw_line):
		raw_line = raw_line.replace("[", "")
		raw_line = raw_line.replace("]", "")
		raw_line = raw_line.split(":")
		return raw_line[0], raw_line[1:]

	@classmethod
	def parse(cls, raw_line):
		return cls(*Tag.extract_info(raw_line))

	@staticmethod
	def is_valid_tag_obj(tag):
		return isinstance(tag, Tag) or type(tag) == Tag

	@staticmethod
	def is_valid_tag(tag):
		return "[" in tag and "]" in tag

	def to_raw_line(self):
		if self.tag_args:
			raw_line = ":".join([self.tag_name, *self.tag_args])
		else:
			raw_line = self.tag_name
		return "[" + raw_line + "]"

class TagGroup(set):
	def __init__(self, owner=None):
		self.owner = owner

	def __str__(self):
		return str(self._group)

	def add(self, tag):
		logDebug("Created tag {0} into <a href='#{1}'>{1}</a>".format(tag, self.owner))
		if Tag.is_valid_tag_obj:
			Tag.owner = self.owner
			super().add(tag)
		else:
			super().add(Tag.parse(tag, owner=self.owner))

	def to_raw(self, auto_join):
		lines = list(self)
		sorted_tags = sorted(lines, key=lambda x: (str(x)[:25] not in ['[select_additional_caste:',], x))

		lines = [tag.to_raw_line() for tag in sorted_tags]

		if auto_join:
			return "\n".join(lines)

		else:
			return lines


if __name__ == "__main__":
	creature_draco = Tag("[CREATURE:DRACO]")
	Tag("another", ["test",])
	Tag("lol")
	Tag("[lol:you are ded]")
	print(list(TagIndex().get_blocks("lol")))