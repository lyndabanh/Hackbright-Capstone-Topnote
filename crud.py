"""CRUD operations."""

from model import db, User, Wine, Rating, Favorite, Comment, connect_to_db


def create_user(name, email, password):
    """Create and return a new user."""

    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def create_wine(title, winery, variety, country, description, designation, points, province, region_1, region_2):
    """Create and return a new wine."""

    wine = Wine(title=title,
                winery=winery,
                variety=variety,
                country=country,
                description=description,
                designation=designation,
                points=points,
                province=province,
                region_1=region_1,
                region_2=region_2)
    
    db.session.add(wine)
    db.session.commit()

    return wine


def rating(user, wine, rating):
    """Create and return a new rating."""

    rating = Rating(user=user, wine=wine, rating=rating)
    #rating = Rating(user_id=user_id, wine_id=wine_id, rating_id=rating_id)
    #above, can do that instead of passing object

    db.session.add(rating)
    db.session.commit()

    return rating


def favorite(user, wine, favorite):
    """Create and add a favorite wine."""

    favorite = Favorite(user=user, wine=wine, favorite=favorite)

    db.session.add(favorite)
    db.session.commit()

    return favorite


def comment(user, wine, comment):
    """Crate and add a wine comment."""

    comment = Comment(user=user, wine=wine, comment=comment)

    db.session.add(comment)
    db.session.commit()

    return comment


def all_wines():

    return Wine.query.all()


def get_wine_by_id(wine_id):

    return Wine.query.filter(Wine.wine_id==wine_id).first()


def all_users():

    return User.query.all()


def get_user_by_id(user_id):

    return User.query.filter(User.user_id==user_id).first()


def get_user_by_email(email):

    return User.query.filter(User.email==email).first()


def all_ratings():

    return Rating.query.all()


def get_ratings_by_wine_id(wine_id):

    return Rating.query.filter(Rating.wine_id==wine_id).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

