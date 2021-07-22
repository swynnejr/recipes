from flask import flash
from flask_app import app
from flask_app.models.user import User


from flask_app.config.mysqlconnection import connectToMySQL

class Recipe():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description =  data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def create_recipe(cls, data):

        query = 'INSERT INTO recipes (name, description, instructions, under_30, users_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(users_id)s);'

        result = connectToMySQL('recipes_schema').query_db(query, data)

        return result

    @staticmethod
    def validate_recipe(data):

        is_valid = True

        if len(data['name']) < 1 or len(data['name']) > 100:
            flash("Recipe name should be 1 to 100 characters.")
            is_valid = False

        if len(data['description']) < 1 or len(data['description']) > 500:
            flash("Recipe description should be 1 to 500 characters.")
            is_valid = False

        return is_valid

    @classmethod
    def get_all_recipes(cls):

        query = 'SELECT * FROM recipes JOIN users ON recipes.users_id = users.id;'

        results = connectToMySQL('recipes_schema').query_db(query)

        recipes = []

        for item in results:
            recipe = cls(item)
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            recipe.user = User(user_data)
            recipes.append(recipe)

        return recipes

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id WHERE recipes.id = %(id)s;"

        result = connectToMySQL('recipes_schema').query_db(query, data)

        recipe = cls(result[0])
        user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'password': result[0]['password'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at']
        }
        recipe.user = User(user_data)

        return recipe

