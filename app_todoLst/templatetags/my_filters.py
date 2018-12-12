from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
#@stringfilter
def loc(lst,ind):
    return lst[ind]

@register.filter
#@stringfilter
def getAttr(obj,attrNm):
    return obj.__dict__[attrNm]


@register.filter
@stringfilter
def split(lstString):
    return lstString.split()
