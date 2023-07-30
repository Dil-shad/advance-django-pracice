from django import template

register = template.Library()

@register.filter
def addclass(value, token):
    value.field.widget.attrs["class"] = token
    return value

@register.filter
def addplaceholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value

# register.filter(addclass)
# register.filter(addplaceholder)