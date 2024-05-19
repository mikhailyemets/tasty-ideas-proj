from django.urls import path
from .views import index, DishListView, DishDetailView, DishCreateView, DishUpdateView, DishDeleteView, delete_review





urlpatterns = [
    path("", index, name="index"),
    path("tasty-ideas/", index, name="index"),
    path('categories/<int:pk>/', DishListView.as_view(), name='dish-list'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path("categories/<int:pk>/dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path('dishes/<int:pk>/update/', DishUpdateView.as_view(), name='dish-update'),
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(), name='dish-delete'),
    path('review/<int:pk>/delete/', delete_review, name='delete_review'),
]

app_name = "tasty_ideas"
