from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required, get_raw_jwt
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required, jwt_required

from models.user import UserModel
from models.post import PostModel
import hashlib

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    "text",
    type=str,
    required=True,
    help="This field can't be blank"
)

class Post(Resource):
    def get(self, user_id, post_id):
        user = UserModel.find_user_by_id(user_id)
        post = PostModel.find_posts_by_post_id(post_id)
        if post and user.id == post.uid:
            return post.json()
        return {
            "message": "Post not Found"
        }, 404

    @fresh_jwt_required
    def delete(self, user_id, post_id):
        post = PostModel.find_posts_by_post_id(post_id)
        user = UserModel.find_user_by_id(user_id)
        cuid = get_jwt_identity()
        if post and user:
            if cuid == post.uid and cuid == user.id:
                post.remove_from_db()
                return {
                    "message": "Post %d Successfully Deleted!" % post.id
                }, 200
        if post is None:
            return {
                "message": "IPost not Found"
            }, 404
        return {
            "message": "Invalid Request!"
        }, 400

class NewPost(Resource):
    @fresh_jwt_required
    def post(self):
        data = post_parser.parse_args()
        cuid = get_jwt_identity()
        user = UserModel.query.filter_by(id=cuid).first()
        post = PostModel(data['text'])
        user.posts.append(post)
        post.save_to_db()
        user.save_to_db()
        return {
            "message": "Post <%s> (user #%d[%s]) Successfullty Posted!" % (
                post.text,
                cuid,
                user.username
            ),
            "content": post.json()[0]
        }, 200