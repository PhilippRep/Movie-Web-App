import os
import requests
from data_manager import DataManager
from flask import Flask
from dotenv import load_dotenv
from models import db, Movie

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models
#data_manager = DataManager() # Create an object of your DataManager class


def get_movie_content(movie):
    """Takes a movie title from a user wish, search over API for the
    informations and return the movie object"""
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&"
    params = {
        "t": movie
    }
    response = requests.get(url, params=params)
    movie_content = response.json()
    print(movie_content)
    title = movie_content['Title']
    year = int(movie_content['Year'])
    director = movie_content['Director']
    poster = movie_content['Poster']
    rating = float(movie_content['imdbRating'])
    genre =  movie_content['Genre']
    content = movie_content['Plot']
    new_movie = Movie(title=title,
                       year=year,
                       director=director,
                       poster=poster,
                       rating=rating,
                       genre=genre,
                       content=content)
    data_manager = DataManager()
    data_manager.add_movie(new_movie)


def main():
    """controls die programm"""
    user_wish = input("Which Movie do you want to add? ")
    get_movie_content(user_wish)


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run()
  main()
