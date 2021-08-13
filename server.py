"""Server for my cellar app."""

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import date
import random


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
bootstrap = Bootstrap(app)


@app.route('/')
def homepage():
    """View homepage."""
    users = crud.all_users()
    random_user1 = random.choice(users)
    random_user2 = random.choice(users)
    random_user3 = random.choice(users)

    if 'user_id' in session:
    #why does 'if session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        if user:
            return render_template('homepage.html', user=user, users=users, random_user1=random_user1, random_user2=random_user2, random_user3=random_user3)
        else:
            flash('Something for went wrong, logging you out.')
            return redirect('/logout')

    return render_template('homepage.html', random_user1=random_user1, random_user2=random_user2, random_user3=random_user3)
    
    # print(dir(session))
    # print(help(session.clear))


@app.route('/search')
def search_wines():
    """Displays results for wine search."""

    title_keywords = request.args.get('title_keywords')
    title_keywords = title_keywords.title()

    wines = crud.search_wines(title_keywords)

    if 'user_id' in session:
        user = crud.get_user_by_id(session['user_id'])
        return render_template('search_results.html', wines=wines, user=user)
    else:
        return render_template('search_results.html', wines=wines)



@app.route('/create_account_page')
def create_account_page():
    """Routes to create account page."""

    return render_template('create_account.html')


@app.route('/login_page')
def login_page():
    """Routes to login page."""

    return render_template('login.html')


@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""
    
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    
    if user:
        flash('An account with that email already exits. Try again.')

    else:
        crud.create_user(name, email, password)
        flash('Account created successfully! You may now log in.')

    return redirect('/')


@app.route('/login', methods=['POST'])
def log_in():
    """User log in."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:

        if password == user.password:
            session['user_id'] = user.user_id
            flash('Logged in!')

        else:
            flash('Incorrect password. Unable to log in.')

    else:
        flash('No account associated with that email address.')
        
    return redirect('/')


@app.route('/logout')
def log_out():
    """User log out."""

    #alternatively, can use del session['user_id']
    session.clear()

    if 'user_id' in session:
        flash('Logout failed')
        #Think about user experience perspective

    else:
        flash("Successfully logged out.")

    return redirect('/')


@app.route('/wines')
def all_wines():
    """Display wine countries and varietals."""

    wines = crud.all_wines()
    countries = crud.get_countries()
    varietals = crud.get_varietals()

    if 'user_id' in session:
    #why does 'in session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('all_wines.html', wines=wines, countries=countries, varietals=varietals, user=user)
    
    else:
        return render_template('all_wines.html', wines=wines, countries=countries, varietals=varietals)


@app.route('/countries')
def wine_countries():
    """Display wine countries"""

    wines = crud.all_wines()
    countries = crud.get_countries()

    if 'user_id' in session:
    #why does 'in session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('wine_countries.html', wines=wines, countries=countries, user=user)
    
    else:
        return render_template('wine_countries.html', wines=wines, countries=countries)


@app.route('/grapes')
def wine_grapes():
    """Display wine varietals"""

    wines = crud.all_wines()
    varietals = crud.get_varietals()

    if 'user_id' in session:
    #why does 'in session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('wine_varietals.html', wines=wines, varietals=varietals, user=user)
    
    else:
        return render_template('wine_varietals.html', wines=wines, varietals=varietals)


@app.route('/wines/country/<country>')
def wines_by_country(country):
    """Display all wine countries."""

    #for value in Session.query(Table.column).distinct():

    wines = crud.get_wines_by_country(country)
    # german_wines = crud.get_wines_by_country('Germany')

    if 'user_id' in session:
    #why does 'in session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('wine_by_country.html', wines=wines, user=user)
    
    else:
        return render_template('wine_by_country.html', wines=wines)


@app.route('/wines/variety/<variety>')
def wines_by_variety(variety):
    """Dispaly all wine varietals."""

    wines = crud.get_wines_by_variety(variety)

    if 'user_id' in session:
        user = crud.get_user_by_id(session['user_id'])
        return render_template('wine_by_variety.html', wines=wines, user=user)

    else:
        return render_template('wine_by_variety.html', wines=wines)


#code for bigger wine details page
@app.route('/wines/<int:wine_id>')
def wine_by_id(wine_id):

    wine = crud.get_wine_by_id(wine_id)
    ratings = crud.get_ratings_by_wine_id(wine_id)
    comments = crud.get_comments_by_wine_id(wine_id)

    if ratings:
        #add ratings to a list
        list_of_ratings = [rating.rating for rating in ratings]

        #calculate average and round to tenth
        average = sum(list_of_ratings)/len(list_of_ratings)
        average = round(average,1)

        star_average = round(average * 2) / 2
        # star_average = int(average)

        #TODO: Implement the following sorted tabled, if desired
        desc_ordered_ratings = crud.get_and_order_rating_by_wine_id(wine_id)
        dict_comments = {comment.user.user_id:comment.comment for comment in comments}

        if session:
            # user_id = session['user_id']
            user = crud.get_user_by_id(session['user_id'])
            current_users_rating = crud.get_rating_by_user_id_and_wine_id(user.user_id, wine_id)
            favorites = crud.get_favorites_by_wine_id(wine_id)
            # print("****************************************** HERE", file=sys.stderr)
            # print(favorites, file=sys.stderr)
            num_favorites = len(favorites)
            current_users_fav = crud.get_favorite_by_user_id_and_wine_id(user.user_id, wine_id)
            return render_template('wine_details.html', wine_id=wine_id, 
                                                        wine=wine, 
                                                        ratings=ratings,
                                                        user=user, 
                                                        current_users_rating=current_users_rating, 
                                                        favorites=favorites,
                                                        num_favorites=num_favorites, 
                                                        current_users_fav=current_users_fav,
                                                        average=average,
                                                        star_average=star_average,
                                                        desc_ordered_ratings=desc_ordered_ratings,
                                                        dict_comments=dict_comments)
        else:
            favorites = crud.get_favorites_by_wine_id(wine_id)
            num_favorites = len(favorites)
            return render_template('wine_details.html', wine=wine, 
                                                        ratings=ratings,
                                                        favorites=favorites,
                                                        num_favorites=num_favorites,
                                                        average=average,
                                                        star_average=star_average,
                                                        desc_ordered_ratings=desc_ordered_ratings,
                                                        dict_comments=dict_comments)

    else:
        if session:
            # user_id = session['user_id']
            user = crud.get_user_by_id(session['user_id'])
            current_users_rating = crud.get_rating_by_user_id_and_wine_id(user.user_id, wine_id)
            favorites = crud.get_favorites_by_wine_id(wine_id)
            num_favorites = len(favorites)
            current_users_fav = crud.get_favorite_by_user_id_and_wine_id(user.user_id, wine_id)
            return render_template('wine_details.html', wine_id=wine_id, 
                                                        wine=wine, 
                                                        ratings=ratings,
                                                        user=user, 
                                                        current_users_rating=current_users_rating, 
                                                        favorites=favorites,
                                                        num_favorites=num_favorites, 
                                                        current_users_fav=current_users_fav)
        else:
            favorites = crud.get_favorites_by_wine_id(wine_id)
            num_favorites = len(favorites)
            return render_template('wine_details.html', wine=wine, 
                                                        ratings=ratings,
                                                        favorites=favorites,
                                                        num_favorites=num_favorites)
  

@app.route('/wines/<int:wine_id>/ratings', methods=['POST'])
def create_update_or_favorite(wine_id):

    user = crud.get_user_by_id(session['user_id'])
    wine = crud.get_wine_by_id(wine_id)
    
    # rating = request.form.get('rating')
    comment = request.form.get('comment')
    favorite = request.form.get('favorite')

    # new_rating = request.form.get('new_rating')
    new_comment = request.form.get('new_comment')

    star_rating = request.form.get('star_rating')
    new_star_rating = request.form.get('new_star_rating')
    # star2 = request.form.get('star2')
    # star3 = request.form.get('star3')
    # star4 = request.form.get('star4')
    # star5 = request.form.get('star5')
    print("*********************")
    print(star_rating)

    print("*********************")
    print(comment)


    # def create_rating_comment_flash_msg(user, wine, comment, star_rating):
    #     crud.create_rating(user, wine, rating)
    #     crud.comment(user, wine, comment)
    #     flash('Rating and comment submitted!')
    #     return redirect(f'/wines/{wine_id}')
    
    # def update_rating_comment_flash_msg(user, wine, new_comment, new_rating):
    #     crud.update_rating(user, wine, new_rating)
    #     crud.update_comment(user, wine, new_comment)
    #     flash('Rating and comment updated!')
    #     return redirect(f'/wines/{wine_id}')
    
    # if star_rating and comment:
    #     crud.create_rating(user, wine, star_rating)
    #     crud.comment(user, wine, comment)
    #     flash('Rating and comment submitted!')
    #     return redirect(f'/wines/{wine_id}')



    #if logged in user makes a new rating and comment, add the rating and comment
    # if rating and comment:
    #     create_rating_comment_flash_msg(user, wine, comment, rating)
    #     # crud.create_rating(user, wine, rating)
    #     # crud.comment(user, wine, comment)
    #     # flash('Rating and comment submitted!')
    #     # return redirect(f'/wines/{wine_id}')
    # #if logged in user updates a previously created rating and comment, update the existing rating and comment
    if star_rating and comment:
        crud.create_rating(user, wine, star_rating)
        crud.comment(user, wine, comment)
        flash('Rating and comment submitted!')
        return redirect(f'/wines/{wine_id}')
    elif new_star_rating and new_comment:
        crud.update_rating(user, wine, new_star_rating)
        crud.update_comment(user, wine, new_comment)
        flash('Rating and comment updated!')
        return redirect(f'/wines/{wine_id}')
    elif favorite:
        crud.favorite(user,wine)
        flash('Favorite added!')
        return redirect(f'/wines/{wine_id}')
    else:
        crud.unfavorite(user.user_id, wine.wine_id)
        flash('Removed from your favorites!')
        return redirect(f'/wines/{wine_id}') 


@app.route('/users')
def all_users():
    """Display all users."""

    users = crud.all_users()

    if 'user_id' in session:
    #why does 'if session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('all_users.html', users=users, user=user)
    
    else:
        return render_template('all_users.html', users=users)


@app.route('/users/<int:user_id>')
def user_by_id(user_id):
#create new key:value pair in session
#session['friend_user_id'] = user_id
    user = crud.get_user_by_id(user_id)
    fav_wines = crud.get_favorites_by_user_id(user_id)
    fav_countries = crud.get_fav_countries(user.user_id)
    fav_varietals = crud.get_fav_varietals(user.user_id)
    comments = crud.get_comments_by_user_id(user.user_id)
    # wine_id = request.form.get('wine_id')
    # rating = crud.get_rating_by_user_id_and_wine_id(user.user_id, wine_id)
   
    ratings = crud.get_ratings_by_user_id(user.user_id)
    dict_ratings = {rating.wine.wine_id:rating.rating for rating in ratings}
    # dict_ratings = {}
    # for rating in ratings:
    #     dict_ratings[rating.wine.wine_id] = rating.rating
    dict_ratings_date = {rating.wine.wine_id:(rating.date).strftime("%B %d, %Y") for rating in ratings}

    if session:
        if user_id != session['user_id']:
            session['friend_user_id'] = user_id

    return render_template('user_details.html', user=user, 
                                                fav_wines=fav_wines, 
                                                fav_countries=fav_countries, 
                                                fav_varietals=fav_varietals, 
                                                comments=comments, 
                                                dict_ratings=dict_ratings,
                                                dict_ratings_date=dict_ratings_date,
                                                user_id=user_id)

@app.route('/fav_countries.json')
def get_entries():
    if session['friend_user_id']:
        return jsonify({'data' : crud.get_dict_of_fav_countries_by_user_id(session['friend_user_id'])})
    else:
        return jsonify({'data' : crud.get_dict_of_fav_countries_by_user_id(session['user_id'])})

    session.pop('friend_user_id')

# @app.route('/fav_countries.json')
# def get_entries():
#     # add conditional, if user is logged in, return this json
#     # get user_id from browser, not from session
#     return jsonify({'data' : crud.get_dict_of_fav_countries_by_user_id(session['user_id'])})

#     #return jsonify(crud.get_dict_of_countries_of_favorites_by_user_id(session['user_id']))
#     # faves = crud.get_favorites_by_user_id(session['user_id'])
#     # return jsonify({fave.favorite_id : fave.to_dict() for fave in faves})
#     # return jsonify({fave.favorite_id: fave.wine.country for fave in faves})

# # @app.route('/friend/fav_countries.json')
# # def get_entries():
# #     # add conditional, if user is logged in, return this json
# #     # get user_id from browser, not from session
# #     return jsonify({'data' : crud.get_dict_of_fav_countries_by_user_id(session['friend_user_id'])})

@app.route('/fav_varietals.json')
def get_entries2():
    if session['friend_user_id']:
        return jsonify({'data' : crud.get_dict_of_fav_varietals_by_user_id(session['friend_user_id'])})
    else:
        return jsonify({'data' : crud.get_dict_of_fav_varietals_by_user_id(session['user_id'])})

    session.pop('friend_user_id')
    # return jsonify({'data' : crud.get_dict_of_fav_varietals_by_user_id(session['user_id'])})


@app.route('/wines/recs')
def wine_recs():
    """Displays all wine recs from logged in user's favorite countries."""
    user = crud.get_user_by_id(session['user_id'])
    wines = crud.get_rec_wines_by_country(user.user_id)
    fav_countries = crud.get_fav_countries(user.user_id)
    return render_template('wine_recs.html', user=user, wines=wines, fav_countries=fav_countries)


# @app.route('/wines/recs/country/<country>')
# def recs_by_country(country):
#     """Displays logged in user's wine recs from specified country."""
#     user = crud.get_user_by_id(session['user_id'])
#     wines = crud.get_wines_by_country(country)
#     return render_template('wine_recs_country.html', user=user, wines=wines)


@app.route('/user/<int:user_id>/recs/country/<country>')
def recs_by_country(user_id, country):
    """Displays wine recs from specified country."""
    user = crud.get_user_by_id(user_id)
    wines = crud.get_wines_by_country(country)
    return render_template('wine_recs_country.html', user=user, wines=wines)


# @app.route('/wines/recs/variety/<variety>')
# def recs_by_variety(variety):
#     """Displays logged in user's wine recs from specified varitel."""
#     user = crud.get_user_by_id(session['user_id'])
#     wines = crud.get_wines_by_variety(variety)
#     return render_template('wine_recs_variety.html', user=user, wines=wines)


@app.route('/user/<int:user_id>/recs/variety/<variety>')
def recs_by_variety(user_id, variety):
    """Displays wine recs from specified varitel."""
    user = crud.get_user_by_id(user_id)
    wines = crud.get_wines_by_variety(variety)
    return render_template('wine_recs_variety.html', user=user, wines=wines)
    

@app.route('/ratings.json')
def ratings_by_user_id():
    if session['friend_user_id']:
        return jsonify({'data' : crud.get_dict_of_ratings_by_user_id(session['friend_user_id'])})
    else:
        return jsonify({'data' : crud.get_dict_of_ratings_by_user_id(session['user_id'])})

    session.pop('friend_user_id')
    # return jsonify({'data' : crud.get_dict_of_ratings_by_user_id(session['user_id'])})


@app.route('/review/wines/<int:wine_id>')
def create_or_update_rating(wine_id):
    """Create or update a wine rating."""

    if session:
        # user_id = session['user_id']
        user = crud.get_user_by_id(session['user_id'])
        current_users_rating = crud.get_rating_by_user_id_and_wine_id(user.user_id, wine_id)
        wine = crud.get_wine_by_id(wine_id)
    
        return render_template('wine_rate.html', wine_id=wine_id, 
                                                    wine=wine, 
                                                    user=user, 
                                                    current_users_rating=current_users_rating)
    else:
        return render_template('wine_rate.html')


@app.route('/favorites/users/<user_id>')
def user_favorites(user_id):
#create new key:value pair in session
#session['friend_user_id'] = user_id
    user = crud.get_user_by_id(user_id)
    fav_wines = crud.get_favorites_by_user_id(user_id)
    # fav_countries = crud.get_fav_countries(user.user_id)
    # fav_varietals = crud.get_fav_varietals(user.user_id)
    # comments = crud.get_comments_by_user_id(user.user_id)

    # ratings = crud.get_ratings_by_user_id(user.user_id)
    # dict_ratings = {rating.wine.wine_id:rating.rating for rating in ratings}
    # # dict_ratings = {}
    # # for rating in ratings:
    # #     dict_ratings[rating.wine.wine_id] = rating.rating
    # dict_ratings_date = {rating.wine.wine_id:(rating.date).strftime("%B %d, %Y") for rating in ratings}

    if user_id != session['user_id']:
        session['friend_user_id'] = user_id

    return render_template('user_favorites.html', user=user, 
                                                fav_wines=fav_wines, 
                                                user_id=user_id)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)