"""CRUD operations."""

from model import db, User, Wine, Rating, Favorite, Comment, connect_to_db
from sqlalchemy import func


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


def update_rating(user, wine, rating):
    """User updates a previously rated wine."""

    #query for the object (user and wine_id)
    current_rating = Rating.query.filter(Rating.user==user, Rating.wine==wine).first()
    #reassign the rating attribute of that rating
    current_rating.rating = rating
    #then potentially need to: commit, may need to add to session before committing
    db.session.merge(current_rating)
    db.session.commit()

    return current_rating


def favorite(user, wine):
    """Create and add a favorite wine."""

    favorite = Favorite(user=user, wine=wine)

    db.session.add(favorite)
    db.session.commit()

    return favorite


def comment(user, wine, comment):
    """Crate and add a wine comment."""

    comment = Comment(user=user, wine=wine, comment=comment)

    db.session.add(comment)
    db.session.commit()

    return comment


#wine queries
def all_wines():
    return Wine.query.all()


def get_wine_by_id(wine_id):
    return Wine.query.filter(Wine.wine_id==wine_id).first()


def get_and_order_rating_by_wine_id(wine_id):
    return Rating.query.filter(Rating.wine_id==wine_id).order_by(Rating.rating.desc()).all()


# def get_group_count_rating_by_user_id(user_id):
#     return Rating.query(Rating.rating, func.count(Rating.rating)).filter(Rating.user_id==user_id).group_by(Rating.rating).all()


#user queries
def all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.filter(User.user_id==user_id).first()


def get_user_by_email(email):
    return User.query.filter(User.email==email).first()


#rating queries
def all_ratings():
    return Rating.query.all()


def get_ratings_by_wine_id(wine_id):
    return Rating.query.filter(Rating.wine_id==wine_id).all()


def get_rating_by_user_id(user_id):    
    return Rating.query.filter(Rating.user_id==user_id).first()


def get_rating_by_user_id_and_wine_id(user_id, wine_id):
    return Rating.query.filter(Rating.user_id==user_id, Rating.wine_id==wine_id).all() 
  

#favorite queries
def get_favorites_by_wine_id(wine_id):
    return Favorite.query.filter(Favorite.wine_id==wine_id).all()


def get_favorites_by_user_id(user_id): 
    return Favorite.query.filter(Favorite.user_id==user_id).all()


def get_dict_of_countries_of_favorites_by_user_id(user_id): 
    fav_wines = Favorite.query.filter(Favorite.user_id==user_id).all()
    
    freq = {}
    for fav in fav_wines:
        if fav.wine.country in freq:
            freq[fav.wine.country]["num_fav"] += 1
        else:
            freq[fav.wine.country] = {
                                        "country" : fav.wine.country,
                                        "num_fav" : 1
                                    }
                                               
    list_of_freq = []
    for item in freq:
        list_of_freq.append(freq[item])

    return list_of_freq


def get_most_favorited_countries(user_id):
    fav_wines = Favorite.query.filter(Favorite.user_id==user_id).all()

    freq = {}
    for fav in fav_wines:
        if fav.wine.country in freq:
            freq[fav.wine.country] += 1
        else:
            freq[fav.wine.country] = 1

    print(freq) 

    print (freq.values())
    print(freq.keys())
    print (freq.items())

    #iterate through the key-value pairs in the freq dictionary
    #next we convert the value v into a float(v) and check if that float is equal to max value
    #if that is the case, we add the key k to the list
    return [k for k,v in freq.items() if float(v) == max(freq.values())]

    #could practice with querying for this data instead. joins and stuff
    #order by num of favorites


def get_wines_by_country(country):
    return Wine.query.filter(Wine.country==country).all()


# def test():
#     fav_countries = get_most_favorited_countries(1)
#     num_favs = len(fav_countries)
#     print(fav_countries)
#     print(num_favs)

#     for country in range(num_favs):

#     wines = []
#     print(len(wines))
#     for country in fav_countries:
#         print(country)
#         wines_of_country = Wine.query.filter(Wine.country==country).all()
#         print(len(wines_of_country))

#         #BUG: This adds the entire list, not each item. So for 2 countries, one list from each country is added.
#         wines.append(wines_of_country)
#         print(len(wines))
        

    

    
    

# def get_count_of_favorite_countries_by_user_id():
#     return Favorite.query(Favorite.wine.country, func.count(Favorite.wine.country)).group_by(Favorite.wine.country).all()


# def get_favorites_by_userid_and_country(user_id, country):

#     users_favorites = Favorite.query.filter(Favorite.user_id==user_id).all()

#     for fav in users_favorites:
#         print(fav.wine)
#         print(fav.wine.country)

#         if == country:

    

# def get_ratings_by_user_id(user_id):  
#     return Rating.query.filter(Rating.user_id==user_id).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

