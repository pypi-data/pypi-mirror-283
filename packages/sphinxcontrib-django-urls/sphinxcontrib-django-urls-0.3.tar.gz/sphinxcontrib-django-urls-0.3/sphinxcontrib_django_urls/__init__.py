try:
    from django.urls import get_resolver
except:
    try:
        from django.core.urlresolvers import get_resolver
    except:
        raise Exception("Can't find Django")

__version__ = "0.3"
urls = {}
def setup(app):
    global urls
    app.connect('autodoc-process-docstring', add_django_url)
    res = get_resolver()
    urls = {k:{'pattern':'','urls':v} for k,v in res.reverse_dict.items()}
    for ns in res.namespace_dict:
        pattern = str(res.namespace_dict[ns][1].pattern)
        urls.update({k:{'pattern':pattern,'urls':v} for k,v in res.namespace_dict[ns][1].reverse_dict.items()})


def add_django_url(app, what, name, obj, options, lines):
    if what == 'function':
        if obj in urls:
            url_struct = urls[obj]['urls']
            if len(url_struct) > 0:
                lines.append("URL path(s):")

                for url in url_struct[:-2]:
                    if type(url) == type([]): continue
                    lines.append("   * %s%s\n" % (urls[obj]['pattern'],url.replace("\\Z", '$')))
            else:
                lines.insert(0,"| has NO URL mapping\n")
        else:
            lines.append("URL path(s): NONE")

