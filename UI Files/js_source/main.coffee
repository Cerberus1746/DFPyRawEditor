single_tag_regex = /\[([\d\w\-\., ]+)\]/gm
single_tag_subst = "[<span class='single_tag'>$1</span>]"

tag_arg_regex = /\[(.*)\:/gm
tag_arg_subst = "[<span class='attr_tag'>$1</span>:"

args_regex = /:([\d\w\-\., ]+)/gm
args_subst = ":<span class='args'>$1</span>"

default_app = new Vue
	el: "#app"
	data:
		message: "[CREATURE:DWARF]"
		highlighted: ""

	mounted: ->
		@highlighted = @message
		@apply_regex(@)

	watch:
		message: (val, oldVal) ->
			@highlighted = val
			@apply_regex(@)

	methods:
		tabber: (event) ->
			message = @message
			originalSelectionStart = event.target.selectionStart
			textStart = message.slice(0, originalSelectionStart)
			textEnd =  message.slice(originalSelectionStart)

			@message = "#{ textStart }\t#{ textEnd }"
			event.target.value = @message
			event.target.selectionEnd = event.target.selectionStart = originalSelectionStart + 1

		sync_scroll: (event) ->
			textarea = event.target
			div1 = document.getElementById("backdrop")
			div1.scrollTop = textarea.scrollTop

		apply_regex: (self) ->
			self.highlighted = self.highlighted.replace(single_tag_regex, single_tag_subst)
			self.highlighted = self.highlighted.replace(tag_arg_regex, tag_arg_subst)
			self.highlighted = self.highlighted.replace(args_regex, args_subst)