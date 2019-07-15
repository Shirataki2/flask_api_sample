from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required, get_raw_jwt
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required, jwt_required

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
user_parser.add_argument(
    "email",
    type=str,
    required=False,
)

posts_parser = reqparse.RequestParser()
posts_parser.add_argument(
    "limit",
    type=int,
    required=True,
    help="This field can't be blank"
)
posts_parser.add_argument(
    "offset",
    type=int,
    required=True,
    help="This field can't be blank"
)

ff_parser = reqparse.RequestParser()
ff_parser.add_argument(
    "id",
    type=int,
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

class UserRelationship(Resource):
    @jwt_required
    def get(self):
        cuid = get_jwt_identity()
        user = UserModel.find_user_by_id(_id=cuid)
        if not user:
            return {
                "message": "User Not Found"
            }, 404
        following = user.get_following()
        follower = user.get_follower()
        return {
            "following": [user.json()[0] for user in following],
            "follower": [user.json()[0] for user in follower]
        }, 200

    @fresh_jwt_required
    def post(self):
        cuid = get_jwt_identity()
        user = UserModel.find_user_by_id(_id=cuid)
        if not user:
            return {
                "message": "User Not Found"
            }, 404
        data = ff_parser.parse_args()
        user.follow_user_by_id(data['id'])
        return {
            "message": "User Followed."
        }

    @fresh_jwt_required
    def delete(self):
        cuid = get_jwt_identity()
        user = UserModel.find_user_by_id(_id=cuid)
        if not user:
            return {
                "message": "User Not Found"
            }, 404
        data = ff_parser.parse_args()
        user.unfollow_user_by_id(data['id'])
        return {
            "message": "User Unfollowed."
        }


class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()
        if UserModel.find_user_by_username(data['username']):
            return {
                "message": "User Already Exists!"
            }, 409
        user = UserModel(data['username'], data['email'], hashlib.sha256(data["password"].encode("utf-8")).hexdigest())
        user.save_to_db()
        return {
            "message": "User %s Created!" % data["username"]
        }, 200

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        user = UserModel.find_user_by_username(data["username"])
        if not user:
            return {
                "message": "User not Found"
            }, 404
        if user and user.password == hashlib.sha256(data["password"].encode("utf-8")).hexdigest():
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "id": user.id,
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {
                "message": "Invalid Credentials"
        }, 401

class UserLogout(Resource):
    @jwt_refresh_token_required
    def post(self):
        return {
            "message": "Successfully Logout!"
        }, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        cuid = get_jwt_identity()
        new_token = create_access_token(identity=cuid, fresh=True)
        return {
            "access_token": new_token,
        }, 200

class UserList(Resource):
    def get(self):
        users = UserModel.get_all_users()
        if users:
            return {
                "users": [user.json()[0] for user in users]
            }, 200
        return {
            "message": "Users Not Found"
        }, 404

class MyPost(Resource):
    @jwt_required
    def post(self):
        data = posts_parser.parse_args()
        cuid = get_jwt_identity()
        lim = data['limit']
        off = data['offset']
        posts = UserModel.find_user_by_id(_id=cuid).get_posts(limit=lim, offset=off)
        if posts:
            return {
                "posts": [post.json()[0] for post in posts]
            }, 200
        return {
            "message": "User Not Found"
        }, 404