from block import Block
from raw_logger import logDebug
from tags import Tag


class Attack(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "attack"
		self.file_path = "library/attack/"
		self.need_prefix = ["attack",]
		self.parents = ["caste", "creature", "caste_group"]

class CanDoInteraction(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "can_do_interaction"
		self.file_path = "library/interaction/"
		self.need_prefix = ["cdi",]
		self.parents = ["caste", "creature", "caste_group"]

class Creature(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "creature"
		self.file_path = "library/creature/"
		self.castes = Block(father=self)
		self.selected_castes = []

		self._current_index = -1

	def __getitem__(self, key):
		return self.castes[key]


class Caste(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "caste"
		self.parents = ["creature",]


class CasteGroup(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.additional_castes = set()
		self.class_type = "caste_group"
		self.parents = ["creature",]

		#self.register_special_tag("select_additional_caste", self.select_additional_caste)

	def select_additional_caste(self, args:str):
		self.additional_castes.add(args)
		logDebug("Selecting additional caste {0} in <a href='#{1}'>{1}</a>\nSelected castes: {2}".format(args, self, self.args_list))