from tags import Tag


class Attack(Tag):
	class_type = "attack"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["attack",]
		self.parents = ["caste", "creature", "select_caste"]
		self.allow_duplicates = True

class CanDoInteraction(Tag):
	class_type = "can_do_interaction"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["cdi",]
		self.parents = ["caste", "creature", "select_caste"]
		self.allow_duplicates = True

class Creature(Tag):
	class_type = "creature"


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

		self.need_prefix = ["tl", "bp", "plus"]
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
		self.parents = ["set_tl_group", "caste", "creature", "select_caste"]

#SELECT_TISSUE_LAYER
class SelectTissueLayer(Tag):
	class_type = "select_tissue_layer"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["plus", "tl"]
		self.parents = ["caste", "creature", "select_caste"]

#TISSUE_LAYER_APPEARANCE_MODIFIER
class TissueLayerAppearanceModifier(Tag):
	class_type = "tissue_layer_appearance_modifier"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["app",]
		self.parents = ["tl_color_modifier", "set_tl_group"]

#TISSUE_STYLE_UNIT
class TissueStyleUnit(Tag):
	class_type = "tissue_style_unit"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.need_prefix = ["tsu",]
		self.parents = ["set_tl_group",]
