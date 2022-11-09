from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash, request
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)  


class User:
    db = 'login_registration'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users  (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() )"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(request.form['first_name']) <=1:
            flash("First name must be at least two letters long ")
            is_valid = False
        if len(request.form['last_name']) <=1:
            flash("Last name must be at least two letters long ")
            is_valid = False
        if len(request.form['email']) <=1:
            flash("Must insert email")
            is_valid = False
        if len(request.form['password']) <= 7:
            flash("Password must be at least 8 characters long.")
            is_valid = False
        if request.form['password'] != request.form['confirm_password'] :
            flash("Passwords don't match. ")
            is_valid = False
        query = "SELECT * FROM users where email = %(email)s"
        if query != False:
            is_valid = False
            flash("Email already registered")
        else:
            return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
