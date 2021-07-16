"""Server for my cellar app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    # print(dir(session))
    # print(help(session.clear))

    if 'user_id' in session:
    #why does 'if session:' not work after you log in, then log out? 
        user = crud.get_user_by_id(session['user_id'])
        return render_template('homepage.html', user=user)
    else:
        return render_template('homepage.html')


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

    session.clear()
    #alternatively, can use del session['user_id']

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
        return render_template('wine_details.html', wine_id=wine_id, wine=wine, user_id=user_id, user=user, current_users_rating=current_users_rating)

    else:
        return render_template('wine_details.html', wine_id=wine_id, wine=wine)


#can specify multiple methods under methods. Would need to conditionally check if method POST or GET for ex)
@app.route('/wines/<int:wine_id>/ratings', methods=['POST'])
def create_rating(wine_id):

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

    #add ratings to a list
    ratings = crud.get_ratings_by_wine_id(wine_id)
    list_of_ratings = [rating.rating for rating in ratings]

    #calculate average and round to tenth
    average = sum(list_of_ratings)/len(list_of_ratings)
    average = round(average,1)

    #TODO: Implement the following sorted tabled, if desired
    desc_ordered_ratings = crud.get_and_order_rating_by_wine_id(wine_id)
    
    return render_template('/wine_ratings.html', user=user, wine=wine, average=average, desc_ordered_ratings=desc_ordered_ratings)

    
# #JS put request. Update the methods, so that it's diff than the function above.
# @app.route('/wines/<int:wine_id>/ratings/update', methods=['POST'])
# def update_rating(wine_id):

#     user = crud.get_user_by_id(session['user_id'])
#     wine = crud.get_wine_by_id(wine_id)
#     rating = request.form.get('new_rating')

#     crud.update_rating(user, wine, rating)

#     ratings = crud.get_ratings_by_wine_id(wine_id)
    
    
#     #add ratings to a list 
#     list_of_ratings = [rating.rating for rating in ratings]

#     print(list_of_ratings)

#     #calculate average and round to tenth
#     average = sum(list_of_ratings)/len(list_of_ratings)
#     average = round(average,1)

#     desc_ordered_ratings = crud.get_and_order_rating_by_wine_id(wine_id)

#     return render_template('/wine_ratings.html', user=user, wine=wine, average=average, desc_ordered_ratings=desc_ordered_ratings)


@app.route('/users')
def all_users():
    """Display all users."""

    users = crud.all_users()

    return render_template('all_users.html', users=users)


@app.route('/users/<user_id>')
def user_by_id(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route('/home')
def redirect_home():
    """Redirect to homepage."""

    return redirect('/')





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
