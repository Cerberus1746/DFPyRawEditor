from collections.abc import Iterable

from raw_logger import logDebug


class Tag(object):
	def __init__(self, tag_name="", tag_args:iter=None, owner_class=None):
		if isinstance(tag_name, Tag):
			self.tag_name = tag_name.tag_name
			self.tag_args = tag_name.tag_args
		else:
			if (isinstance(tag_args, Iterable) and not isinstance(tag_args, str)) or tag_args == None:
				self.tag_args = tag_args
			else:
				raise(Exception("tag_args attr has to be a iter"))

			if (":" in tag_name and tag_args == None) or ("[" in tag_name or "]" in tag_name):
				split_tag = tag_name.split(":")
				self.tag_name = split_tag[0]
				self.tag_args = split_tag[1:]
			else:
				self.tag_name = tag_name
				self.tag_args = tag_args


		self.prefix = self.tag_name.split("_")[0]
		self.owner = owner_class
		self.need_prefix = False
		self.parents = False

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def __lt__(self, other):
		return str(self) < str(other)

	def __hash__(self):
		if self.tag_args:
			return hash(self.tag_name + str(self.tag_args))
		else:
			return hash(self.tag_name)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return self.to_raw_line()

	@staticmethod
	def extract_info(raw_line):
		raw_line = raw_line.replace("[", "")
		raw_line = raw_line.replace("]", "")
		raw_line = raw_line.split(":")
		return (raw_line[0], raw_line[1:])

	@classmethod
	def parse(cls, raw_line):
		return cls(*Tag.extract_info(raw_line))

	def to_raw_line(self):
		raw_line = ":".join([self.tag_name, *self.tag_args])
		return "[" + raw_line + "]"

class TagGroup(object):
	def __init__(self, owner=None):
		self._group = set()
		self.owner = owner

	def __iter__(self):
		yield from self._group

	def __next__(self):
		return self._group.__next__()

	def __str__(self):
		return str(self._group)

	def __len__(self):
		return len(self._group)

	def add(self, tag):
		logDebug("Created tag {0} into <a href='#{1}'>{1}</a>".format(tag, self.owner))
		if isinstance(tag, Tag):
			Tag.owner = self.owner
			self._group.add(tag)
		else:
			self._group.add(Tag.parse(tag, owner=self.owner))

	def to_raw(self, auto_join):
		lines =  list(self._group)
		sorted_tags = sorted(lines, key=lambda x: (str(x)[:25] !='[select_additional_caste:', x))

		lines = [tag.to_raw_line() for tag in sorted_tags]

		if auto_join:
			return "\n".join(lines)

		else:
			return lines