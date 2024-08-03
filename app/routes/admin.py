# app/routes/admin.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId

admin_bp = Blueprint('admin', __name__)
'''
# 管理員角色檢查裝飾器
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        print('a', user_id)
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        print('b')
        if user and user.get("role") == "admin":
            print('c')
            return fn(*args, **kwargs)
        else:
            print('d')
            return jsonify({"msg": "Admin access required"}), 403
    return wrapper

@admin_bp.route('/products', methods=['GET'])
@admin_required
def admin_list_products():
    products = list(mongo.db.products.find())
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products), 200

'''