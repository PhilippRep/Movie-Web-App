from models import db, User, Movie


class DataManager():
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_user(self):
        all_users = User.query.all()
        return all_users

    def get_movies(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return []
        return user.movies

    def add_movie(self, movie):
