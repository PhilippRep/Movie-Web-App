from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User(id = {self.id}, title = {self.name})"

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=True)
    director = db.Column(db.String, nullable=True)
    rating = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String, nullable=True)
    content = db.Column(db.Text, nullable= True)
    poster = db.Column(db.String, nullable=False, default="/static/no-poster.png")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='movies')

    def __repr__(self):
        return f"Movie(id = {self.id}, title = {self.title})"
