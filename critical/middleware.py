from __future__ import unicode_literals
import hashlib
import re

from cssmin import cssmin

from django.core.cache import cache
from django.template import Context
from django.template.loader import get_template

from .marks import (CRITICAL_MARK_BEGIN, CRITICAL_MARK_END, CRITICAL_ASYNC_MARK,
                    CRITICAL_KEY_MARK_BEGIN, CRITICAL_KEY_MARK_END)
from .parser import extract_css_entries
from .util import download_css
from .core import get_critical_css


CRITICAL_CSS_RE = re.compile(
    '{begin}(.*?){end}'.format(begin=re.escape(CRITICAL_MARK_BEGIN),
                               end=re.escape(CRITICAL_MARK_END)),
    re.MULTILINE | re.DOTALL)
ASYNC_SNIPPET_RE = re.compile(re.escape(CRITICAL_ASYNC_MARK))
CRITICAL_KEY_RE = re.compile(
    '{begin}(.*?){end}'.format(begin=re.escape(CRITICAL_KEY_MARK_BEGIN),
                               end=re.escape(CRITICAL_KEY_MARK_END)))


class CriticalCssMiddleware(object):
    def process_response(self, request, response):
        if response.streaming:
            return response

        content = response.content

        match = CRITICAL_CSS_RE.search(content)

        if not match:
            return response

        critical_css_fragment = match.group(1)

        key_match = CRITICAL_KEY_RE.search(content)
        if key_match:
            content = CRITICAL_KEY_RE.sub('', content)
            key = key_match.group(1)
        else:
            key = 'default'

        h = hashlib.sha1()
        h.update(critical_css_fragment)
        cache_key = 'django_critical:{hash}:{key}'.format(
            hash=h.hexdigest(), key=key)

        cached = cache.get(cache_key)

        if cached is not None:
            new_fragment, css_entries = cached
        else:
            css_entries = extract_css_entries(request, critical_css_fragment)
            css = download_css(css_entries)
            critical_css = get_critical_css(response.content, css)
            critical_css = cssmin(critical_css)
            new_fragment = '<style>{css}</style>'.format(
                css=critical_css.replace('\\', '\\\\'))
            cache.set(cache_key, (new_fragment, css_entries))

        content = CRITICAL_CSS_RE.sub(new_fragment, content)

        async_snippet_template = get_template('critical/async_snippet.html')
        async_snippet = async_snippet_template.render(Context({
            'critical_css_fragment': critical_css_fragment,
            'css_entries': css_entries,
        }))

        content = ASYNC_SNIPPET_RE.sub(async_snippet, content)

        response.content = content
        return response
