from django import template

register = template.Library()


@register.filter
def get_attr(obj: object, attr: str):
    return getattr(obj, attr)
