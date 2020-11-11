from django import template

register = template.Library()


@register.filter
def round_float(value):
    if value:
        return "{:,.1f}".format(value)
    else:
        return "0"
