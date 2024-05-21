from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from tasty_ideas.models import Category, Ingredient, Dish, Review


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(dish_type="sushi")
        self.assertEqual(category.dish_type, "sushi")
        self.assertEqual(str(category), "sushi")


class CookModelTest(TestCase):
    def test_cook_creation(self):
        cook = get_user_model().objects.create_user(
            username="testcook",
            first_name="Test",
            last_name="Cook",
            password="testpass123",
            experience=5,
        )
        self.assertEqual(cook.username, "testcook")
        self.assertEqual(cook.first_name, "Test")
        self.assertEqual(cook.last_name, "Cook")
        self.assertEqual(cook.experience, 5)
        self.assertEqual(str(cook), "Test, Cook, 5")


class IngredientModelTest(TestCase):
    def test_ingredient_creation(self):
        ingredient = Ingredient.objects.create(name="Test Ingredient")
        self.assertEqual(ingredient.name, "Test Ingredient")
        self.assertEqual(str(ingredient), "Test Ingredient")


class DishModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(dish_type="sushi")
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")

    def test_dish_creation(self):
        dish = Dish.objects.create(
            name="Test Dish",
            price=10.99,
            cooking_time=30.0,
            spicy="easy",
            category=self.category,
            difficulty="easy",
            recipe="Test recipe",
        )
        dish.ingredients.add(self.ingredient)
        self.assertEqual(dish.name, "Test Dish")
        self.assertEqual(dish.price, 10.99)
        self.assertEqual(dish.cooking_time, 30.0)
        self.assertEqual(dish.spicy, "easy")
        self.assertEqual(dish.category, self.category)
        self.assertEqual(dish.difficulty, "easy")
        self.assertEqual(dish.recipe, "Test recipe")
        self.assertEqual(dish.ingredients.first(), self.ingredient)
        self.assertEqual(str(dish), "Test Dish, price: (10.99)")


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(dish_type="sushi")
        self.dish = Dish.objects.create(
            name="Test Dish",
            price=10.99,
            cooking_time=30.0,
            spicy="easy",
            category=self.category,
            difficulty="easy",
            recipe="Test recipe",
        )

    def test_review_creation(self):
        review = Review.objects.create(
            dish=self.dish,
            left_by=self.user,
            content="Test review content",
            created_at=timezone.now(),
        )
        self.assertEqual(review.dish, self.dish)
        self.assertEqual(review.left_by, self.user)
        self.assertEqual(review.content, "Test review content")
        self.assertEqual(str(review), f"{self.dish}, {self.user}")
