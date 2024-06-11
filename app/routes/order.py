# app/routes/order.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId

order_bp = Blueprint('order', __name__)

@order_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    # 從當前用戶的購物車中獲取所有項目
    cart_items = list(mongo.db.cart.find({"user_id": user_id}))

    if not cart_items:
        return jsonify({"msg": "Cart is empty"}), 400

    order_items = []
    total_price = 0
    for item in cart_items:
        product = mongo.db.products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            order_items.append({
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "product_name": product["name"],
                "product_price": product["price"]
            })
            total_price += item["quantity"] * product["price"]

    order_id = mongo.db.orders.insert_one({
        "user_id": user_id,
        "items": order_items,
        "total_price": total_price,
        "status": "pending"
    }).inserted_id
    # 清空用戶的購物車
    mongo.db.cart.delete_many({"user_id": user_id})

    return jsonify({"msg": "Order created successfully", "order_id": str(order_id)}), 201

@order_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    # 從 URL 中獲取訂單 ID 並從數據庫中查找對應的訂單
    order = mongo.db.orders.find_one({"_id": ObjectId(order_id), "user_id": user_id})

    if not order:
        return jsonify({"msg": "Order not found"}), 404

    order['_id'] = str(order['_id'])
    return jsonify(order), 200

@order_bp.route('/pay', methods=['POST'])
@jwt_required()
def pay_order():
    data = request.get_json()
    order_id = data.get('order_id')
    user_id = get_jwt_identity()
    # 從數據庫中查找對應的訂單
    order = mongo.db.orders.find_one({"_id": ObjectId(order_id), "user_id": user_id})

    if not order:
        return jsonify({"msg": "Order not found"}), 404

    if order['status'] == 'paid':
        return jsonify({"msg": "Order is already paid"}), 400

    # 假設支付成功
    mongo.db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": "paid"}})

    return jsonify({"msg": "Order paid successfully"}), 200
