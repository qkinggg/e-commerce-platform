 # app/__init__.py
from flask import Flask, jsonify, make_response, url_for
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_jwt_extended.exceptions import NoAuthorizationError

mongo = PyMongo()   # Flask擴展，用於將Flask應用與MongoDB數據庫集成。
bcrypt = Bcrypt()   # Flask擴展，用於加密和驗證密碼
jwt = JWTManager()  # Flask擴展，用於處理基於JSON Web Tokens (JWT) 的身份驗證。

def create_app():
    app = Flask(__name__)
    jwt = JWTManager(app)

    # 加載 .env 文件
    load_dotenv()
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

    app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # 設置 JWT 位置為 cookie
    app.config['JWT_COOKIE_NAME'] = 'access_token_cookie'  # 設置 cookie 名稱
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # 如果不需要 CSRF 保護，設置為 False

    # 初始化擴展
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 設置錯誤處理
    @app.errorhandler(NoAuthorizationError)
    def handle_auth_error(e):
        response = make_response(jsonify({
            "msg": "Missing or invalid token",
            "redirect": url_for('home.home')
        }), 401)
        return response

    # 處理 token 過期的情況
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        response = make_response(jsonify({
            "msg": "Token has expired",
            "redirect": url_for('auth.login')
        }), 201)
        response.set_cookie('access_token_cookie', '', expires=0)  # 清除特定的 cookie
        return response

    # 註冊藍圖
    from .routes.auth import auth_bp
    from .routes.product import product_bp
    from .routes.cart import cart_bp
    from .routes.order import order_bp
    from .routes.admin import admin_bp
    from app.routes.home import home_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/order')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(home_bp)

    return app
