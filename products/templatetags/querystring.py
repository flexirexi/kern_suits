from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def querystring(request, **new_params):
    """Builds a query string"""
    query = request.GET.copy()
    for k, v in new_params.items():
        query[k] = v
    return urlencode(query)
