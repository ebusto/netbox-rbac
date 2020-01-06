from pygments            import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers     import PythonLexer, YamlLexer

from django import template

import yaml

register = template.Library()

def render(lexer, value):
	return highlight(value, lexer, HtmlFormatter(
		nobackground = True,
		noclasses    = True,
		prestyles    = 'background: #ffffff; border: 0px; font-family: default; padding: 2px; width: min-content;',
	))

@register.filter(name='render_python')
def render_python(value):
	return render(PythonLexer(), value)

@register.filter(name='render_yaml')
def render_yaml(value):
	return render(YamlLexer(), yaml.dump(value))
