"""Server for my cellar app."""

from datetime import datetime, timedelta
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


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
    """Display all wines."""

    wines = crud.all_wines()

    if 'user_id' in session:
    #why does 'if session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('all_wines.html', wines=wines, user=user)
    
    else:
        return render_template('all_wines.html', wines=wines)


@app.route('/wines/<int:wine_id>')
def wine_by_id(wine_id):

    wine = crud.get_wine_by_id(wine_id)
    
    #Query to see if current user whose logged in already rated this wine
    #If the user already rated this wine, add an if conditional to the html page
    #In the html page, include a message that says you've already rated this and give option to update/edit your rating
    #Render update rating form

    if session:
        user_id = session['user_id']
        user = crud.get_user_by_id(user_id)
        current_users_rating = crud.get_rating_by_user_id_and_wine_id(user_id, wine_id)
        favorites = crud.get_favorites_by_wine_id(wine_id)
        num_favorites = len(favorites)
        return render_template('wine_details.html', wine_id=wine_id, wine=wine, user_id=user_id, user=user, current_users_rating=current_users_rating, num_favorites=num_favorites)

    else:
        favorites = crud.get_favorites_by_wine_id(wine_id)
        num_favorites = len(favorites)
        return render_template('wine_details.html', wine_id=wine_id, wine=wine, num_favorites=num_favorites)


@app.route('/wines/<int:wine_id>/ratings', methods=['POST'])
def create_update_or_favorite(wine_id):

    user = crud.get_user_by_id(session['user_id'])
    wine = crud.get_wine_by_id(wine_id)
    
    rating = request.form.get('rating')
    new_rating = request.form.get('new_rating')

    #if logged in user makes a new rating, add the rating to the ratings table
    if rating:
        crud.rating(user, wine, rating)
    #if logged in user updates a previously created rating, update the rating in the ratings table
    elif new_rating:
        crud.update_rating(user, wine, new_rating)
    else:
        crud.favorite(user,wine)

    #if 1 or more ratings for this wine exist, calculate average rating
    ratings = crud.get_ratings_by_wine_id(wine_id)
    if ratings:
        #add ratings to a list
        list_of_ratings = [rating.rating for rating in ratings]

        #calculate average and round to tenth
        average = sum(list_of_ratings)/len(list_of_ratings)
        average = round(average,1)

        #TODO: Implement the following sorted tabled, if desired
        desc_ordered_ratings = crud.get_and_order_rating_by_wine_id(wine_id)

        return render_template('/wine_ratings.html', user=user, wine=wine, average=average, desc_ordered_ratings=desc_ordered_ratings)
    
    return render_template('/wine_ratings.html', user=user, wine=wine)


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
    #query doesn't work
    #countries = crud.get_count_of_favorite_countries_by_user_id()

    return render_template('user_details.html', user=user, fav_wines=fav_wines)


@app.route('/home')
def redirect_home():
    """Redirect to homepage."""

    return redirect('/')


@app.route('/chartjs')
def show_chartjs():

    if 'user_id' in session:
    #why does 'if session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('chartjs.html', user=user)
    else:
        return render_template('chartjs.html')


# @app.route('/sales_this_week.json')
# def get_total_sales_this_week():
#     """Get the daily total # of melons sold for the past 7 days."""

#     # weekly_sales = list of tuples (datetime, int)

#     sales_this_week = []
#     for date, total in weekly_sales:
#         sales_this_week.append({'date': date.isoformat(),
#                                 'melons_sold': total})

#     return jsonify({'data': sales_this_week})


@app.route('/test.json')
def get_entries():
    #return jsonify(crud.get_dict_of_countries_of_favorites_by_user_id(session['user_id']))

    faves = crud.get_favorites_by_user_id(session['user_id'])
    return jsonify({fave.favorite_id: fave.to_dict() for fave in faves})
    #return jsonify({fave.favorite_id: fave.wine.country for fave in faves})



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
