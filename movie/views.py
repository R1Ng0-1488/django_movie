from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView, View
from django.db.models import Q

from .models import Movies, Category, Actor, Genre, Rating
from .forms import ReviewsForm, RatingForm
# Create your views here.
class MoviesView(ListView):
    """Вывод фильмов"""
    queryset = Movies.objects.filter(draft=False)
    paginate_by = 1

class MoviesDetailView(DetailView):
    """Детали фильма"""
    model = Movies
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewsForm()
        return context


class AddReview(View):
    """Отправка отзывов"""
    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        movie = Movies.objects.get(pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(DetailView):
    """Вывод деталей актера"""
    model = Actor
    slug_field = 'name'



class FilterMovies(ListView):
    """Фильтрует фильмы"""
    paginate_by = 1

    def get_queryset(self):
        queryset = Movies.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genre__in=self.request.GET.getlist('genre'))
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context['genre'] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class AddStarRating(View):
    def get_client_ip(self, request):
        x = request.META.get('HTTP_X_FORWARDED_FOR')
        if x:
            ip = x.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск"""
    paginate_by = 1

    def get_queryset(self):
        return Movies.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        return context
