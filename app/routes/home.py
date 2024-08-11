# app/routes/home.py
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from app.models import Product

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@jwt_required(optional=True)  # 使用可選的 JWT 驗證
def home():
    verify_jwt_in_request(optional=True)  # 確保在請求中解析 JWT
    current_user = get_jwt_identity()
    if current_user:
        token = get_jwt()['jti']  # 或者其他你用來獲取 token 的方法
    else:
        token = None
    products = Product.find_all()
    return render_template('index.html', products=products, current_user=current_user, access_token=token)
