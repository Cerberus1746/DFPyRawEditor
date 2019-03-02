from default_class import DefaultClass

class Interaction(DefaultClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.file_path = "library/interaction/"
		self.prefix = ["i",]
		self.parents = False

class ITarget(DefaultClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.file_path = "library/interaction/"
		self.prefix = ["it",]
		self.parents = ["interaction",]

class IEffect(DefaultClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.file_path = "library/interaction/"
		self.prefix = ["ie", "syndrome"]
		self.parents = ["interaction",]