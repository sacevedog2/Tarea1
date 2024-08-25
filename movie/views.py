from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
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

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    
    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}
    
    # Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
    
    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))
    
    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    
    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    
    #Guardar la grafica en un objeto BytesIO
    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png1 = buffer1.getvalue()
    buffer1.close()
    graphic = base64.b64encode(image_png1)
    graphic = graphic.decode('utf-8')

    # Crear un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_genre = {}
    
    # Filtrar las películas por género y contar la cantidad de películas por el primer género
    for movie in all_movies:
        genre = movie.genre.split(',')[0].strip() if movie.genre else "None"
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1

    # Posiciones de las barras para el gráfico de géneros
    genre_bar_positions = range(len(movie_counts_by_genre))
    
    # Crear la gráfica de barras para géneros
    plt.bar(genre_bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    
    # Personalizar la gráfica de géneros
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(genre_bar_positions, movie_counts_by_genre.keys(), rotation=90)
    
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica en un objeto BytesIO separado
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()

    # Convertir la gráfica de géneros a base64
    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic2 = base64.b64encode(image_png2)
    graphic2 = graphic2.decode('utf-8')

    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {'graphic': graphic, 'graphic2': graphic2})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})
