from .models import Ingredient, RecipeIngredient, Tag


def get_ingredients(data):
    ingredients = {}
    for key, ingredient_name in data.items():
        if 'nameIngredient' in key:
            ingredient = key.split('_')
            quantity = data.get(f'valueIngredient_{ingredient[1]}')
            quantity = quantity.replace(',', '.')
            ingredients[ingredient_name] = float(quantity)
    return ingredients


def get_tags(request):
    if 'tags' in request.GET:
        tags = request.GET.get('tags')
        tag = tags.split(',')
        tags_qs = Tag.objects.filter(title__in=tag)
    else:
        tags_qs = None
    return tags_qs


def create_recipe_ingredient(ing_dict, recipe):
    for key in ing_dict:
        RecipeIngredient.objects.create(
            quantity=ing_dict[key],
            ingredient=Ingredient.objects.get(title=key),
            recipe=recipe,
        )
