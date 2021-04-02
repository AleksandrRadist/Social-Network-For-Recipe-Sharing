from django import template

from recipes.models import Cart, Favorit, Follow

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


@register.filter
def formatting_tags(request, tag):
    if 'tags' in request.GET:
        tags = request.GET.get('tags')
        tags = tags.split(',')
        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
        if '' in tags:
            tags.remove('')
        result = ','.join(tags)
        return result
    return tag


@register.filter(name='in_cart')
def in_cart(recipe, user):
    return Cart.objects.filter(shopper=user, recipe=recipe).exists()


@register.filter(name='in_follow')
def in_follow(author, user):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='in_favorite')
def in_favorite(recipe, user):
    return Favorit.objects.filter(author=user, recipe=recipe).exists()


@register.filter
def in_tags(request, tag):
    tags = []
    if 'tags' in request.GET:
        tags = request.GET.get('tags')
    if tag in tags:
        return True
    return False


@register.filter
def get_tags(request):
    tags = []
    if 'tags' in request.GET:
        tags = request.GET.get('tags')
    return tags
