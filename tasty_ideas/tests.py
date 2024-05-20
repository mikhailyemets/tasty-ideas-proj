from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Category, Dish, Review, Ingredient
from .views import CommentaryForm
from tasty_ideas.forms import (
    MainPageSearchForm,
    DishSearchForm,
    CookCreateForm,
    CookForm,
    DishForm,
)

# --------- TEST VIEWS  ---------


class DishListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(dish_type="Test Dish Type")
        cls.dish1 = Dish.objects.create(
            name="Test Dish 1",
            price=10.99,
            cooking_time=30,
            spicy="easy",
            category=cls.category,
            difficulty="easy",
            recipe="Test recipe 1",
        )
        cls.dish2 = Dish.objects.create(
            name="Test Dish 2",
            price=12.99,
            cooking_time=45,
            spicy="medium",
            category=cls.category,
            difficulty="medium",
            recipe="Test recipe 2",
        )

    def test_dish_list_view_with_search_query(self):
        search_query = "Test Dish 1"
        response = self.client.get(
            reverse("tasty_ideas:dish-list", kwargs={"pk": self.category.pk}),
            {"query": search_query},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, search_query)
        self.assertNotContains(response, self.dish2.name)

    def test_dish_list_view_without_results(self):
        search_query = "Non-existing Dish"
        response = self.client.get(
            reverse("tasty_ideas:dish-list", kwargs={"pk": self.category.pk}),
            {"query": search_query},
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["dishes"], [])

    def test_dish_list_view_no_pagination_if_less_than_3(self):
        response = self.client.get(
            reverse("tasty_ideas:dish-list", kwargs={"pk": self.category.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["dishes"]), 2)

    def test_dish_list_view_pagination_if_greater_then_2(self):
        dish3 = Dish.objects.create(
            name="Test Dish 3",
            price=15.99,
            cooking_time=60,
            spicy="hot",
            category=self.category,
            difficulty="hard",
            recipe="Test recipe 3",
        )

        response = self.client.get(
            reverse("tasty_ideas:dish-list", kwargs={"pk": self.category.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["dishes"]), 2)


class DishDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(dish_type="Test Dish Type")
        cls.dish = Dish.objects.create(
            name="Test Dish",
            price=10.99,
            cooking_time=30,
            spicy="easy",
            category=cls.category,
            difficulty="easy",
            recipe="Test recipe",
        )

    def test_dish_detail_view(self):
        response = self.client.get(
            reverse("tasty_ideas:dish-detail", kwargs={"pk": self.dish.pk})
        )
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.dish.name)
        self.assertContains(response, self.dish.price)

    def test_dish_detail_view_with_invalid_dish_id(self):
        invalid_dish_id = 99999
        response = self.client.get(
            reverse("tasty_ideas:dish-detail", kwargs={"pk": invalid_dish_id})
        )
        self.assertEqual(response.status_code, 404)

    def test_dish_detail_view_comment_form(self):
        response = self.client.get(
            reverse("tasty_ideas:dish-detail", kwargs={"pk": self.dish.pk})
        )
        self.assertEqual(response.status_code, 200)

        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], CommentaryForm)

    def test_dish_detail_view_reviews(self):
        Review.objects.create(
            dish=self.dish,
            left_by=get_user_model().objects.create(username="user1"),
            content="Review 1",
        )
        Review.objects.create(
            dish=self.dish,
            left_by=get_user_model().objects.create(username="user2"),
            content="Review 2",
        )

        response = self.client.get(
            reverse("tasty_ideas:dish-detail", kwargs={"pk": self.dish.pk})
        )
        self.assertEqual(response.status_code, 200)

        self.assertTrue("reviews" in response.context)
        self.assertEqual(len(response.context["reviews"]), 2)

    def test_dish_detail_view_add_review(self):
        user = get_user_model().objects.create(username="test_user")
        self.client.force_login(user)

        response = self.client.post(
            reverse("tasty_ideas:dish-detail", kwargs={"pk": self.dish.pk}),
            {"content": "New review content"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().content, "New review content")


class DishCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(dish_type="Test Dish Type")
        cls.user = get_user_model().objects.create_user(
            username="test_user", password="testpassword"
        )

    def test_dish_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("tasty_ideas:dish-create", kwargs={"pk": self.category.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertEqual(response.context["category_pk"], self.category.pk)


class DishUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(dish_type="Test Dish Type")
        cls.dish = Dish.objects.create(
            name="Test Dish",
            price=10.99,
            cooking_time=30,
            spicy="easy",
            category=cls.category,
            difficulty="easy",
            recipe="Test recipe",
        )
        cls.user = get_user_model().objects.create_user(
            username="test_user", password="testpassword"
        )

    def test_dish_update_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("tasty_ideas:dish-update", kwargs={"pk": self.dish.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertEqual(response.context["is_update_view"], True)
        self.assertEqual(response.context["category_pk"], self.category.pk)

    def test_dish_update_view_redirect_when_not_authenticated(self):
        data = {
            "name": "Updated Test Dish",
            "price": 15.99,
            "cooking_time": 60,
            "spicy": "hot",
            "difficulty": "hard",
            "recipe": "Updated recipe",
        }
        response = self.client.post(
            reverse("tasty_ideas:dish-update", kwargs={"pk": self.dish.pk}), data
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)


class DishDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(dish_type="Test Dish Type")
        cls.dish = Dish.objects.create(
            name="Test Dish",
            price=10.99,
            cooking_time=30,
            spicy="easy",
            category=cls.category,
            difficulty="easy",
            recipe="Test recipe",
        )
        cls.user = get_user_model().objects.create_user(
            username="test_user", password="testpassword"
        )

    def test_dish_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("tasty_ideas:dish-delete", kwargs={"pk": self.dish.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("dish" in response.context)
        self.assertEqual(response.context["dish"], self.dish)

    def test_dish_delete_view_post(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("tasty_ideas:dish-delete", kwargs={"pk": self.dish.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dish.objects.count(), 0)


class DeleteReviewViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test_user")
        self.category = Category.objects.create(dish_type="Test Dish Type")
        self.dish = Dish.objects.create(
            name="Test Dish",
            price=10.99,
            spicy="easy",
            cooking_time=5,
            category=self.category,
            difficulty="easy",
            recipe="Test recipe",
        )
        self.review = Review.objects.create(
            dish=self.dish, left_by=self.user, content="Test Review"
        )

    def test_delete_review_by_anonymous_user(self):
        self.client.logout()
        response = self.client.post(
            reverse("tasty_ideas:delete_review", kwargs={"pk": self.review.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)

    def test_delete_review_with_invalid_review_id(self):
        self.client.force_login(self.user)
        invalid_review_id = 99999
        response = self.client.post(
            reverse("tasty_ideas:delete_review", kwargs={"pk": invalid_review_id})
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Review.objects.count(), 1)


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="testpassword",
        )

    def test_user_profile_view_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasty_ideas:user_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasty_ideas/user_profile.html")
        self.assertTrue("form" in response.context)
        self.assertTrue("user" in response.context)
        self.assertEqual(response.context["user"], self.user)

    def test_user_profile_view_redirect_for_anonymous_user(self):
        response = self.client.get(reverse("tasty_ideas:user_profile"))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_form_submission(self):
        self.client.force_login(self.user)
        new_username = "new_test_user"
        response = self.client.post(
            reverse("tasty_ideas:user_profile"),
            {
                "username": new_username,
                "first_name": "New",
                "last_name": "User",
                "password1": "newpassword",
                "password2": "newpassword",
                "email": "newtest@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            get_user_model().objects.get(id=self.user.id).username, new_username
        )
        self.assertEqual(
            get_user_model().objects.get(id=self.user.id).first_name, "New"
        )

    def test_user_profile_invalid_form_submission(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("tasty_ideas:user_profile"),
            {
                "username": "",
                "first_name": "New",
                "last_name": "User",
                "password1": "newpassword",
                "password2": "newpassword",
                "email": "newtest@example.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertTrue("username" in form.errors)
        self.assertEqual(form.errors["username"], ["This field is required."])


# --------- TEST MODELS  ---------


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


# --------- TEST FORMS  ---------


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
