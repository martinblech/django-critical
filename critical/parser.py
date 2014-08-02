from django.utils.six.moves import html_parser


class CssCollectorHtmlParser(html_parser.HTMLParser):
    def __init__(self, content):
        html_parser.HTMLParser.__init__(self)
        self.content = content
        self._current_tag = None
        self.css_entries = []
        self.feed(self.content)
        self.close()

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == 'link':
            is_css = False
            url = None
            for name, value in attrs:
                name = name.strip().lower()
                if (name == 'rel' and value.strip().lower() == 'stylesheet'):
                    is_css = True
                if name == 'href':
                    url = value.strip()
            if not is_css:
                return
            self.css_entries.append({'href': url})
        if tag == 'style':
            self.css_entries.append({})
            self._current_tag = tag

    def handle_endtag(self, tag):
        if self._current_tag and self._current_tag == tag.lower():
            self._current_tag = None

    def handle_data(self, data):
        if self._current_tag == 'style':
            self.css_entries[-1]['text'] = data


def extract_css_entries(request, content):
    parser = CssCollectorHtmlParser(content)
    css_entries = parser.css_entries
    for entry in css_entries:
        try:
            entry['href'] = request.build_absolute_uri(entry['href'])
        except KeyError:
            pass
    return css_entries
