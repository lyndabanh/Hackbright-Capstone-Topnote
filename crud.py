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


def comment(user, wine, comment):
    """Create and return a new comment."""

    comment = Comment(user=user, wine=wine, comment=comment)

    db.session.add(comment)
    db.session.commit()

    return comment


def update_comment(user, wine, comment):
    """User updates a previously created comment."""

    current_comment = Comment.query.filter(Comment.user==user, Comment.wine==wine).first()

    #Conditional allows you to "update" a comment even if a previous comment doesn't exist
    if current_comment:
        current_comment.comment = comment
        db.session.merge(current_comment)
    else:
        current_comment = Comment(user=user, wine=wine, comment=comment)

    db.session.commit()

    return current_comment


def get_comments_by_user_id(user_id):
    return Comment.query.filter(Comment.user_id==user_id).all()


def favorite(user, wine):
    """Create and add a favorite wine."""

    favorite = Favorite(user=user, wine=wine)

    db.session.add(favorite)
    db.session.commit()

    # return favorite


def unfavorite(user_id, wine_id):
    """Remove favorited wine ('unfavorite')."""

    # favorite = Favorite.query.get(user_id, wine_id)
    favorite = Favorite.query.filter(Favorite.user_id==user_id, Favorite.wine_id==wine_id).delete() 
    db.session.commit()
    


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

#is this used anywhere? should be ratings by user id (plural)
def get_rating_by_user_id(user_id):    
    return Rating.query.filter(Rating.user_id==user_id).first()


def get_rating_by_user_id_and_wine_id(user_id, wine_id):
    return Rating.query.filter(Rating.user_id==user_id, Rating.wine_id==wine_id).all() 
  

#favorite queries
def get_favorites_by_wine_id(wine_id):
    return Favorite.query.filter(Favorite.wine_id==wine_id).all()
    #likely returning a string
    # res = Favorite.query.filter(Favorite.wine_id==wine_id).all()

    # if type(res) is str:
    #     res = [res]
    # return res


def get_favorites_by_user_id(user_id): 
    return Favorite.query.filter(Favorite.user_id==user_id).all()


def get_favorite_by_user_id_and_wine_id(user_id, wine_id):
    return Favorite.query.filter(Favorite.user_id==user_id, Favorite.wine_id==wine_id).all() 


def get_dict_of_fav_countries_by_user_id(user_id): 
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
                                               
    # list_of_freq = []
    # for item in freq:
    #     list_of_freq.append(freq[item])

    # return list_of_freq
    return [freq[item] for item in freq]

def get_dict_of_fav_varietals_by_user_id(user_id): 
    fav_wines = Favorite.query.filter(Favorite.user_id==user_id).all()
    
    freq = {}
    for fav in fav_wines:
        if fav.wine.variety in freq:
            freq[fav.wine.variety]["num_fav"] += 1
        else:
            freq[fav.wine.variety] = {
                                        "variety" : fav.wine.variety,
                                        "num_fav" : 1
                                    }
                        
    return [freq[item] for item in freq]


def get_fav_countries(user_id):
    fav_wines = Favorite.query.filter(Favorite.user_id==user_id).all()

    freq = {}
    for fav in fav_wines:
        if fav.wine.country in freq:
            freq[fav.wine.country] += 1
        else:
            freq[fav.wine.country] = 1

    #iterate through the key-value pairs in the freq dictionary
    #next we convert the value v into a float(v) and check if that float is equal to max value
    #if that is the case, we add the key k to the list
    return [k for k,v in freq.items() if float(v) == max(freq.values())]

    #could practice with querying for this data instead. joins and stuff
    #order by num of favorites


def get_wines_by_country(country):
    return Wine.query.filter(Wine.country==country).all()


def get_wines_by_variety(variety):
    return Wine.query.filter(Wine.variety==variety).all()


def get_countries():
    # result = Wine.query.with_entities(Wine.country).distinct()
    query = Wine.query.distinct(Wine.country)
    return [q.country for q in query]


def get_varietals():
    # result = Wine.query.with_entities(Wine.country).distinct()
    query = Wine.query.distinct(Wine.variety)
    return [q.variety for q in query]


def get_fav_varietals(user_id):
    fav_wines = Favorite.query.filter(Favorite.user_id==user_id).all()

    freq = {}
    for fav in fav_wines:
        if fav.wine.variety in freq:
            freq[fav.wine.variety] += 1
        else:
            freq[fav.wine.variety] = 1

    #iterate through the key-value pairs in the freq dictionary
    #next we convert the value v into a float(v) and check if that float is equal to max value
    #if that is the case, we add the key k to the list
    return [k for k,v in freq.items() if float(v) == max(freq.values())]

    #could practice with querying for this data instead. joins and stuff
    #order by num of favorites


def get_rec_wines_by_country(user_id):
    fav_countries = get_fav_countries(user_id)
    
    rec_wines = []
    while fav_countries:
        wines = Wine.query.filter(Wine.country==fav_countries.pop()).all()
        for wine in wines:
            rec_wines.append(wine)
    
    return rec_wines


def get_rec_wines_by_variety(user_id):
    fav_varietals = get_fav_countries(user_id)
    
    rec_wines = []
    while fav_varietals:
        wines = Wine.query.filter(Wine.variety==fav_varietals.pop()).all()
        for wine in wines:
            rec_wines.append(wine)
    
    return rec_wines


# def get_ratings_by_user_id(user_id):  
#     ratings = Rating.query.filter(Rating.user_id==user_id).all()


#     critic_rating = []
#     your_rating = []
#     for rating in ratings:
#         your_rating.append(rating.rating)
#         critic_rating.append(rating.wine.points)
    
#     return (your_rating + critic_rating)

    # return Rating.query.filter(Rating.user_id==user_id).all()


def get_ratings_by_user_id(user_id):  
    return Rating.query.filter(Rating.user_id==user_id).all()


def get_dict_of_ratings_by_user_id(user_id): 
    ratings = Rating.query.filter(Rating.user_id==user_id).all()
    
    dict_ratings = {}
    for rating in ratings:
        dict_ratings[rating] = {
                                "wine_id" : rating.wine.wine_id,
                                "critic_rating" : rating.wine.points,
                                "user_rating" : rating.rating
                                }

    return [dict_ratings[item] for item in dict_ratings]


def search_wines(title_keywords):
    """Search bar."""

    wines = Wine.query.filter(Wine.title.like('%' + title_keywords + '%')).all()

    return wines


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

