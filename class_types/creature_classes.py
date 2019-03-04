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

		self._current_index = -1


class Caste(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "caste"
		self.parents = ["creature",]


class CasteGroup(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "caste_group"
		self.parents = ["creature",]

