from ShopifyTupperware import app
from ShopifyTupperware.data.user_db import UserDb
import hashlib
import base64
from flask import request, jsonify
#from flask_jwt_simple import create_jwt
from flask_jwt_extended import create_access_token

class UserController:

    #use for Basic Authorization
    @app.route('/user', methods= ['POST'])
    def user_validation():
        authorization = request.authorization
        if not authorization:
            return jsonify(msg= 'Missing Authorization'), 401
        username = authorization['username']
        password = authorization['password']
        if not username or not password:
            return jsonify(msg= 'Wrong Authorization values'), 401
        password_enc = hashlib.md5(password.encode()).hexdigest()
        user_valid = UserDb.get_valid_user_secret(username, password_enc)
        if not user_valid:
            return jsonify(msg= 'Username and Password not valid'), 401
        return jsonify(jwt= create_access_token(identity= username)), 200

    #use for Login Authentication
    @app.route('/user/login', methods= ['POST'])
    def user_login():
        if not request.is_json:
            return jsonify(msg= 'Missing JSON body'), 400
        body = request.get_json(force=True)
        username = body.get('username', None)
        password = body.get('password', None)
        if not username or not password:
            return jsonify(msg= 'Missing username and password parameter'), 400
        password_enc = hashlib.md5(password.encode()).hexdigest()
        user_valid = UserDb.valid_user(username, password_enc)

        if not user_valid:
            return jsonify(msg= 'Username and Password not valid'), 401
        response = jsonify(jwt= create_access_token(identity= username)), 200
        return response
