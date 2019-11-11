"""
Context processors for Sunshine UK
"""
from django.conf import settings

def settings_processor(request):
    md = {}
    for x in dir(settings):
        md[x] = getattr(settings, x)
    return md
