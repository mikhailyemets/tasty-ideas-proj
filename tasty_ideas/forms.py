from django import forms
from django.contrib.auth.forms import UserCreationForm

from tasty_ideas.models import Cook, Dish, Ingredient


class MainPageSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name.."
            }
        )
    )


class DishSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name or ingredient.."
            }
        )
    )


class CookCreateForm(UserCreationForm):
    class Meta:
        model = Cook
        fields = ['username', 'email', 'password1', 'password2']


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Dish
        fields = "__all__"

