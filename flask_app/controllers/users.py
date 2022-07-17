from ssl import HAS_TLSv1_1
from unicodedata import category
from flask import redirect, request, render_template, session, flash
from flask_app.models import user, recipe
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/recipes')
    return render_template('index.html')

@app.route('/process', methods = ['POST'])
def process():
    if request.form['type'] == 'register':
        if not user.User.validate_register(request.form):
            return redirect('/')
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password':bcrypt.generate_password_hash(request.form['password']) 
        }
        print('a punto de guardar')
        session['id'] = user.User.save(data)
        return redirect('/recipes')

    elif request.form['type'] == 'login':
        user1 = user.User.get_user_by_email(request.form['email']) 
        if user1 == False or not bcrypt.check_password_hash(user1.password, request.form['password']):
            flash('Invalid email/password', category = 'login')
            return redirect('/')
        session['id'] = user1.id
        return redirect('/recipes')
    elif request.form['type'] == 'new_recipe':
        if not recipe.Recipe.validate_recipe(request.form):
            return redirect('/recipes/new')
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'cooked_date': request.form['cooked_date'],
            'under_30': request.form['under_30'],
            'user_id': request.form['user_id']
        }
        id = recipe.Recipe.save(data)   
        return redirect(f'/recipes/{id}')
    elif request.form['type'] == 'edit_recipe':
        print('HEREEEEEE')
        if not recipe.Recipe.validate_recipe(request.form):
            return redirect(f'/recipes/edit/{request.form["recipe_id"]}')
        data = {
            'recipe_id': request.form['recipe_id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'cooked_date': request.form['cooked_date'],
            'under_30': request.form['under_30']
        }
        recipe.Recipe.update(data)
        return redirect(f'/recipes/{request.form["recipe_id"]}') 

@app.route('/recipes')
def recipes():
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    recipes = recipe.Recipe.get_all()
    return render_template('recipes.html', user = user1, recipes = recipes)

@app.route('/recipes/new')
def new_recipe():
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    return render_template('new_recipe.html', user = user1)

@app.route('/recipes/<int:id>')
def the_recipe(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    recipe1 = recipe.Recipe.get_recipe_by_id_with_creator(id)
    return render_template('recipe.html', user = user1, recipe = recipe1)

@app.route('/recipes/edit/<int:id>')
def edit(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    recipe1 = recipe.Recipe.get_recipe_by_id_with_creator(id)
    if session['id'] != recipe1.user_id:
        return redirect('/recipes')
    return render_template('edit.html', user = user1, recipe = recipe1)

@app.route('/delete/<int:id>')
def delete(id):
    if not 'id' in session:
        return redirect('/')
    recipe1 = recipe.Recipe.get_recipe_by_id(id)
    if int(session['id']) == int(recipe1.user_id):
        recipe.Recipe.delete(id)
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')