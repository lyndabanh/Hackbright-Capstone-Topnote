"""Server for my cellar app."""

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
bootstrap = Bootstrap(app)


@app.route('/')
def homepage():
    """View homepage."""

    if 'user_id' in session:
    #why does 'if session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('homepage.html', user=user)
    else:
        return render_template('homepage.html')
    
    # print(dir(session))
    # print(help(session.clear))

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
    """Display wine countries"""

    wines = crud.all_wines()
    countries = crud.get_countries()
    varietals = crud.get_varietals()

    if 'user_id' in session:
    #why does 'in session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('all_wines.html', wines=wines, countries=countries, varietals=varietals, user=user)
    
    else:
        return render_template('all_wines.html', wines=wines, countries=countries, varietals=varietals)
    

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
    # merlots = crud_get_wines_by_variety('Merlot')

    if 'user_id' in session:
        user = crud.get_user_by_id(session['user_id'])
        return render_template('wine_by_variety.html', wines=wines, user=user)

    else:
        return render_template('wine_by_variety.html', wines=wines)

# #code for smaller wine details page and wine details ratings on diff page
# @app.route('/wines/<int:wine_id>')
# def wine_by_id(wine_id):

#     wine = crud.get_wine_by_id(wine_id)
    
#     #Query to see if current user whose logged in already rated this wine
#     #If the user already rated this wine, add an if conditional to the html page
#     #In the html page, include a message that says you've already rated this and give option to update/edit your rating
#     #Render update rating form

#     if session:
#         # user_id = session['user_id']
#         user = crud.get_user_by_id(session['user_id'])
#         current_users_rating = crud.get_rating_by_user_id_and_wine_id(user.user_id, wine_id)
#         favorites = crud.get_favorites_by_wine_id(wine_id)
#         num_favorites = len(favorites)
#         current_users_fav = crud.get_favorite_by_user_id_and_wine_id(user.user_id, wine_id)
#         return render_template('wine_details.html', wine_id=wine_id, 
#                                                     wine=wine, 
#                                                     user=user, 
#                                                     current_users_rating=current_users_rating, 
#                                                     num_favorites=num_favorites, 
#                                                     current_users_fav=current_users_fav)
#     else:
#         favorites = crud.get_favorites_by_wine_id(wine_id)
#         num_favorites = len(favorites)
#         return render_template('wine_details.html', wine_id=wine_id, 
#                                                     wine=wine,
#                                                     num_favorites=num_favorites)

# # # this app route pairs with app route/view fxn for smaller wine details page + separate wine details ratings page
# # @app.route('/wines/<int:wine_id>/ratings')
# # def create_update_or_favorite(wine_id):

# #     user = crud.get_user_by_id(session['user_id'])
# #     wine = crud.get_wine_by_id(wine_id)
    
# #     # rating = request.form.get('rating')
# #     # comment = request.form.get('comment')
# #     # favorite = request.form.get('favorite')

# #     # new_rating = request.form.get('new_rating')
# #     # new_comment = request.form.get('new_comment')
    

# #     # #if logged in user makes a new rating, add the rating to the ratings table
# #     # if rating:
# #     #     crud.rating(user, wine, rating)
# #     #     crud.comment(user, wine, comment)
# #     #     return redirect(f'/wines/{wine_id}')
# #     # #if logged in user updates a previously created rating, update the rating in the ratings table
# #     # elif new_rating:
# #     #     crud.update_rating(user, wine, new_rating)
# #     #     crud.update_comment(user, wine, new_comment)
# #     #     return redirect(f'/wines/{wine_id}')
# #     # elif favorite:
# #     #     crud.favorite(user,wine)
# #     #     return redirect(f'/wines/{wine_id}')
# #     # else:
# #     #     crud.unfavorite(user.user_id, wine.wine_id)
# #     #     return redirect(f'/wines/{wine_id}')

# #     #if 1 or more ratings for this wine exist(s), calculate average rating
# #     ratings = crud.get_ratings_by_wine_id(wine_id)
# #     if ratings:
# #         #add ratings to a list
# #         list_of_ratings = [rating.rating for rating in ratings]

# #         #calculate average and round to tenth
# #         average = sum(list_of_ratings)/len(list_of_ratings)
# #         average = round(average,1)

# #         #TODO: Implement the following sorted tabled, if desired
# #         desc_ordered_ratings = crud.get_and_order_rating_by_wine_id(wine_id)
# #         return render_template('/wine_ratings.html', user=user, 
# #                                                     wine=wine, 
# #                                                     average=average, 
# #                                                     desc_ordered_ratings=desc_ordered_ratings)
# #         # return redirect(f'/wines/{wine_id}', user=user, wine=wine, average=average, desc_ordered_ratings=desc_ordered_ratings)
# #         # return redirect(f'/wines/{wine_id}')
# #     return render_template('/wine_ratings.html', user=user, 
# #                                                 wine=wine)
# #     # return redirect(f'/wines/{wine_id}', user=user, wine=wine)
# #     # return redirect(f'/wines/{wine_id}')    


# #code for bigger wine details page
@app.route('/wines/<int:wine_id>')
def wine_by_id(wine_id):

    wine = crud.get_wine_by_id(wine_id)
    ratings = crud.get_ratings_by_wine_id(wine_id)

    if ratings:
        #add ratings to a list
        list_of_ratings = [rating.rating for rating in ratings]

        #calculate average and round to tenth
        average = sum(list_of_ratings)/len(list_of_ratings)
        average = round(average,1)

        #TODO: Implement the following sorted tabled, if desired
        desc_ordered_ratings = crud.get_and_order_rating_by_wine_id(wine_id)

        if session:
            # user_id = session['user_id']
            user = crud.get_user_by_id(session['user_id'])
            current_users_rating = crud.get_rating_by_user_id_and_wine_id(user.user_id, wine_id)
            favorites = crud.get_favorites_by_wine_id(wine_id)
            num_favorites = len(favorites)
            current_users_fav = crud.get_favorite_by_user_id_and_wine_id(user.user_id, wine_id)
            return render_template('wine_details.html', wine_id=wine_id, 
                                                        wine=wine, 
                                                        user=user, 
                                                        current_users_rating=current_users_rating, 
                                                        num_favorites=num_favorites, 
                                                        current_users_fav=current_users_fav,
                                                        average=average,
                                                        desc_ordered_ratings=desc_ordered_ratings)
        else:
            favorites = crud.get_favorites_by_wine_id(wine_id)
            num_favorites = len(favorites)
            return render_template('wine_details.html', wine=wine, 
                                                        num_favorites=num_favorites,
                                                        average=average,
                                                        desc_ordered_ratings=desc_ordered_ratings)

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
                                                        user=user, 
                                                        current_users_rating=current_users_rating, 
                                                        num_favorites=num_favorites, 
                                                        current_users_fav=current_users_fav)
        else:
            favorites = crud.get_favorites_by_wine_id(wine_id)
            num_favorites = len(favorites)
            return render_template('wine_details.html', wine=wine, 
                                                        num_favorites=num_favorites)
  

@app.route('/wines/<int:wine_id>/ratings', methods=['POST'])
def create_update_or_favorite(wine_id):

    user = crud.get_user_by_id(session['user_id'])
    wine = crud.get_wine_by_id(wine_id)
    
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    favorite = request.form.get('favorite')

    new_rating = request.form.get('new_rating')
    new_comment = request.form.get('new_comment')


    #if logged in user makes a new rating, add the rating to the ratings table
    if rating and comment:
        crud.rating(user, wine, rating)
        crud.comment(user, wine, comment)
        flash('Rating and comment submitted!')
        return redirect(f'/wines/{wine_id}')
    #if logged in user updates a previously created rating, update the rating in the ratings table
    elif new_rating and new_comment:
        crud.update_rating(user, wine, new_rating)
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

#     # #if 1 or more ratings for this wine exist(s), calculate average rating
#     # ratings = crud.get_ratings_by_wine_id(wine_id)
#     # if ratings:
#     #     #add ratings to a list
#     #     list_of_ratings = [rating.rating for rating in ratings]

#     #     #calculate average and round to tenth
#     #     average = sum(list_of_ratings)/len(list_of_ratings)
#     #     average = round(average,1)

#     #     #TODO: Implement the following sorted tabled, if desired
#     #     desc_ordered_ratings = crud.get_and_order_rating_by_wine_id(wine_id)
#     #     return render_template('/wine_details.html', user=user, wine=wine, average=average, desc_ordered_ratings=desc_ordered_ratings)
#     #     # return redirect(f'/wines/{wine_id}', user=user, wine=wine, average=average, desc_ordered_ratings=desc_ordered_ratings)
#     #     # return redirect(f'/wines/{wine_id}')
#     # return render_template('/wine_details.html', user=user, wine=wine)
#     # # return redirect(f'/wines/{wine_id}', user=user, wine=wine)
#     # # return redirect(f'/wines/{wine_id}')    


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


@app.route('/users/<user_id>')
def user_by_id(user_id):

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

    return render_template('user_details.html', user=user, fav_wines=fav_wines, fav_countries=fav_countries, fav_varietals=fav_varietals, comments=comments, dict_ratings=dict_ratings)


@app.route('/fav_countries.json')
def get_entries():
    # add conditional, if user is logged in, return this json
    return jsonify({'data' : crud.get_dict_of_fav_countries_by_user_id(session['user_id'])})

    #return jsonify(crud.get_dict_of_countries_of_favorites_by_user_id(session['user_id']))
    # faves = crud.get_favorites_by_user_id(session['user_id'])
    # return jsonify({fave.favorite_id : fave.to_dict() for fave in faves})
    # return jsonify({fave.favorite_id: fave.wine.country for fave in faves})

@app.route('/fav_varietals.json')
def get_entries2():
    return jsonify({'data' : crud.get_dict_of_fav_varietals_by_user_id(session['user_id'])})


@app.route('/recs')
def wine_recs():
    user = crud.get_user_by_id(session['user_id'])
    wines = crud.get_rec_wines_by_country(user.user_id)
    fav_countries = crud.get_fav_countries(user.user_id)
    return render_template('wine_recs.html', user=user, wines=wines, fav_countries=fav_countries)


@app.route('/wines/recs/country/<country>')
def recs_by_country(country):
    user = crud.get_user_by_id(session['user_id'])
    wines = crud.get_wines_by_country(country)
    return render_template('wine_recs_country.html', user=user, wines=wines)


@app.route('/wines/recs/variety/<variety>')
def recs_by_variety(variety):
    user = crud.get_user_by_id(session['user_id'])
    wines = crud.get_wines_by_variety(variety)
    return render_template('wine_recs_variety.html', user=user, wines=wines)
    

@app.route('/ratings.json')
def ratings_by_user_id():
    return jsonify({'data' : crud.get_dict_of_ratings_by_user_id(session['user_id'])})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
