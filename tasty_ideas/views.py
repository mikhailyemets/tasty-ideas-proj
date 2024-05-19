from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import DishSearchForm, CookCreateForm, DishForm
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
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get("query")

        queryset = Dish.objects.filter(
            category_id=self.kwargs['pk']
        ).annotate(review_count=Count('reviews')).prefetch_related(
            'ingredients'
        )

        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) |
                models.Q(ingredients__name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = DishSearchForm(self.request.GET or None)
        context["category_pk"] = self.kwargs['pk']
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
        context["reviews"] = Review.objects.filter(dish=self.object)
        context["user"] = self.request.user
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


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "tasty_ideas/dish_list_form.html"

    def get_success_url(self):
        return reverse_lazy("tasty_ideas:dish-list",
                            kwargs={"pk": self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_view'] = False
        context['category_pk'] = self.kwargs['pk']
        return context


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "tasty_ideas/dish_list_form.html"

    def get_success_url(self):
        return reverse("tasty_ideas:dish-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update_view'] = True
        context['category_pk'] = self.kwargs.get('pk', None)
        return context


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "tasty_ideas/dish_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("tasty_ideas:dish-list",
                            kwargs={"pk": self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_pk'] = self.kwargs.get('pk', None)
        return context


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.left_by:
        review.delete()
    return redirect(reverse('tasty_ideas:dish-detail', kwargs={'pk': review.dish.pk}))
