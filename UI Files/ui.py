"""
Communicate between Python and Javascript asynchronously using
inter-process messaging with the use of Javascript Bindings.
"""

import cefpython3.cefpython_py36 as cef
from jinja2 import Environment, FileSystemLoader, select_autoescape

import base64

mime_prepend = "data:"
mime_suffix = ";base64,"

mime_types = {
	"png": "image/png",
	"jpg": "image/jpg",
	"js": "application/javascript",
	"css": "text/css",
	"coffee": "application/vnd.coffeescript"
}

def to_base64(filename):
	extension = filename.split(".")[-1]
	with open(filename, "rb") as image_file:
		base_prefix = mime_prepend + mime_types[extension] + mime_suffix
		return base_prefix + base64.b64encode(image_file.read()).decode('utf8')

def main():
	env = Environment(
		loader=FileSystemLoader("templates"),
		autoescape=select_autoescape(['html',]),
	)

	env.filters['to_base64'] = to_base64

	template = env.get_template('main.html')

	html = template.render()

	cef.Initialize()
	browser = cef.CreateBrowserSync(url=cef.GetDataUrl(html), window_title="Javascript Bindings")

	cef.MessageLoop()
	del browser
	cef.Shutdown()


if __name__ == '__main__':
	main()
