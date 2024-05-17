from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .forms import DishSearchForm
from .models import Category, Dish


def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.annotate(dish_count=Count('dishes')).order_by(
        'dish_type'
    )
    context = {
        'categories': categories
    }
    return render(request, 'tasty_ideas/index.html', context)


class DishListView(generic.ListView):
    model = Dish
    template_name = 'tasty_ideas/dish_list.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return Dish.objects.prefetch_related().filter(
                category_id=self.kwargs['pk'], name__icontains=name)
        return Dish.objects.prefetch_related().filter(
            category_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        context["search_form"] = DishSearchForm()
        return context


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = 'tasty_ideas/dish_detail.html'
    context_object_name = 'dish'
