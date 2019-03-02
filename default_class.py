import json, os

from raw_logger import logDebug, logError, info
from tags import TagGroup, Tag


class DefaultClass(object):
	def __init__(self, args_list, id_name, file_class, father, auto_add_tags = False):
		self.father = father
		self.id_name = id_name
		self.args_list = args_list
		self.file_class = file_class

		self.tags = TagGroup(self)
		self.child_raw_classes = []

		self.file_path = ""
		self.tags_file = 'tags.json'
		self.tags_with_args_file = 'tags_with_attrs.json'

		self.prefix = False
		self.parents = False

		if not auto_add_tags:
			with open(os.path.join(self.file_path, self.tags_file)) as tag_file:
				self.available_tags = json.load(tag_file)

			with open(os.path.join(self.file_path, self.tags_with_args_file)) as tag_with_attrs:
				self.available_arg_with_tags = json.load(tag_with_attrs)

	def __len__(self):
		return len(self.tags)

	def __iter__(self):
		return self.all_tags

	def __next__(self):
		return self.next()

	def next(self):
		self.current_index += 1
		if self.current_index < len(self):
			return self.all_tags[self.current_index]
		else:
			raise StopIteration()

	def __str__(self):
		return self.__class__.__name__

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash(self.id_name + str(self.args_list))

	@property
	def last_class(self):
		return self.file_class.last_class

	@last_class.setter
	def last_class(self, value):
		info['last_class'] = value
		self.file_class.last_class = value

	@property
	def last_master_class(self):
		return self.file_class.last_master_class

	@property
	def special_functions(self):
		return self.file_class.special_functions

	def is_special(self, tag):
		return tag.tag_name in self.special_functions.keys()

	def execute_special(self, tag:Tag):
		current_function = self.special_functions[tag.tag_name]
		if self.class_type not in current_function["available_types"]:
			raise(Exception("Invalid class type"))

		current_function["function"](*tag.tag_args)

	def special_is_valid(self, tag:Tag):
		check_avalaibles = self.special_functions[tag.tag_name]["available_types"]
		return_value = self.class_type in check_avalaibles

		logDebug("Checking special {} with available class type {} with result {}".format(tag, check_avalaibles, return_value))
		return return_value

	def parse_tag(self, tag:Tag):
		if self.prefix:
			if tag.prefix not in self.prefix:
				self.last_class = self.father
				return self.last_class.parse_tag(tag)

		if self.is_special(tag):
			if self.special_is_valid(tag):
				self.execute_special(tag)
			else:
				self.last_class = self.father
				logDebug(
					"Start recursion with special tag {0} to avoid <a href='#{1}'>{1}</a> to find {2}" % (
						tag,
						self,
						self.special_functions[tag.tag_name]["available_types"]
					)
				)
				return self.last_class.parse_tag(tag)
		else:
			self.tags.add(tag)

	def assign_class_parents(self, new_class):
		if self.last_class.class_type in new_class.parents:
			new_class.father.child_raw_classes.append(new_class)

			logDebug("Created <span id='{last_class}'>{last_class}</span> child class into {father} from {this}".format(
				last_class=new_class,
				father=new_class.father,
				this=self
			))
			self.last_class = new_class

		elif self.last_class.father:
			logDebug("Start Recursion for {0!s} to find {1!s} to evade <a href='#{2!s}'>{2!s}</a>".format(
				new_class,
				new_class.parents,
				self.last_class
			))
			self.last_class = self.last_class.father
			self.assign_class_parents(new_class)
		else:
			logError("Invalid class {} for {} or {}" % (new_class, self.last_class, self.last_class.father))

	def register_special_tag(self, tag, special_function):
		if not tag in self.special_functions.keys():
			self.special_functions[tag] = {
				"function": special_function,
				"available_types": set()
			}
			is_new = True

		else:
			is_new = False

		self.special_functions[tag]["available_types"].add(self.class_type)
		return is_new

	def end_trigger(self):
		pass

	def to_raw(self):
		lines = []
		lines.append("[" + ":".join((self.class_type, self.id_name)) + "]")
		lines.append(self.tags.to_raw())

		for child in self.child_raw_classes:
			lines.append(child.to_raw())

		return "\n".join(lines)


	def write_files(self):
		if not self.file_class.auto_add_tags:
			with open(os.path.join(self.file_path, self.tags_file), "w") as json_file:
				tmp_tags = {}
				for tag in self.single_tags:
					tmp_tags[tag] = {"description": ""}
				json_file.write(json.dumps(tmp_tags, sort_keys=True, indent=4))

			with open(os.path.join(self.file_path, self.tags_with_args_file), "w") as json_file:
				json_file.write(json.dumps(list(self.tags_with_args), sort_keys=True, indent=4))