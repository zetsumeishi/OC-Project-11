from django import template

register = template.Library()


@register.filter
def round_float(value):
    return "{:,.1f}".format(value)
