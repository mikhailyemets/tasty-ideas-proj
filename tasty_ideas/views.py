from django.contrib import messages
from django import forms
from django.db import models
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import DishSearchForm, CookCreateForm
from .models import Category, Dish, Review


def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'tasty_ideas/index.html', context)


class DishListView(generic.ListView):
    model = Dish
    template_name = 'tasty_ideas/dish_list.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        query = self.request.GET.get("query")

        queryset = Dish.objects.prefetch_related().filter(category_id=self.kwargs['pk'])

        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) |
                models.Q(ingredients__name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        context["search_form"] = DishSearchForm()
        return context


class CommentaryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = 'tasty_ideas/dish_detail.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentaryForm()
        context['reviews'] = self.object.reviews.all()
        context['category_id'] = self.object.category.id
        context['next'] = self.request.path
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            form = CommentaryForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                new_review = Review.objects.create(
                    left_by=request.user,
                    dish=self.object,
                    content=content
                )
                return redirect('tasty_ideas:dish-detail', pk=self.object.pk)
            else:
                messages.error(request, "Please provide a valid review.")
        else:
            messages.error(request, "Please log in before adding reviews.")
        return redirect('tasty_ideas:dish-detail', pk=self.object.pk)


class SignUpView(generic.CreateView):
    form_class = CookCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
