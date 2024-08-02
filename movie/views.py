from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
# Create your views here.

def home(request):
    #return HttpResponse('Hello, World!')
    #return render(request, 'home.html' , {'name': 'Sebastian'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies, 'name': 'Sebastian'})

def about(request):
    #return HttpResponse('About page')
    return render(request, 'about.html')
