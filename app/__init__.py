 # app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

mongo = PyMongo()   # Flask擴展，用於將Flask應用與MongoDB數據庫集成。
bcrypt = Bcrypt()   # Flask擴展，用於加密和驗證密碼
jwt = JWTManager()  # Flask擴展，用於處理基於JSON Web Tokens (JWT) 的身份驗證。

def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # 初始化擴展
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.route('/')
    def index():
        return 'Hello, welcome to the E-commerce platform!'

    # 註冊藍圖（在後續步驟中創建）
    from .routes.auth import auth_bp
    from .routes.product import product_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/product')
    '''
    
    from .routes.cart import cart_bp
    from .routes.order import order_bp

    
    
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/order')
    '''
    return app
