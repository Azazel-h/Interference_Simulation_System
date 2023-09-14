from typing import Any

from django import template

register = template.Library()


@register.simple_tag
def apply_meth_on_list_elems(target: list, method: str, *params: Any):
    return [getattr(i, method)(*params) for i in target]
