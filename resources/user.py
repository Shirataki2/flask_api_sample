from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required

from models.user import UserModel
import hashlib

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="This field can't be blank"
)
user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="This field can't be blank"
)

class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user:
            return user.json()
        return {
            "message": "User Not Found"
        }, 404

    @fresh_jwt_required
    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        cuid = get_jwt_identity()
        if cuid != user_id:
            return {
                "message": "User Token Doesn't Match!"
            }, 400
        if user:
            user.remove_from_db() 
            return {
                "message": "User Successfully Deleted!"
            }, 200
        return {
            "message": "User Not Found"
        }, 404

class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()
        if UserModel.find_user_by_username(data['username']):
            return {
                "message": "User Already Exists!"
            }, 409
        user = UserModel(data['username'], hashlib.sha256(data["password"].encode("utf-8")).hexdigest())
        user.save_to_db()
        return {
            "message": "User %s Created!" % data["username"]
        }

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        user = UserModel.find_user_by_username(data["username"])
        if user and user.password == hashlib.sha256(data["password"].encode("utf-8")).hexdigest():
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {
                "message": "Invalid Credentials"
        }, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        cuid = get_jwt_identity()
        new_token = create_access_token(identity=cuid, fresh=False)
        new_rtoken = create_refresh_token(identity=cuid)
        return {
            "access_token": new_token,
            "refresh_token": new_rtoken
        }, 200

