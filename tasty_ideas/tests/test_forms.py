from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from tasty_ideas.forms import (
    DishForm,
    CookForm,
    CookCreateForm,
    DishSearchForm,
    MainPageSearchForm,
)
from tasty_ideas.models import Category, Ingredient


class MainPageSearchFormTest(TestCase):

    def test_main_page_search_form_valid_data(self):
        form = MainPageSearchForm(data={"name": "Sushi"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Sushi")

    def test_main_page_search_form_empty_data(self):
        form = MainPageSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")


class DishSearchFormTest(TestCase):

    def test_dish_search_form_valid_data(self):
        form = DishSearchForm(data={"query": "Spicy"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "Spicy")

    def test_dish_search_form_empty_data(self):
        form = DishSearchForm(data={"query": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "")


class CookCreateFormTest(TestCase):

    def test_cook_create_form_valid_data(self):
        form = CookCreateForm(
            data={
                "username": "newcook",
                "first_name": "New",
                "last_name": "Cook",
                "email": "newcook@example.com",
                "password1": "strongpassword123",
                "password2": "strongpassword123",
            }
        )
        self.assertTrue(form.is_valid())
        cook = form.save()
        self.assertEqual(cook.username, "newcook")
        self.assertEqual(cook.first_name, "New")
        self.assertEqual(cook.last_name, "Cook")
        self.assertEqual(cook.email, "newcook@example.com")

    def test_cook_create_form_invalid_data(self):
        form = CookCreateForm(
            data={
                "username": "newcook",
                "first_name": "New",
                "last_name": "Cook",
                "email": "newcook@example.com",
                "password1": "strongpassword123",
                "password2": "differentpassword",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class CookFormTest(TestCase):

    def test_cook_form_valid_data(self):
        user = get_user_model().objects.create_user(
            username="testcook",
            first_name="Test",
            last_name="Cook",
            email="testcook@example.com",
        )
        form = CookForm(
            data={
                "username": "testcookupdated",
                "first_name": "Updated",
                "last_name": "Cook",
                "email": "updatedcook@example.com",
            },
            instance=user,
        )
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, "testcookupdated")
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "Cook")
        self.assertEqual(updated_user.email, "updatedcook@example.com")

    def test_cook_form_invalid_data(self):
        user = get_user_model().objects.create_user(
            username="testcook",
            first_name="Test",
            last_name="Cook",
            email="testcook@example.com",
        )
        form = CookForm(
            data={
                "username": "",
                "first_name": "Updated",
                "last_name": "Cook",
                "email": "updatedcook@example.com",
            },
            instance=user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class DishFormTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(dish_type="sushi")
        self.ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        self.ingredient2 = Ingredient.objects.create(name="Ingredient 2")

    def test_dish_form_valid_data(self):
        form = DishForm(
            data={
                "name": "Test Dish",
                "price": 10.99,
                "cooking_time": 30.0,
                "spicy": "easy",
                "category": self.category.pk,
                "difficulty": "easy",
                "recipe": "Test recipe",
                "ingredients": [self.ingredient1.pk, self.ingredient2.pk],
            }
        )
        self.assertTrue(form.is_valid())
        dish = form.save()
        self.assertEqual(dish.name, "Test Dish")
        self.assertEqual(dish.price, Decimal("10.99"))
        self.assertEqual(dish.cooking_time, 30.0)
        self.assertEqual(dish.spicy, "easy")
        self.assertEqual(dish.category, self.category)
        self.assertEqual(dish.difficulty, "easy")
        self.assertEqual(dish.recipe, "Test recipe")
        self.assertQuerysetEqual(
            dish.ingredients.all(),
            [self.ingredient1, self.ingredient2],
            transform=lambda x: x,
        )

    def test_dish_form_invalid_data(self):
        form = DishForm(
            data={
                "name": "",
                "price": 10.99,
                "cooking_time": 30.0,
                "spicy": "easy",
                "category": self.category.pk,
                "difficulty": "easy",
                "recipe": "Test recipe",
                "ingredients": [self.ingredient1.pk, self.ingredient2.pk],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
