from django import template

register = template.Library()


@register.filter(name='replacer')
def replacer(value, arg):
    return value.replace(' ', arg)
