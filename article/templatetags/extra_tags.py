from django import template

# 如果不加括号()，会报 TypeError: filter() missing 1 required positional argument: 'self'
register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})
