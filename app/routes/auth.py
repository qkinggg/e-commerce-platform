 # app/routes/auth.py
from flask import Blueprint, request, jsonify, make_response, render_template, url_for
from app import bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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

        # 登錄後生成 access token
        access_token = create_access_token(identity=email)

        # 設置 Cookie 並返回重定向 URL
        response = make_response(jsonify({
            "msg": "User logged in successfully",
            "redirect": url_for('home.home')
        }), 201)
        response.set_cookie(
            'access_token_cookie',  # 使用正確的 cookie 名稱
            access_token,
            httponly=True,
            samesite='Strict',
            path='/'
        )

        return response
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        print(email, password)

        if not email or not password:
            return jsonify({"msg": "Missing email or password"}), 400

        user = User.find_by_email(email)
        # 如果找到用戶並且密碼匹配，生成一個 JWT 訪問令牌並返回。
        if user and bcrypt.check_password_hash(user['password'], password):
            # 生成 JWT token
            access_token = create_access_token(identity=email)

            # 設置 Cookie 並返回重定向 URL
            response = make_response(jsonify({
                "msg": "User logged in successfully",
                "redirect": url_for('home.home')
            }))
            response.set_cookie(
                'access_token_cookie',  # 使用正確的 cookie 名稱
                access_token,
                httponly=True,
                samesite='Strict',
                path='/'
            )

            return response
        else:
            return jsonify({"msg": "Bad email or password"}), 401

    # 如果是 GET 方法，顯示登錄頁面
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # 從 JWT 中提取當前用戶的身份信息並返回
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
