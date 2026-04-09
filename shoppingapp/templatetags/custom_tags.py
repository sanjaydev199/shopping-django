from django import template

register = template.Library()

@register.filter
def remaining_stars(value):
    """Returns the remaining stars out of 5."""
    return 5 - value