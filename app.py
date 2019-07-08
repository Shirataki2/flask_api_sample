import os, sys

from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from resources.user import User, UserRegister, UserLogin, TokenRefresh

from database.db import init_db

def create_app(env=None):
    app = Flask(__name__)
    if env is None:
        env = os.getenv('ENV', 'DEV')
    if env.upper() not in ['DEV', 'TEST', 'PROD']:
        print('[E] Unknown env: %s' % env, file=sys.stderr)
        exit(1)
    print("[*] Using %s Config" % env, file=sys.stderr)
    if env == 'PROD':
        app.config.from_object("config.ProdConfig")
    elif env == 'TEST':
        app.config.from_object("config.TestConfig")
    else:
        app.config.from_object("config.DevConfig")
    jwt = JWTManager(app)
    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify({
            "description": "Token has expired!",
            "error": "token_expired"
        }), 401
    @jwt.unauthorized_loader
    def unauthorized_loader_callback(error):
        return jsonify({
            "description": "Access token not found!!",
            "error": "unauthorized_loader"
        }), 401
    @jwt.needs_fresh_token_loader
    def fresh_token_loader_callback():
        return jsonify({
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token"
        }), 401
    CORS(app)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', '')
    init_db(app)
    api = Api(app)
    api.add_resource(User, "/user/<int:user_id>")
    api.add_resource(UserRegister, "/register")
    api.add_resource(UserLogin, "/login")
    api.add_resource(TokenRefresh, "/refresh")
    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=True)

