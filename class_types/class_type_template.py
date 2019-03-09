from tags import Tag


class TypeName(Tag):
	"""


	"""
	class_type = "attack"

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		self.need_prefix = ["attack",]
		self.parents = ["caste", "creature", "select_caste"]