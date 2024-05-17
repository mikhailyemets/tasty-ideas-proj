from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    DISH_TYPES = [
        ("sushi", "sushi rolls"),
        ("nigiri", "nigiri"),
        ("sashimi", "sashimi"),
        ("salad", "salads"),
        ("soup", "soups"),
    ]
    dish_type = models.CharField(max_length=50, choices=DISH_TYPES)
    image = models.URLField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("dish_type",)

    def __str__(self):
        return self.dish_type


class Cook(AbstractUser):
    experience = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        ordering = ("first_name",)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}, {self.experience}"


class Dish(models.Model):
    SPICY_CHOICES = [
        ("easy", "Not spicy at all"),
        ("medium", "Can be a little spicy"),
        ("hot", "Spicy as hell"),
    ]
    DIFFICULTY_CHOICES = [
        ("easy", "Easy to make"),
        ("medium", "Required some skills"),
        ("hard", "Required skills and a lot of time"),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cooking_time = models.DecimalField(max_digits=8, decimal_places=2)
    spicy = models.CharField(max_length=50, choices=SPICY_CHOICES)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)
    ingredients = models.ManyToManyField(
        "Ingredient",
        related_name="dishes"
    )
    recipe = models.TextField()
    image = models.URLField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Dishes"
        ordering = ("difficulty",)

    def __str__(self):
        return f"{self.name}, price: ({self.price})"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Review(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    left_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("left_by",)

    def __str__(self):
        return f"{self.dish}, {self.left_by}"