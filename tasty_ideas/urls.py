from django.urls import path
from .views import IndexView, DishListView, DishDetailView, DishCreateView, DishUpdateView, DishDeleteView, delete_review, user_profile





urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasty-ideas/", IndexView.as_view(), name="index"),
    path('categories/<int:pk>/', DishListView.as_view(), name='dish-list'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path("categories/<int:pk>/dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path('dishes/<int:pk>/update/', DishUpdateView.as_view(), name='dish-update'),
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(), name='dish-delete'),
    path('review/<int:pk>/delete/', delete_review, name='delete_review'),
    path('profile/', user_profile, name='user_profile'),
]


app_name = "tasty_ideas"
