from .models import Category, Movies, Genre
#
# def categories(request):
#     return {'categories': Category.objects.all()}
#
# def last_movies(request):
#     return {'last_movies': Movies.objects.order_by('-id')[4]}

class MoviesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response, count=4):
        response.context_data['categories'] = Category.objects.all()
        response.context_data['last_movies'] = Movies.objects.order_by('-id')[:count]
        response.context_data['genres'] = Genre.objects.all()
        return response

def movies_middleware(request, count=4):
    context = {}
    context['categories'] = Category.objects.all()
    context['last_movies'] = Movies.objects.order_by('-id')[:count]
    context['genres'] = Genre.objects.all()
    context['years'] = Movies.objects.filter(draft=False).values('year')
    return context
