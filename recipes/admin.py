from django.contrib import admin

from .models import (Cart, Favorit, Follow, Ingredient, Recipe,
                     RecipeIngredient, Tag)


class IngredientsInline(admin.TabularInline):
    model = Recipe.ingredient.through


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'description',
        'get_ingredients',
        'cooking_time',
        'pub_date',
        'get_tags',
        'image',
    )
    inlines = [IngredientsInline, ]
    exclude = ('ingredient',)
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity',)
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


class CartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'shopper',)
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class FavoritAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe',)
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorit, FavoritAdmin)
