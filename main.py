import os, re, types

from block import Block

from raw_logger import logDebug, logInfo, info, logError
from tags import Tag
import inspect, sys
import class_types.creature_classes
import class_types.interaction_classes

#raw_root = "D:\\Desktop\\Dwarf Fortress\\Dwarf Fortress - Original\\Dwarf Fortress 0.44.12\\raw\\objects"

raw_root = "."

#file_name = "interaction_standard.txt"
file_name = "creature_z_dragons.txt"
#file_name = "creature_z_dragons_test.txt"


class File(Block):
	def __init__(self, path, file_name, *args, **kwargs):
		super().__init__(Tag(), self, *args, **kwargs)
		self.are_classes = {}

		for class_types in ["class_types.creature_classes", "class_types.interaction_classes"]:
			for _, class_instance in inspect.getmembers(sys.modules[class_types], inspect.isclass):
				if hasattr(class_instance, 'class_type'):
					self.are_classes[class_instance.class_type] = class_instance


		regex = r"\[([\d\w\s\-\:\.,]+)\]"

		self.tag = None
		self.path = os.path.dirname(path)
		full_path = os.path.join(path, file_name)
		self.last_class_block = False

		self.regex = re.compile(regex)

		if not os.path.isdir(path):
			logError("Invalid folder supplied")

		if not os.path.isfile(full_path):
			logError("Invalid file supplied")

		self.file_name = file_name.split(".")
		self.file_extension = self.file_name[-1]
		del(self.file_name[-1])
		self.file_name = "".join(self.file_name)

		with open(full_path, "r") as current_raw:
			for line in re.findall(self.regex, current_raw.read()):
				self.parse_line(line.lower())

	def parse_line(self, line):
		if type(line) != Tag:
			info['last_raw_line'] = line.upper()
			new_tag = Tag.parse(line)
		else:
			new_tag = line

		if self.is_class(new_tag):
			self.create_class(new_tag)

		elif new_tag.tag_name == "object":
			self.tag = new_tag

		elif self.check_prefix(new_tag) == "INVALID":
			self.last_class_block = self.last_class_block.parent_block
			self.parse_line(new_tag)

		else:
			self.last_class_block.add_tag(new_tag)

	def is_class(self, tag):
		return tag.tag_name in self.are_classes.keys()

	def create_class(self, tag):
		raw_class_dict = self.are_classes[tag.tag_name]
		default_obj = raw_class_dict

		new_class = types.new_class(
			name=(tag.tag_name + "-" + "-".join(tag.tag_args)).title(),
			bases=(default_obj,),
		)

		self.assign_parents(new_class(tag))


	def check_prefix(self, tag_or_class):
		needed_prefix = self.last_class_block.tag.need_prefix
		if not needed_prefix:
			return True
		if type(tag_or_class) == Tag:
			if tag_or_class.prefix not in needed_prefix:
				return "INVALID"

		elif issubclass(type(tag_or_class), Tag):
			logError(tag_or_class)
			if tag_or_class.tag.prefix not in needed_prefix:
				return "INVALID"

		else:
			raise Exception("Invalid tag_or_class {} found".format(tag_or_class))


	def assign_parents(self, new_class):
		info['last_class'] = new_class
		if not new_class.parents:
			info['last_master_class'] = new_class
			self.last_class_block = self.create_block(new_class)
			logDebug("Created <span id='{new_class}'>{new_class}</span> master class".format(new_class=new_class))


		elif self.last_class_block.tag.class_type in new_class.parents:
			logDebug("Created <span id='{new_class}'>{new_class}</span> into {father}".format(
				new_class= new_class,
				father= self.last_class_block
			))

			self.last_class_block = self.last_class_block.create_block(new_class)

		elif self.last_class_block.parent_block:
			logDebug(
				"Start recursion for class {new_class} with type {class_type} with last class {last_class} to find {parents}".format(
					new_class=new_class,
					class_type= new_class.class_type,
					last_class=self.last_class_block,
					parents=new_class.parents
			))

			self.last_class_block = self.last_class_block.parent_block
			self.assign_parents(new_class)

		else:
			logDebug("No parent found for {new_class}".format(
				new_class=new_class,
			))
			raise(Exception("No parent found"))

	def to_raw(self):
		return self.file_name + ("\n"*2) + super().to_raw(True)


file = File(raw_root, file_name)
logInfo("<pre>"+ file.to_raw() +"</pre>")
