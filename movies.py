import requests

API_KEY = "76fd86b44934594733709734a733a559"

URL = "https://api.themoviedb.org/3/search/movie?"


API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NmZkODZiNDQ5MzQ1OTQ3MzM3MDk3MzRhNzMzYTU1OSIsInN1YiI6IjYyNjBhNGFkM2Q3NDU0MTVhNzI2MGNmOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4HBVBHQH9e0ksbSIAB6uMbWq1A3Rmf35CXtOoqnfAyQ"


def search_movie(title):
    params = {
        "api_key": "76fd86b44934594733709734a733a559",
        "query":title
    }

    response = requests.get(URL, params=params)
    movies = response.json()
    return movies['results']


def get_movie_detail(id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key=76fd86b44934594733709734a733a559')
    movie = response.json()
    return [movie['original_title'],f'https://image.tmdb.org/t/p/w500/{movie["poster_path"]}',movie['release_date'][:4],movie['overview']]
