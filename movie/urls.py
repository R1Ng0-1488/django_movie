from django.urls import path

from . import views

app_name = 'movie'
urlpatterns = [
    path('', views.MoviesView.as_view(), name='movies'),
    path('filter/', views.FilterMovies.as_view(), name='filter'),
    path('search/', views.Search.as_view(), name='search'),
    path('add_rating/', views.AddStarRating.as_view(), name='add_rating'),
    path('<slug:slug>/', views.MoviesDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('actors/<str:slug>/', views.ActorView.as_view(), name='actor_detail'),
]
