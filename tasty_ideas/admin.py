from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from tasty_ideas.models import Cook, Category, Dish, Ingredient, Review


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("experience",)
    fieldsets = (
        *UserAdmin.fieldsets,
        (None, {'fields': ('experience',)}),
    )
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (None, {
            'classes': ('wide',),
            'fields': (
            'first_name', 'last_name',
            'experience'),
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name", ]
    list_filter = ["dish_type", ]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ["name", ]
    list_filter = ["category", "price", "cooking_time", ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ["left_by", ]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name", ]


admin.site.unregister(Group)

