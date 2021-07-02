"""Server for my cellar app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Routes and view functions go here

@app.route('/')
def homepage():
    """View homepage."""

    # print(dir(session))
    # print(help(session.clear))

    return render_template('homepage.html')


@app.route('/wines')
def all_wines():
    """Display all wines."""

    wines = crud.all_wines()

    return render_template('all_wines.html', wines=wines)


@app.route('/wines/<wine_id>')
def wine_by_id(wine_id):

    wine = crud.get_wine_by_id(wine_id)
    #Query to see if current user whose logged in already rated this wine
    #If the user already rated this wine, add an if conditional to the html page (similar to if logged in)
    #In the html page, include a message that says you've already rated this and give option to update/edit your rating
    #Render update rating form. Can either update rating or delete that rating row from your table and create a new rating. 

    return render_template('wine_details.html', wine=wine)


@app.route('/users')
def all_users():
    """Display all users."""

    users = crud.all_users()

    return render_template('all_users.html', users=users)


@app.route('/users/<user_id>')
def user_by_id(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


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

    if password == user.password:
        session['user_id'] = user.user_id
        flash('Logged in!')

    else:
        flash('Incorrect password. Unable to log in.')
        
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


@app.route('/wines/<wine_id>/ratings', methods=['POST'])
def create_rating(wine_id):

    user = crud.get_user_by_id(session['user_id'])
    wine = crud.get_wine_by_id(wine_id)
    rating = request.form.get('rating')

    crud.rating(user, wine, rating)
    ratings = crud.get_ratings_by_wine_id(wine_id)

    return render_template('/wine_ratings.html', wine=wine, ratings=ratings)

# or rewrite crud rating() function to take wine_id, and user_id arguments insteads of objects


# @app.route('/wines/<wine_id>/update_ratings', methods=['POST'])
# def update_rating(wine_id):

#     user = crud.get_user_by_id(session['user_id'])
#     wine = crud.get_wine_by_id(wine_id)
#     rating = request.form.get('rating')

#     **crud.update_rating .... (user, wine, rating)
        #find current rating and update it
#     ratings = crud.get_ratings_by_wine_id(wine_id)

#     return render_template('/wine_ratings.html', wine=wine, ratings=ratings)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
