from tags import Tag


class Attack(Tag):
	class_type = "attack"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["attack",]
		self.parents = ["caste", "creature", "select_caste"]

class CanDoInteraction(Tag):
	class_type = "can_do_interaction"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["cdi",]
		self.parents = ["caste", "creature", "select_caste"]

class Creature(Tag):
	class_type = "creature"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._current_index = -1


class Caste(Tag):
	class_type = "caste"
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.parents = ["creature",]


class SelectCaste(Tag):
	class_type = "select_caste"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.parents = ["creature",]

class SetTlGroup(Tag):
	class_type = "set_tl_group"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["tl", "bp"]
		self.parents = ["caste", "creature", "select_caste"]

#BODY_DETAIL_PLAN
class BodyDetailPlan(Tag):
	class_type = "body_detail_plan"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.parents = ["caste", "creature", "select_caste"]

class SetBpGroup(Tag):
	class_type = "set_bp_group"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["bp",]
		self.parents = ["caste", "creature", "select_caste"]

class BpAppearanceModifier(Tag):
	class_type = "bp_appearance_modifier"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["app",]
		self.parents = ["set_tl_group", "set_bp_group"]

class TlColorModifier(Tag):
	class_type = "tl_color_modifier"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["tlcm",]
		self.parents = ["set_tl_group",]

