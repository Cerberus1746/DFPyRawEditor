import os, re, types

from class_types.creature_classes import Creature, Caste, Attack, CanDoInteraction, CasteGroup
from class_types.interaction_classes import Interaction, ITarget, IEffect
from raw_logger import logDebug, logInfo, info
from tags import Tag


raw_root = "D:\\Desktop\\Dwarf Fortress\\Dwarf Fortress - Original\\Dwarf Fortress 0.44.12\\raw\\objects"
raw_root = "."

file_name = "interaction_standard.txt"
file_name = "creature_z_dragons.txt"
file_name = "creature_z_dragons_test.txt"


class File(object):
	are_classes = {
		"interaction": Interaction,
		"i_target": ITarget,
		"i_effect": IEffect,
		"creature":  Creature,
		"caste": Caste,
		"select_caste": CasteGroup,
		"can_do_interaction": CanDoInteraction,
		"attack": Attack
	}

	special_functions = {}

	master_parents = []
	last_class = None

	file_blocks = {}
	regex = r"\[([\d\w\s\-\:\.,]+)\]"

	current_block_level = 0
	file_name = None
	file_type = None

	auto_add_tags = True

	@property
	def last_master_class(self):
		if len(self.master_parents):
			return self.master_parents[-1]
		else:
			return False

	def __init__(self, path, file_name):
		self.path = os.path.dirname(path)
		full_path = os.path.join(path, file_name)

		self.regex = re.compile(self.regex)

		if not os.path.isdir(path):
			self.logError("Invalid folder supplied")

		if not os.path.isfile(full_path):
			self.logError("Invalid file supplied")

		self.file_name = file_name.split(".")
		self.file_extension = self.file_name[-1]
		del(self.file_name[-1])
		self.file_name = "".join(self.file_name)

		with open(full_path, "r") as current_raw:
			for line in re.findall(self.regex, current_raw.read()):
				self.parse_line(line.lower())

			self.last_master_class.end_trigger()

		for current_class in self.master_parents:
			current_class.write_files()

	def parse_line(self, line):
		info['last_raw_line'] = line.upper()
		new_tag = Tag.parse(line)

		if self.is_class(new_tag):
			self.create_class(new_tag)

		elif new_tag.tag_name == "object":
			self.file_type = new_tag.tag_args[0]

		else:
			self.last_class.parse_tag(new_tag)

	def is_class(self, tag):
		return tag.tag_name in self.are_classes.keys()

	def create_class(self, tag):
		raw_class_dict = self.are_classes[tag.tag_name]
		default_obj = raw_class_dict

		new_class = types.new_class(
			name=(tag.tag_name + "-" + "-".join(tag.tag_args)).title(),
			bases=(default_obj,),
		)
		new_class = new_class(
			tag.tag_args,
			":".join(tag.tag_args),
			self,
			self.last_class,
			self.auto_add_tags
		)

		if not new_class.parents:
			if self.last_master_class:
				self.last_master_class.end_trigger()
			info['last_class'] = info['last_master_class'] = new_class
			self.last_class = self.last_master_parent = new_class
			self.master_parents.append(new_class)
			logDebug("Created <span id='{new_class}'>{new_class}</span> master class".format(new_class=new_class))

		elif new_class.class_type == "caste":
			self.last_class = new_class
			self.last_master_class.castes[new_class.args_list[0]] = new_class
			logDebug(
				"Created caste <span id='{new_class}'>{new_class}</span> into <a href='#{last_master}'>{last_master}</a> master class".format(
				new_class=new_class,
				last_master=self.last_master_class
			))

		elif new_class.class_type == "select_caste":
			self.last_class = new_class
			self.last_master_class.selected_castes.append(new_class)
			logDebug("Created caste selection <span id='{new_class}'>{new_class}</span> into <a href='#{last_master}'>{last_master}</a> master class".format(
				new_class=new_class,
				last_master=self.last_master_class
			))

		else:
			self.last_class.assign_class_parents(new_class)


file = File(raw_root, file_name)
logInfo("<pre>"+file.last_master_class.to_raw()+"</pre>")