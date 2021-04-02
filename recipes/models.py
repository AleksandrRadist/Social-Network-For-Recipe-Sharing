from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    TAG_CHOICES = [
        ('breakfast', 'завтрак'),
        ('lunch', 'обед'),
        ('dinner', 'ужин'),
    ]
    title = models.CharField(
        max_length=50,
        choices=TAG_CHOICES
    )

    def __str__(self):
        return self.title


class Ingredient(models.Model):

    title = models.CharField(
        max_length=300
    )
    dimension = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.title)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='ingredients'
    )
    cooking_time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    tag = models.ManyToManyField(
        Tag, related_name='tags'
    )
    image = models.ImageField(
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-pub_date']

    def get_ingredients(self):
        return self.ingredient.all().values_list('title', flat=True)

    def get_tags(self):
        return self.tag.all().values_list('title', flat=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='quantities'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_quantity'
    )
    quantity = models.FloatField()

    def __str__(self):
        return str(self.ingredient)


class Cart(models.Model):
    shopper = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_carts'
    )

    def __str__(self):
        return self.recipe.title

    class Meta:
        unique_together = ('shopper', 'recipe')


class Favorit(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorits'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorits'
    )

    def __str__(self):
        return f'author - {self.author} | recipe - {self.recipe.title}'

    class Meta:
        unique_together = ('author', 'recipe')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    def __str__(self):
        return f'follower - {self.user} | following - {self.author}'

    class Meta:
        unique_together = ('user', 'author')
