from block import Block

class Interaction(Block):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.file_path = "library/interaction/"
		self.prefix = ["i",]
		self.parents = False

class ITarget(Block):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.file_path = "library/interaction/"
		self.prefix = ["it",]
		self.parents = ["interaction",]

class IEffect(Block):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.file_path = "library/interaction/"
		self.prefix = ["ie", "syndrome"]
		self.parents = ["interaction",]