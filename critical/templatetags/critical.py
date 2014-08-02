from __future__ import unicode_literals
from django import template

from .. import (CRITICAL_MARK_BEGIN, CRITICAL_MARK_END, CRITICAL_ASYNC_MARK,
                CRITICAL_KEY_MARK_BEGIN, CRITICAL_KEY_MARK_END)

register = template.Library()


class CriticalNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def get_original_content(self, context):
        return self.nodelist.render(context)

    def render(self, context):
        return ('{begin}{original_content}{end}'
                '<style id="django-critical-async-css-marker"></style>').format(
                    begin=CRITICAL_MARK_BEGIN,
                    end=CRITICAL_MARK_END,
                    original_content=self.get_original_content(context))


@register.tag
def critical(parser, token):
    """
    Extracts and inlines critical path CSS.

    Syntax::

        {% critical %}
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
        {% endcritical %}

    Which would be rendered something like::

        <style type="text/css">
        h1 { border:5px solid green; }
        </style>
    """

    nodelist = parser.parse(('endcritical',))
    parser.delete_first_token()

    args = token.split_contents()

    if len(args) != 1:
        raise template.TemplateSyntaxError(
            '{tag} tag takes no arguments.'.format(tag=args[0]))

    return CriticalNode(nodelist)


@register.simple_tag
def critical_async():
    return CRITICAL_ASYNC_MARK

@register.simple_tag
def critical_key(key):
    return '{begin}{key}{end}'.format(begin=CRITICAL_KEY_MARK_BEGIN,
                                      end=CRITICAL_KEY_MARK_END,
                                      key=key)
