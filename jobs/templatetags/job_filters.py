from django import template

register = template.Library()


@register.filter
def in_list(value, arg):
    """Check if value is in the given list/iterable."""
    return value in (arg or [])