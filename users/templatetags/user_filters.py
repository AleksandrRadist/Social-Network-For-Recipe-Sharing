from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def pluralize(value, endings):
    endings = endings.split(',')
    if value % 100 in (11, 12, 13, 14):
        return endings[2]
    if value % 10 == 1:
        return endings[0]
    if value % 10 in (2, 3, 4):
        return endings[1]
    else:
        return endings[2]
