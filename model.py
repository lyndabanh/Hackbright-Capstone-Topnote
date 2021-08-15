"""Models for wine cellar app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    email = db.Column (db.String, unique=True)
    password = db.Column (db.String)
    quote = db.Column (db.String)

    ratings = db.relationship('Rating')
    favorites = db.relationship('Favorite')
    comments = db.relationship('Comment')

    def to_dict(self):
        return {'user_id' : self.user_id,
                'name' : self.name,
                'email' : self.email,
                'password' : self.password}

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Wine(db.Model):
    """A wine."""

    __tablename__ = 'wines'

    wine_id = db.Column (db.Integer, autoincrement=True, primary_key=True)
    title = db.Column (db.String)
    winery = db.Column (db.String)
    variety = db.Column (db.String)
    country = db.Column (db.String)
    description = db.Column (db.String)
    designation = db.Column (db.String)
    points = db.Column (db.Integer)
    province = db.Column (db.String)
    region_1 = db.Column (db.String, nullable=True)
    region_2 = db.Column (db.String, nullable=True)

    ratings = db.relationship('Rating')
    favorites = db.relationship('Favorite')
    comments = db.relationship('Comment')

    def to_dict(self):
        return {'wine_id' : self.wine_id,
                'winery' : self.winery,
                'variety' : self.variety,
                'country' : self.country,
                'description' : self.description,
                'designation' : self.designation,
                'points' : self.points,
                'province' : self.province,
                'region_1' : self.region_1,
                'region_2' : self. region_2}

    def __repr__(self):
        return f'<Wine wine_id={self.wine_id} title={self.title}>'
    

class Rating(db.Model):
    """A user's wine rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column (db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column (db.Integer, db.ForeignKey('users.user_id'))
    wine_id = db.Column (db.Integer, db.ForeignKey('wines.wine_id'))
    rating = db.Column (db.Integer)
    date = db.Column (db.DateTime, default=(date.today()).strftime("%B %d, %Y"))

    user = db.relationship('User')
    wine = db.relationship('Wine')

    def to_dict(self):
        return {'rating_id' : self.rating_id,
                'user_id' : self.user_id,
                'wine_id' : self.wine_id,
                'rating' : self.rating,
                'rating_date' : self.date}

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} rating={self.rating} user_id={self.user_id} wine_id={self.wine_id}>'


class Favorite(db.Model):
    """A user's favorited wine."""

    __tablename__ = 'favorites'

    favorite_id = db.Column (db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column (db.Integer, db.ForeignKey('users.user_id'))
    wine_id = db.Column (db.Integer, db.ForeignKey('wines.wine_id'))
    #favorite = db.Column (db.String)

    user = db.relationship('User')
    wine = db.relationship('Wine')

    def to_dict(self):
        return {'favorite_id' : self.favorite_id,
                'user_id' : self.user_id,
                'wine_id' : self.wine_id,
                'wine.country' : self.wine.country}


    def __repr__(self):
        return f'<Favorite favorite_id={self.favorite_id} user_id={self.user_id}, wine_id={self.wine_id}>'


class Comment(db.Model):
    """User's comment about a wine."""

    __tablename__ = 'comments'

    comment_id = db.Column (db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column (db.Integer, db.ForeignKey('users.user_id'))
    wine_id = db.Column (db.Integer, db.ForeignKey('wines.wine_id'))
    comment = db.Column (db.String)

    user = db.relationship('User')
    wine = db.relationship('Wine')

    def to_dict(self):
        return {'comment_id' : self.comment_id,
                'user_id' : self.user_id,
                'wine_id' : self.wine_id,
                'comment' : self.comment}

    def __repr__(self):
        return f'<Comment comment_id={self.comment_id} comment={self.comment}>'


def connect_to_db(flask_app, db_uri='postgresql:///mycellar', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)



