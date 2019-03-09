'''
Module that handles tag blocks (or you can call tag group)

Authors:
	Leandro (Cerberus1746) Benedet Garcia
'''
from collections import OrderedDict

from tags import TagGroup, Tag
from raw_logger import logInfo


class Block(OrderedDict):
	"""
	This basically serves as a group for a special tag.
	For example:
	::
		[CAN_DO_INTERACTION:MATERIAL_EMISSION]
			[CDI:ADV_NAME:Spit]
			[CDI:USAGE_HINT:NEGATIVE_SOCIAL_RESPONSE]
			[CDI:USAGE_HINT:TORMENT]
			[CDI:BP_REQUIRED:BY_CATEGORY:MOUTH]
			[CDI:MATERIAL:LOCAL_CREATURE_MAT:SPIT:LIQUID_GLOB]
			[CDI:VERB:spit:spits:NA]
			[CDI:TARGET:C:LINE_OF_SIGHT]
			[CDI:TARGET_RANGE:C:15]
			[CDI:MAX_TARGET_NUMBER:C:1]
			[CDI:WAIT_PERIOD:30]

	This will start a block with CAN_DO_INTERACTION:MATERIAL_EMISSION tag as index
	and will hold all CDI tags that are after it.

	Args:
		tag (Tag): Tag that will serve as index of the block ([CREATURE:DWARF] for example)
		father (Block): Block that is the parent of the current block
		block_level (int): Is used to determine the tabulation for the current block, this tends to be automatic
	"""
	def __init__(self, tag, father, block_level = -1, *args, **kwargs):
		"""
		Initialize class
		"""

		assert isinstance(tag, Tag), "Name is invalid"
		assert isinstance(father, Block), "Block is invalid"

		block_level += 1
		self.block_level = block_level

		self.tags = TagGroup(owner=self)

		self.parent_block = father
		self.tag = tag

		logInfo("block level {}".format(self.block_level, self.tag))

		tag.block = self

		super().__init__(*args, **kwargs)

	def __str__(self):
		"""
		This function always returns the parsed tag that is the index of this block

		Returns:
			str: The raw representation of the index tag ([CREATURE:DWARF] for example)
		"""
		return str(self.tag)

	def __repr__(self):
		"""
		Same as __str__
		"""
		return self.__str__()

	def __setitem__(self, key, value):
		"""
		Assign a block with a tag as index

		Args:
			key (Tag): Tag or object that inherits Tag
			value (Block): The new block
		"""
		return self.assign_block(key, value)

	@property
	def last_class(self):
		"""
		This property returns the last tag that was used as index of the child of this block

		Returns:
			Tag: Last index added as a child
		"""
		return list(self.keys())[-1]

	@property
	def last_block(self):
		"""
		This property returns the last block that is a child of this block

		Returns:
			Block: Last block added as a child
		"""
		return self[self.last_class]

	def create_block(self, tag):
		"""
		Automatically create a new child block with tag as index

		Args:
			tag (Tag): The tag index
		"""
		assert (isinstance(tag, Tag) or issubclass(type(tag), Tag)), "Tag needs to be a subclass of tag or a tag"

		created_block = Block(tag, self, self.block_level)
		self[tag] = created_block
		return created_block

	def assign_block(self, tag, block):
		"""
		Assign a block with a tag as index

		Args:
			tag (Tag): Tag or object that inherits Tag
			block (Block): The new block

		Returns:
			Block: The created block
		"""
		assert (isinstance(tag, Tag) or issubclass(type(tag), Tag)), "Key needs to be a tag"
		assert isinstance(block, Block), "Value needs to be a block"

		return super().__setitem__(tag, block)

	def to_raw(self, auto_join):
		"""
		Function used to convert all the child blocks and the tags in this block to Dwarf Fortress raws

		Args:
			auto_join (bool): If true, will return a string with the parsed tags separated by a line break,
			if False, will return a list of parsed tags

		Returns:
			list or str: returns string if auto_join is true and list if it's False
		"""

		lines = [("\t" * (self.block_level - 1)) + self.tag.to_raw_line(),]

		before_tabs = self.tags.to_raw(False)
		if len(before_tabs) > 0:
			after_tabs = map(lambda x: ("\t" * self.block_level) + x, before_tabs)

			lines.append("\n".join(after_tabs))

		for child_class in self.values():
			lines.append(child_class.to_raw(True))

		if auto_join:
			return "\n".join(lines)

		else:
			return lines

	def to_dict(self, add_name = True):
		"""
		Psst, psst, this isn't currently working, so look away for a bit. Yeah, that way,

		Todo:
			* Find a good pattern to organize the dictionaries
		"""

		inner_dict = {}

		for current_tag in self.tags:
			tag_name = current_tag.tag_name
			tag_args = current_tag.tag_args

			if tag_args:
				if tag_name not in inner_dict: inner_dict[tag_name] = []
				inner_dict[tag_name].append(":".join(tag_args))
			else:
				if "tags" not in inner_dict: inner_dict["tags"] = []
				inner_dict["tags"].append(tag_name)

		for tag_key, current_parent in self.items():
			tag_name = tag_key.tag_name
			tag_args = tag_key.tag_args
			if tag_name not in inner_dict:
				inner_dict[tag_name] = []

			inner_dict[tag_name].append([":".join(tag_args), current_parent.to_dict(False)])


		if add_name:
			return {
				self.tag.tag_name: [":".join(self.tag.tag_args), inner_dict]
			}
		else:
			return inner_dict


	def add_tag(self, tag):
		"""
		Function used to add tags to current block

		Args:
			tag (Tag): tag to be added
		"""
		self.tags.add(tag)
