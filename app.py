import os
import requests
from data_manager import DataManager
from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv
from models import db, Movie

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models
data_manager = DataManager() # Create an object of your DataManager class


def get_movie_content(movie, user_id):
    """Takes a movie title from a user wish, search over API for the
    informations and return the movie object"""
    url = f"http://www.omdbapi.com/"
    params = {
        "apikey": API_KEY,
        "t": movie
    }
    try:
        response = requests.get(url, params=params)
        movie_content = response.json()
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
                           content=content,
                           user_id=user_id)
    except Exception as e:
        app.logger.error(f"API Fehler: {e}")
        return None
    return new_movie

@app.route('/')
def index():
    """Die Startseite deiner Anwendung. Zeigt eine Liste aller registrierten Nutzer und ein
    Formular zum Hinzufügen neuer Nutzer. (Diese Route verwendet standardmäßig GET."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/create_user', methods=['POST'])
def create_user():
    """Wenn der Nutzer das „Nutzer hinzufügen“-Formular abschickt, wird eine POST-Anfrage ausgelöst.
    Der Server erhält die neuen Nutzerdaten, fügt sie der Datenbank hinzu und leitet dann zurück zu /.
    """
    new_user = request.form.get('title')
    if new_user == "" or new_user.strip() == "":
        return redirect(url_for('index'))
    data_manager.create_user(new_user)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    """Wenn du auf einen Nutzernamen klickst, ruft die App die Liste der
    Lieblingsfilme dieses Nutzers ab und zeigt sie an."""
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Fügt einen neuen Film zur Favoritenliste eines Nutzers hinzu."""
    response = request.form.get('new_title')
    new_movie = get_movie_content(response, user_id)
    if not new_movie:
        return redirect(url_for('list_movies', user_id=user_id))
    data_manager.add_movie(new_movie)
    return redirect(url_for('list_movies', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_title(user_id, movie_id):
    """Den Titel eines bestimmten Films in der Liste eines Nutzers ändern,
    ohne sich auf OMDb für Korrekturen zu verlassen."""
    updated_title = request.form.get('update_title')
    data_manager.update_movie(movie_id, updated_title)
    return redirect(url_for('list_movies', movie_id=movie_id, user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Entfernt einen bestimmten Film aus der Liste der Lieblingsfilme eines Nutzers."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_movies', movie_id=movie_id, user_id=user_id))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Entfernt einen bestimmten Film aus der Liste der Lieblingsfilme eines Nutzers."""
    data_manager.delete_user(user_id)
    return redirect(url_for('index', user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f"404 Not Found: {e}")
    return render_template('404.html'), 404

@app.errorhandler(403)
def no_access(e):
    app.logger.error(f"Access Error: {e}")
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Server Error: {e}")
    return render_template('500.html'), 500


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)
