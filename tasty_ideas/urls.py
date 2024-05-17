from django.urls import path
from .views import index, DishListView, DishDetailView


urlpatterns = [
    path("", index, name="index"),
    path("tasty-ideas/", index, name="index"),
    path('categories/<int:pk>/', DishListView.as_view(), name='dish-list'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
]

app_name = "tasty_ideas"
