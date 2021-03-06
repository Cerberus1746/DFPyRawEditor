from tags import Tag

class Interaction(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "interaction"
		self.need_prefix = ["i",]
		self.parents = False

class ITarget(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "i_target"
		self.need_prefix = ["it",]
		self.parents = ["interaction",]
		self.allow_duplicates = True

class IEffect(Tag):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.class_type = "i_effect"
		self.need_prefix = ["ie", "syndrome"]
		self.parents = ["interaction",]