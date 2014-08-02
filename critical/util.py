from __future__ import unicode_literals
from django.utils.six.moves import urllib


def download_css(css_entries):
    css = []
    for entry in css_entries:
        try:
            url = entry['href']
            css.append(urllib.request.urlopen(url).read())
        except KeyError:
            pass
        try:
            css.append(entry['text'])
        except KeyError:
            pass
    return ''.join(css)
