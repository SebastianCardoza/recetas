from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked_date = data['cooked_date']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save(cls, data):
        data['user_id'] = int(data['user_id'])
        query = 'INSERT INTO recipes (name, description, instructions, cooked_date, under_30, user_id) values (%(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(under_30)s, %(user_id)s);'
        return connectToMySQL('esquema_recetas').query_db(query,data)

    @classmethod
    def get_recipe_by_id(cls, id):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('esquema_recetas').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_recipe_by_id_with_creator(cls, id):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('esquema_recetas').query_db(query, data)
        recipe = cls(results[0])
        recipe.creator = user.User.get_user_by_id(recipe.user_id)
        return recipe

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL('esquema_recetas').query_db(query)
        recipes = []
        for recipe in results:
            recipe = cls(recipe)
            recipe.creator = user.User.get_user_by_id(recipe.user_id)
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_recipes_by_user_id(cls, user_id):
        query = 'SELECT * FROM recipes WHERE user_id = %(user_id)s;'
        data = {'user_id':user_id}
        results = connectToMySQL('esquema_recetas').query_db(query, data)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        data = {'id': id}
        connectToMySQL('esquema_recetas').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooked_date = %(cooked_date)s, under_30 = %(under_30)s WHERE id = %(recipe_id)s;'    
        connectToMySQL('esquema_recetas').query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash('Name has to be at least 3 characters', category='new_recipe')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('Description has to be at least 3 characters', category='new_recipe')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('Instructions have to be at least 3 characters', category='new_recipe')
            is_valid = False
        return is_valid
