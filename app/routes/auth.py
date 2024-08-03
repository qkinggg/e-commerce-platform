 # app/routes/auth.py
from flask import Blueprint, request, jsonify
from app import bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # 從請求中獲取 JSON 數據，並提取 email 和 password
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    if User.find_by_email(email):
        return jsonify({"msg": "User already exists"}), 400
    
    # 將密碼進行哈希處理後插入資料庫
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashed_password, role='user')
    user.save()
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.find_by_email(email)
    # 如果找到用戶並且密碼匹配，生成一個 JWT 訪問令牌並返回。
    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad email or password"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # 從 JWT 中提取當前用戶的身份信息並返回
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
