from django.urls import path

from . import views

urlpatterns = [
    path('subscriptions/', views.follow_index, name='subscriptions'),
    path('subscriptions/subscribe/', views.profile_follow, name='subscriptions_subscribe'),
    path('unsubscribe/<int:author_id>/', views.profile_unsubscribe, name='subscriptions_unsubscribe'),
    path('favorit/', views.favorit_index, name='favorit'),
    path('favorit/add/', views.favorite_add, name='favorit_add'),
    path('favorit/<int:recipe_id>/remove/', views.favorite_remove, name='favorit_remove'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('recipe/new/', views.recipe_new, name='recipe_new'),
    path(
        'recipe/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='recipe_edit'
    ),
    path(
        'recipe/<int:recipe_id>/delete/',
        views.recipe_delete,
        name='recipe_delete'
    ),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('cart/', views.cart_list, name='cart'),
    path(
        'cart/download/',
        views.cart_list_download,
        name='cart_download'
    ),
    path(
        'cart/<int:recipe_id>/remove/',
        views.cart_remove,
        name='cart_remove'
    ),
    path(
        'cart/<int:recipe_id>/delete/',
        views.cart_delete_recipe,
        name='cart_delete'
    ),
    path('cart/add/', views.cart_add, name='cart_add'),

    path('profile/<str:username>/', views.profile, name='profile'),
    path('', views.index, name='index'),
]
