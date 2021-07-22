from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/users/register', methods =['POST'])
def register_user():
    if (User.validate_registration(request.form)):
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
        User.create_user(data)
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

    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    flash("You are logged out.")
    return redirect ('/')

@app.route('/dashboard')
def dashboard():
    recipes = Recipe.get_all_recipes()
    print(recipes)
    return render_template('dashboard.html', recipes = recipes)

@app.route('/recipes/new')
def add_recipe():
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():

    if Recipe.validate_recipe(request.form):
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'under_30': request.form['under_30'],
            'users_id': session['user_id']
        }
        Recipe.create_recipe(data)
        print('recipe valid')
        return redirect('/dashboard')
    print('recipe invalid')
    return redirect('/recipes/new')

@app.route('/recipes/<int:recipe_id>')
def show_info(recipe_id):

    recipe = Recipe.get_recipe_by_id({'id': recipe_id})

    return render_template('recipe_info.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):

    recipe = Recipe.get_recipe_by_id({'id': recipe_id})

    if session['user_id'] != recipe.users_id:
        return redirect(f'/recipes/{recipe_id}')

    return render_template('edit_recipe.html', recipe = recipe)


@app.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):

    if Recipe.validate_recipe(request.form):
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'under_30': request.form['under_30'],
            'id': recipe_id
            # 'users_id': session['user_id']
        }
        Recipe.update_recipe(data)
        return redirect(f'/recipes/{recipe_id}')

    return redirect(f'/recipes/{recipe_id}/edit')

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id({'id': recipe_id})


    if session['user_id'] != recipe.users_id:
        return redirect(f'/recipes/{recipe_id}')


    Recipe.delete_recipe(data)
    return redirect('/dashboard')

    # recipe = Recipe.get_recipe_by_id({'id': recipe_id})

    # if session['user_id'] != show.users_id:
    #     return redirect(f'/shows/{show_id}')

    return render_template('delete_recipe.html', recipe = recipe)
