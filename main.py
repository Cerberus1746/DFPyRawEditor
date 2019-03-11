'''
Authors:
	Leandro (Cerberus1746) Benedet Garcia
'''

import inspect, sys
import os, re, types, json, yaml

from block import Block
import class_types.creature_classes  # @UnusedImport
import class_types.interaction_classes  # @UnusedImport
from raw_logger import logDebug, logInfo, info, logError
from tags import Tag

#raw_root = "D:\\Desktop\\Dwarf Fortress\\Dwarf Fortress - Original\\Dwarf Fortress 0.44.12\\raw\\objects"
raw_root = "."

#file_name = "interaction_standard.txt"
file_name = "creature_z_dragons.txt"
#file_name = "creature_z_dragons_test.txt"
#file_name = "creature_standard_test.txt"


class File(Block):
	def __init__(self, path, file_name, *args, **kwargs):
		super().__init__(Tag(file_name, [path,]), self, *args, **kwargs)
		self.are_classes = {}

		for class_types in ["class_types.creature_classes", "class_types.interaction_classes"]:
			for _, class_instance in inspect.getmembers(sys.modules[class_types], inspect.isclass):
				if hasattr(class_instance, 'class_type'):
					self.are_classes[class_instance.class_type] = class_instance


		regex = r"\[([\d\w\-\:\., ]+)\]"

		self.tag = None
		self.path = os.path.dirname(path)
		full_path = os.path.join(path, file_name)

		self.regex = re.compile(regex)

		if not os.path.isdir(path):
			logError("Invalid folder supplied", IOError())

		if not os.path.isfile(full_path):
			logError("Invalid file supplied", IOError())

		self.file_name = file_name.split(".")
		self.file_extension = self.file_name[-1]
		del(self.file_name[-1])
		self.file_name = "".join(self.file_name)

		with open(full_path, "r") as current_raw:
			for line in re.findall(self.regex, current_raw.read()):
				self.parse_line(line.lower())

	def parse_line(self, line):
		split_line = line.split(":")
		tag_name = split_line[0]
		tag_args =  split_line[1:]
		tag_prefix = tag_name.split("_")[0]

		if self.is_class(tag_name):
			self.create_class(tag_name, tag_args)

		elif tag_name == "object":
			self.tag = Tag.parse(line)

		elif self.check_prefix(tag_prefix) == "INVALID":
			self.last_class_block = self.last_class_block.parent_block
			self.parse_line(line)

		else:
			self.last_class_block.add_tag(Tag.parse(line))

	def is_class(self, tag_name):
		return tag_name in self.are_classes.keys()

	def create_class(self, tag_name, tag_args):
		raw_class_dict = self.are_classes[tag_name]
		default_obj = raw_class_dict

		new_class = types.new_class(
			name=(tag_name + "-" + "-".join(tag_args)).title(),
			bases=(default_obj,),
		)
		new_class = new_class(tag_name, tag_args)

		self.assign_parents(new_class)


	def check_prefix(self, prefix):
		needed_prefix = self.last_class_block.tag.need_prefix
		if not needed_prefix:
			return True

		if prefix not in needed_prefix:
			return "INVALID"

	def assign_parents(self, new_class):
		info['last_class'] = new_class
		try:
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
					"Start recursion for class {new_class} with type {class_type} \
					with last class {last_class} to find {parents}".format(
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
		except AttributeError as e:
			logDebug(self.last_block)
			logError(self.last_block, e)

	def to_raw(self):
		return self.file_name + ("\n" * 2) + super().to_raw(True)

	def to_json(self):
		with open("export.json", "w") as json_file:
			json.dump(super().to_dict(), json_file, indent=4)

	def to_yaml(self):
		with open("export.yaml", "w") as yaml_file:
			yaml.dump(super().to_dict(), yaml_file, indent=4)

if __name__ == "__main__":
	file = File(raw_root, file_name)
	file.to_json()
	file.to_yaml()
	#logInfo("<pre>" + file.to_raw() + "</pre>")