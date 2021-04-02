from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'cooking_time', 'description', 'image')
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
