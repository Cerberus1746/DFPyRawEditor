"""
Communicate between Python and Javascript asynchronously using
inter-process messaging with the use of Javascript Bindings.
"""

import cefpython3.cefpython_py36 as cef
from jinja2 import Environment
from hamlish_jinja import HamlishExtension

g_htmlcode = """
%html
	%head
		%script src = "http://coffeescript.org/v2/browser-compiler/coffeescript.js"  type = "text/javascript"
		%script type = "text/coffeescript"
			parts = ["Hello", "from", "CoffeeScript"]
			for part in parts
				console.log part
			txt = parts.join ' '
			txt += "."

		%style
			body, html {
				font-family: Arial;
				font-size: 11pt;
			}

		%script
			function print(msg) {
				document.getElementById("console").innerHTML += msg+"<br>";
			}

			function js_function(value) {
				print("Value sent from Python: <b>"+value+"</b>");
				py_function("I am a Javascript string #1", js_callback);
			}

			function js_callback(value, py_callback) {
				print("Value sent from Python: <b>"+value+"</b>");
				py_callback("I am a Javascript string #2");
			}
	%body
		%h1
			Javascript Bindings
		#console
"""

def main():
	env = Environment(extensions=[HamlishExtension])
	env.hamlish_mode = 'indented'
	env.hamlish_enable_div_shortcut = True

	html = env.hamlish_from_string(g_htmlcode).render()

	print(html)

	cef.Initialize()
	browser = cef.CreateBrowserSync(url=cef.GetDataUrl(html), window_title="Javascript Bindings")
	browser.SetClientHandler(LifespanHandler())
	bindings = cef.JavascriptBindings()
	bindings.SetFunction("py_function", py_function)
	bindings.SetFunction("py_callback", py_callback)
	browser.SetJavascriptBindings(bindings)
	cef.MessageLoop()
	del browser
	cef.Shutdown()


def py_function(value, js_callback):
	print("Value sent from Javascript: "+value)
	js_callback.Call("I am a Python string #2", py_callback)


def py_callback(value):
	print("Value sent from Javascript: "+value)


class LifespanHandler(object):
	def OnLoadEnd(self, browser, **_):
		browser.ExecuteFunction("js_function", "I am a Python string #1")


if __name__ == '__main__':
	main()
