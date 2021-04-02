import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import paginator_items_on_page as items_on_page

from .forms import RecipeForm
from .models import (Cart, Favorit, Follow, Ingredient, Recipe,
                     RecipeIngredient, User)
from .service import create_recipe_ingredient, get_ingredients, get_tags


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def index(request):
    recipes = Recipe.objects.select_related(
        'author').prefetch_related('tag',)

    tags_qs = get_tags(request)
    if tags_qs:
        recipes = Recipe.objects.filter(tag__in=tags_qs).distinct()

    paginator = Paginator(recipes, items_on_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'recipe': recipes
    })


def profile(request, username):
    account = get_object_or_404(User, username=username)
    account_recipes = account.recipes.all()

    tags_qs = get_tags(request)
    if tags_qs:
        account_recipes = Recipe.objects.filter(
            author=account, tag__in=tags_qs).distinct()

    paginator = Paginator(account_recipes, items_on_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {
        'page': page,
        'paginator': paginator,
        'profile': account,
        'recipe': account_recipes
    })


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    return render(request, 'includes/recipe.html', {
        'recipe': recipe
    })


@login_required
def recipe_new(request):
    author = get_object_or_404(User, username=request.user)

    recipe_form = RecipeForm(
        request.POST or None, files=request.FILES or None
    )

    ingredients_list = get_ingredients(request.POST)

    if recipe_form.is_valid():
        if len(ingredients_list) == 0:
            recipe_form.add_error('title', 'Добавьте хотя бы 1 ингредиент')
            return render(request, 'recipe_form.html', {'form': recipe_form, })
        if [x for x in ingredients_list.values() if float(x) <= 0]:
            recipe_form.add_error('title', 'Количество ингредиентов не '
                                           'может быть равно 0 или меньше')
            return render(request, 'recipe_form.html', {'form': recipe_form, })
        recipe = recipe_form.save(commit=False)
        recipe.author = author
        recipe.save()
        create_recipe_ingredient(ingredients_list, recipe)
        recipe_form.save_m2m()
        return redirect('index')
    return render(request, 'recipe_form.html', {'form': recipe_form, })


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe.id)

    ingredients_in_recipe = RecipeIngredient.objects.filter(
        recipe=recipe).select_related('ingredient').all()
    ingredients_list_old = []

    for item in ingredients_in_recipe:
        ingredient_item = []
        ingredient_item.append(item.ingredient.title)
        ingredient_item.append(item.quantity)
        ingredient_item.append(item.ingredient.dimension)
        ingredients_list_old.append(tuple(ingredient_item))

    recipe_form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe)

    ingredients_list = get_ingredients(request.POST)
    if recipe_form.is_valid():
        if len(ingredients_list) == 0:
            recipe_form.add_error('title', 'Добавьте хотя бы 1 ингредиент')
            return render(request, 'recipe_form.html', {'form': recipe_form, })
        if [x for x in ingredients_list.values() if float(x) <= 0]:
            recipe_form.add_error('title', 'Количество ингредиентов не '
                                           'может быть равно 0 или меньше')
            return render(request, 'recipe_form.html', {'form': recipe_form, })
        recipe = recipe_form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe.quantities.all().delete()
        create_recipe_ingredient(ingredients_list, recipe)
        recipe_form.save_m2m()
        return redirect('index')
    return render(request, 'recipe_change_form.html', {
        'form': recipe_form,
        'recipe': recipe,
        'ingredients_list_old': ingredients_list_old
    })


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def ingredients(request):
    ingredient = request.GET['query']
    ingredient_list = list(Ingredient.objects.filter(
        title__icontains=ingredient).values('title', 'dimension'))
    return JsonResponse(ingredient_list, safe=False)


@login_required
def cart_add(request):
    recipe_id = json.loads(request.body)['id']
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if Cart.objects.get_or_create(
            shopper=request.user, recipe=recipe):
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def cart_remove(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    user = get_object_or_404(User, username=request.user.username)

    obj = get_object_or_404(Cart, shopper=user, recipe=recipe)
    if obj.delete():
        return JsonResponse({'success': False})
    return JsonResponse({'success': True})


@login_required
def cart_list(request):
    recipes = request.user.carts.all()
    return render(request, 'cart_list.html', {'recipes': recipes})


@login_required
def cart_delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Cart, shopper=request.user, recipe=recipe_id)
    recipe.delete()
    return redirect('cart')


@login_required
def cart_list_download(request):
    recipes = Recipe.objects.filter(recipe_carts__shopper=request.user).values(
        'ingredient__title', 'ingredient__dimension', )

    ingredients_list = recipes.annotate(
        quantity=Sum('quantities__quantity')
    ).order_by()

    ingredient_txt = [
        (f"\u2022 {item['ingredient__title'].capitalize()} "
         f"({item['ingredient__dimension']}) \u2014 {item['quantity']} \n")
        for item in ingredients_list
    ]
    file = 'ingredients.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file}'
    return response


@login_required
def follow_index(request):
    follows = Follow.objects.select_related(
        'user', 'author'
    ).filter(user=request.user)

    paginator = Paginator(follows, items_on_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator,
    })


@login_required
def profile_follow(request):
    author_id = json.loads(request.body)['id']
    author = get_object_or_404(User, id=author_id)

    if request.user == author:
        return JsonResponse({'success': False})

    if not Follow.objects.filter(
            user=request.user, author=author
    ).exists():
        follow = Follow(user=request.user, author=author)
        follow.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def profile_unsubscribe(request, author_id):
    author = get_object_or_404(User, id=author_id)
    if Follow.objects.filter(user=request.user, author=author).delete():
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def favorit_index(request):
    favorit_recipes = Recipe.objects.select_related(
        'author'
    ).prefetch_related('tag',).filter(favorits__author=request.user)

    tags_qs = get_tags(request)
    if tags_qs:
        favorit_recipes = Recipe.objects.filter(
            favorits__author=request.user, tag__in=tags_qs
        ).distinct()

    paginator = Paginator(favorit_recipes, items_on_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorit.html', {
        'page': page,
        'paginator': paginator,
        'recipe': favorit_recipes
    })


@login_required
def favorite_add(request):
    recipe_id = json.loads(request.body)['id']
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if Favorit.objects.get_or_create(author=request.user, recipe=recipe):
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def favorite_remove(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=request.user.username)
    favorit = get_object_or_404(Favorit, author=author, recipe=recipe)
    if favorit.delete():
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
