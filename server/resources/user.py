from flask_restful import Resource, reqparse, request
import jwt
from base64 import b64encode
import os
from common.util import mongo
from bson.json_util import dumps, default
from passlib.context import CryptContext

JWT_ALG = "HS256"
PASSWORD_CONTEXT = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    return PASSWORD_CONTEXT.encrypt(password)

def check_encrypted_password(password, hashed):
    return PASSWORD_CONTEXT.verify(password, hashed)


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
        user = mongo.db.user_data.find_one({"username": _user})
        if user is None:
            return {"message": "User {} does not exist".format(_user)}
        password_match = check_encrypted_password(_password, user.get('password'))
        if password_match:
            token_binary = jwt.encode({
                "username": user.get('username'),
                "reviewerName": user.get('reviewerName'),
                "id": str(user.get('id'))
            }, user.get('secret'), JWT_ALG)
            token = token_binary.decode('utf-8')
            mongo.db.user_data.update_one({'username': user.get('username')}, { '$set': {'session_token': token}})
            return {"message": "user {} is successfully logged in".format(_user), "name": user.get('reviewerName'), "id":str(user.get('_id')), "token": token}, 200
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

        users = mongo.db.user_data.find({"username": _user},{"_id": 0, "username": 1})
        if users.count() >= 1:
            return {"message": "username already exists"}, 409

        secret = b64encode(os.urandom(16)).decode('utf-8')
        encrypted_password = encrypt_password(_password)

        query = {
            "username": _user,
            "password": encrypted_password,
            "reviewerName": _name,
            "secret": secret
        }
        try:
            mongo.db.user_data.insert_one(query)
            return {"message": "User {} is successfully registered".format(_user)}, 200
        except Exception as e:
            print(e)
            return {"message": "Something went wrong"}
