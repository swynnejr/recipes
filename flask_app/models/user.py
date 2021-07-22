from flask import flash
from flask_app import app
import re

from flask_app.config.mysqlconnection import connectToMySQL

class User():

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name =  data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        results = connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_users_with_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        users = []

        for item in results:
            users.append(User(item))

        return users

    # @classmethod
    # def get_users_with_username(cls, data):
    #     query = "SELECT * FROM users WHERE username = %(username)s;"

    #     results = connectToMySQL('recipes_schema').query_db(query, data)

    #     users = []

    #     for item in results:
    #         users.append(User(item))

    #     return users

    @staticmethod
    def validate_registration(data):
        is_valid = True
# establish email rules (EXCEPT ON EXAM)
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# name between 2-32 characters
        if len(data['first_name']) < 2 or len(data['first_name']) > 32:
            flash("First name should be 2 to 32 characters.")
            is_valid = False
        if len(data['last_name']) < 2 or len(data['last_name']) > 32:
            flash("Last name should be 2 to 32 characters.")
            is_valid = False
# valid email
        if not email_regex.match(data['email']):
            flash("Please provide a valid email adress.")
            is_valid = False
# password at least 8 characters
        if len(data['password']) < 8:
            flash("Please provide a password with at least 8 characters.")
            is_valid = False
# password and confirm should match
        if data['password'] != data['confirm_password']:
            flash("Please insure password and confirm password match.")
            is_valid = False
        else:
            flash("Registration successful. Please login to continue.")


# insure username not in use
        # if len(User.get_users_with_username({'username': data['username']})) != 0:
        #     flash("This username is already in use.")
        #     is_valid = False

# insure email not in use
        if len(User.get_users_with_email({'email': data['email']})) != 0:
            flash("This email is already in use.")
            is_valid = False

# RETURN is_valid
        return is_valid
