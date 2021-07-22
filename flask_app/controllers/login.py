from flask_app.models.user import User
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/users/register', methods =['POST'])
def register_user():
# FUNCTIONALITY CHECK: You can call the hash out here and then print it, OR you call it with the dat input below.
    # pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # print(pw_hash)
# validate form data
    if (User.validate_registration(request.form)):
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
# IF you want "registration success page ADD user.id = User.create_user(data) below  VVVVVVV
        User.create_user(data)
# IF you want a "registration success" landing page VVVV
        # session['user_id'] = user.id
        # return redirect('/success')

# create user IF data is valid
    return redirect('/')

@app.route('/users/login', methods = ['POST'])
def login_user():

    users = User.get_users_with_email(request.form)

    if len(users) != 1:
        flash("User with given email does not exist.")

        return redirect('/')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password for given user is incorrect.")
        return redirect('/')

    session['user_id'] = user.id
    session['email'] = user.email
    session['first_name'] = user.first_name
    # session['username'] = user.username

    return redirect('/dashboard')

# WE WILL WANT TO CHANGE ^^^redirect('/')^^^ and VVV @app.route VVV

# @app.route('/success')
# def success():
#     if 'user_id' not in session:
#         flash("Please log in to view this page.")
#         return redirect('/')

#     return render_template('success.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You are logged out.")
    return redirect ('/')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/recipes/new')
def add_recipe():
    return render_template('new_recipe.html')

@app.route('/recipes/create')
def 