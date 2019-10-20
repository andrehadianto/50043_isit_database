from flask_restful import Resource, reqparse, request
import jwt
from base64 import b64encode
import os
from common.util import mongo
from bson.json_util import dumps, default

JWT_ALG = "HS256"

class UserLogin(Resource):
    """Returns user's id and generated jwt"""
    def post(self):
        req_json = request.get_json()
        try:
            _user = req_json['user']
            _password = req_json['pwd']
        except Exception as e:
            print(e)
            return {"message": "username and password are required fields"}, 400

        user_is_exist = False
        user_list = mongo.db.user_data.find({},{"_id": 0, "username": 1})
        for user in user_list:
            if user.get("username") == _user:
                user_is_exist = True
                break
        if not user_is_exist:
            return {"message": "User {} does not exist".format(_user)}

        user = mongo.db.user_data.find_one({"username": _user})
        user_secret = user.get("secret")
        user_password = b64encode(jwt.encode({"username": _user, "password": _password}, user_secret, JWT_ALG)).decode('utf-8')
        if user_password == user.get("password"):
            return {"message": "user {} is successfully logged in".format(_user), "data": {"token": user_password, "id": str(user.get("_id"))}}, 200
        else:
            return {"message": "Invalid password"}

class UserSignup(Resource):
    def post(self):
        req_json = request.get_json()
        try:
            _user = req_json['user']
            _password = req_json['pwd']
            _name = req_json['name']
        except Exception as e:
            print(e)
            return {"message": "username, password, and name are required fields"}, 400

        user_list = mongo.db.user_data.find({},{"_id": 0, "username": 1})
        for user in user_list:
            if user.get("username") == _user:
                return {"message": "username already exists"}, 409

        secret = b64encode(os.urandom(16)).decode('utf-8')
        pwd_token_binary = jwt.encode({
            "username": _user,
            "password": _password
            }, secret, JWT_ALG) 
        pwd_token = b64encode(pwd_token_binary).decode('utf-8')
        query = {
            "username": _user,
            "password": pwd_token,
            "reviewerName": _name,
            "secret": secret
        }
        try:
            mongo.db.user_data.insert_one(query)
            return {"message": "User {} is successfully registered".format(_user)}, 200
        except Exception as e:
            print(e)
            return {"message": "Something went wrong"}