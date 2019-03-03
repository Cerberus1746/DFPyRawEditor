# -*- coding: utf-8 -*-
import logging
import os


file_header = """
<html>
	<head>
		<style>
			body {
				width: 100%%;
			}

			ul {
				margin-top: 0px;
				padding-top: 0px;
			}

			li p {
				margin-top: 0px;
				padding-top: 0px;
			}

			.class_name {
				color: blue;
			}

			.raw_line {
				font-style: oblique
			}

			.error {
				margin-bottom: 0px;
				padding-bottom: 0px;
			}
		</style>
	</head>
	<body>"""

file_footer = """</body>
</html>
"""
class FileHandlerWithHeader(logging.FileHandler):
	def __init__(self, filename, header, footer, mode='a', encoding=None, delay=0):
		self.header = header
		self.footer = footer
		self.file_pre_exists = os.path.exists(filename)

		logging.FileHandler.__init__(self, filename, mode, encoding, delay)

		if not delay and self.stream is not None:
			self.stream.write('%s\n' % header)

	def emit(self, record):
		if self.stream is None:
			self.stream = self._open()

			if not self.file_pre_exists:
				self.stream.write('%s\n' % self.header)

		logging.FileHandler.emit(self, record)

	def close(self):
		self.stream.write('\n%s' % self.footer)
		super().close()

class MyFormatter(logging.Formatter):
	err_fmt = u"\t\t<p style='color:red;'>ERROR: %(msg)s</p>"
	info_fmt = u"\t\t<p class='error'>%(msg)s</p>"

	dbg_fmt = '''
		<ul>
			<li>
				<b>Last master class:</b>
				<span class="class_name"><a href="#%(last_master_class)s">%(last_master_class)s</a></span>
			</li>
			<li>
				<b>Last class:</b>
				<span class="class_name"><a href="#%(last_class)s">%(last_class)s</a></span>
			</li>
			<li>
				<b>Last raw line:</b>
				<span class="raw_line">[%(last_raw_line)s]</span>
			</li>
			<li>
				<b>Message:</b>
				<p>%(message)s<p>
			</li>
		</ul>'''

	def __init__(self):
		super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

	def format(self, record):
		format_orig = self._style._fmt

		if record.levelno == logging.DEBUG:
			self._style._fmt = MyFormatter.dbg_fmt

		elif record.levelno == logging.INFO:
			self._style._fmt = MyFormatter.info_fmt

		elif record.levelno == logging.ERROR:
			self._style._fmt = MyFormatter.err_fmt

		result = logging.Formatter.format(self, record)
		self._style._fmt = format_orig

		return result


file_log = "{0}/{1}.html".format(".", "debug")

info = {
	'last_master_class': None,
	'last_class': None,
	'last_raw_line': None
}

rootLogger = logging.getLogger("root")
rootLogger.setLevel(logging.DEBUG)

fileHandler = FileHandlerWithHeader(file_log, file_header, file_footer, mode="w")
fileHandler.setFormatter(MyFormatter())

rootLogger.addHandler(fileHandler)
rootLogger.addHandler(logging.StreamHandler())

def logDebug(message):
	rootLogger.debug(message, extra=info)

def logInfo(message):
	rootLogger.info(message, extra=info)

def logWarn(message):
	rootLogger.warn(message, extra=info)

def logError(message):
	rootLogger.error(message, extra=info)
	raise Exception(message)
