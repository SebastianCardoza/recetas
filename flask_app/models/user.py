from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL('esquema_recetas').query_db(query,data)

    @classmethod
    def get_user_by_id_with_recipes(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('esquema_recetas').query_db(query, data)
        user = cls(results[0])
        user.recipes = recipe.Recipe.get_recipe_by_id(id)
        return user

    @classmethod
    def get_user_by_id(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('esquema_recetas').query_db(query, data)
        user = cls(results[0])
        return user

    @classmethod
    def get_user_by_email(cls, email):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email': email}
        print('se logro?')
        results = connectToMySQL('esquema_recetas').query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('esquema_recetas').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        data = {'id': id}
        connectToMySQL('esquema_recetas').query_db(query, data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name has to be at least 2 characters', category='register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name has to be at least 2 characters', category='register')
            is_valid = False
        if User.get_user_by_email(user['email']) != False:
            flash('Email already exists', category='register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Email is not valid', category='register')    
            is_valid = False
        if len(user['password']) < 8:
            flash('Password has to be at least 8 characters', category='register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords doesnt match', category='register')
            is_valid = False
        return is_valid
