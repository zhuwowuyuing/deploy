__author__ = 'liangnaihua'

from django import template

register = template.Library()

@register.filter
def diskmeasure(value):
    ret_mb = float(value)/1024/1024
    if ret_mb < 1:
        return "%.2f MB"%(ret_mb)
    elif ret_mb > 1 and ret_mb < 1024:
        return "%.2f MB"%(ret_mb)
    else:
        ret_gb = ret_mb/1024
        if ret_gb > 1:
            return "%.2f GB"%(ret_gb)

@register.filter
def memmeasure(value):
    ret_mb = float(value)/1024
    return "%.2f GB"%(ret_mb)


