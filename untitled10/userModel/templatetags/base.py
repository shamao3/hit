# base.py
from django import template
import json,re
register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary,str):
        dictionary=re.sub("u'","\"",dictionary)
        dictionary=re.sub("'","\"",dictionary)
        dictionary=json.loads(dictionary)
    return dictionary.get(key)