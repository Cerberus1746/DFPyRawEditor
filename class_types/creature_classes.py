from default_class import DefaultClass
from raw_logger import logDebug


class Attack(DefaultClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "attack"
		self.file_path = "library/attack/"
		self.prefix = ["attack",]
		self.parents = ["caste", "creature", "caste_group"]

class CanDoInteraction(DefaultClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "can_do_interaction"
		self.file_path = "library/interaction/"
		self.prefix = ["cdi",]
		self.parents = ["caste", "creature", "caste_group"]

class Creature(DefaultClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "creature"
		self.file_path = "library/creature/"
		self.castes = {}
		self.castes_tags = {}
		self.castes_classes = {}
		self.selected_castes = []

		self._current_index = -1

	def __getitem__(self, key):
		return self.castes[key]

	def assign_class_parents(self, new_class):
		if new_class.class_type == "caste":
			self.last_class = new_class
			self.register_caste(new_class)

		elif new_class.class_type == "caste_group":
			self.last_class = new_class
			self.selected_castes.append(new_class)

		else:
			return super().assign_class_parents(new_class)

	def to_raw(self):
		lines = []
		lines.append(super().to_raw())

		for current_caste in self.castes.values():
			lines.append(current_caste.to_raw())

		for current_caste in self.selected_castes:
			lines.append(current_caste.to_raw())

		return "\n".join(lines)


class Caste(DefaultClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "caste"
		self.parents = ["creature",]


class CasteGroup(Caste):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.additional_castes = set()
		self.class_type = "caste_group"

		self.register_special_tag("select_additional_caste", self.select_additional_caste)

	def select_additional_caste(self, args:str):
		self.additional_castes.add(args)
		logDebug("Selecting additional caste {0} in <a href='#{1}'>{1}</a>\nSelected castes: {2}".format(args, self, self.args_list))

	def to_raw(self):
		lines = []
		lines.append("[" + ":".join((self.class_type, self.id_name)) + "]")
		for additional in self.additional_castes:
			lines.append("[select_additional_caste:" + additional + "]")

		lines.append(self.tags.to_raw())

		for child in self.child_raw_classes:
			lines.append(child.to_raw())

		return "\n".join(lines)