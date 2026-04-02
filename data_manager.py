from sqlalchemy.util import method_is_overridden

from models import db, User, Movie


class DataManager():
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        all_users = User.query.all()
        return all_users

    def get_movies(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return []
        return user.movies

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.title = new_title
        db.session.commit()

    def delete_movie(self, movie_id):
        movie_to_delete = Movie.query.get(movie_id)
        db.session.delete(movie_to_delete)
        db.session.commit()
