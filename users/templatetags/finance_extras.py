from django import template


register = template.Library()


@register.filter
def space_intformat(value):
    try:
        value = float(value)
        return '{:,.0f}'.format(value).replace(',', ' ').replace('.', ' ')
    except (ValueError, TypeError):
        return value
