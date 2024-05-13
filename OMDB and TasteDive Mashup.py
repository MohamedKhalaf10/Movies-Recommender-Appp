# check 24.14 for project description

######################################################################## Module Imports #######################################################
import requests
import json
######################################################################## Functions Defenitions ################################################
def get_movies_from_tastedive(movie: str) -> dict:
    ''' Get info about a movie from TasteDive API '''
    baseURL = "https://tastedive.com/api/similar"
    params = {
        "q" : movie,
        "type" : "movies",
        "limit" : 5,
        "k" : "Api Key"
    }

    return requests.get(baseURL, params=params).json()

def extract_movie_titles(data: str) -> list:
    ''' Extracts the list of movie '''
    return [result['Name'] for result in data['Similar']['Results']]

def get_related_titles(movies: list) -> dict:
    ''' Gets five related movies for each movie title from TasteDive '''
    result = []
    for movie in movies:
        data = extract_movie_titles(get_movies_from_tastedive(movie))
        data = [movieTitle for movieTitle in data if movieTitle not in result]
        result = result + data
    return result

def get_movie_data(movie: str) -> dict:
    "Get info from OMBD API about a moive"
    baseURL = "http://www.omdbapi.com/"
    params = {
        "apikey" : "Api Key",
        "t" : movie,
        "type" : "movie"
    }
    return requests.get(baseURL, params).json()

def get_movie_rating(OMBD_dict: dict) -> int:
    ''' takes an OMDB dictionary result for one movie and extracts the Rotten Tomatoes rating as an integer '''
    result = 0
    for rating in OMBD_dict['Ratings']:
        if rating['Source'] == 'Rotten Tomatoes':
           result = int(rating['Value'].replace("%", ""))
    return result            
           
def get_sorted_recommendations(movies: list) -> list:
    relatedList = get_related_titles(movies)
    return sorted(relatedList, key = lambda movie: (get_movie_rating(get_movie_data(movie)), movie), reverse = True)