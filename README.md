django-critical
===============

Inlines critical path CSS and defers loading full CSS asynchronously.

How it works
------------

`django-critical` parses the HTML between `{% critical %}` and `{% endcritical
%}` and searches for CSS.

```html
{% critical %}
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
<style>
  .jumbotron h1 {
    color: red;
  }
</style>
{% endcritical %}
```

It downloads and concatenates all CSS that it finds and uses
[penthouse](https://github.com/pocketjoso/penthouse/) to extract the
critical path CSS rules from it, which end up inlined and minified in place of
the original CSS.

```html
<style>html{font-family:sans-serif;-webkit-text-size-adjust:100%…</style>
```

Later in the HTML, before the closing `</body>` tag, the `{% critical_async %}`
template tag takes care of loading the rest of the CSS using FilamentGroup's
[loadCSS](https://github.com/filamentgroup/loadCSS).

Installation
------------

* Install `django-critical`:

```sh
pip install django-critical
```

* Add `critical` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = (
    # other apps
    "critical",
)
```

* Add `critical.middleware.CriticalCssMiddleware` to your `MIDDLEWARE_CLASSES`
  setting:

```python
MIDDLEWARE_CLASSES = (
    # other middlewares
    "critical.middleware.CriticalCssMiddleware",
)
```

* Point your `CRITICAL_PENTHOUSE_PATH` setting to the correct path, e.g.:

```python
CRITICAL_PENTHOUSE_PATH = os.path.join(
    BASE_DIR, 'node_modules/penthouse/penthouse.js')
```

Caching
-------

`django-critical` calculates the critical path CSS for the first request, caches
the result and reuses this CSS verbatim for further requests. Most web
applications have different critical path CSS for different groups of pages,
though. This can be solved using the `{% critical_key "<key>" %}` template tag,
so that different templates can have different caching keys.

Is this stable and ready for production use?
--------------------------------------------

No. `django-critical` is in a very early stage of development, so you should use
it at your own risk. [Bug
reports](https://github.com/martinblech/django-critical/issues) and
[contributions](https://github.com/martinblech/django-critical/pulls) are
welcome, though!
