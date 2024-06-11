# app/routes/cart.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from bson import ObjectId

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    user_id = get_jwt_identity()

    if not product_id or not quantity:
        return jsonify({"msg": "Missing product_id or quantity"}), 400

    # 檢查產品是否存在於 products 集合中
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    cart_item = mongo.db.cart.find_one({"user_id": user_id, "product_id": product_id})

    if cart_item:
        mongo.db.cart.update_one(
            {"_id": cart_item["_id"]},
            {"$inc": {"quantity": quantity}}
        )
    else:
        mongo.db.cart.insert_one({
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        })

    return jsonify({"msg": "Product added to cart"}), 201

@cart_bp.route('/view', methods=['GET'])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    # 查找用戶購物車中的所有項目
    cart_items = list(mongo.db.cart.find({"user_id": user_id}))
    result = []

    for item in cart_items:
        product = mongo.db.products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            item_data = {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "product_name": product["name"],
                "product_price": product["price"]
            }
            result.append(item_data)
        else:
            print(f"產品ID {item['product_id']} 不存在於 products 集合中。")

    return jsonify(result), 200


@cart_bp.route('/remove', methods=['POST'])
@jwt_required()
def remove_from_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = get_jwt_identity()

    if not product_id:
        return jsonify({"msg": "Missing product_id"}), 400

    result = mongo.db.cart.delete_one({"user_id": user_id, "product_id": product_id})

    if result.deleted_count == 0:
        return jsonify({"msg": "Product not found in cart"}), 404

    return jsonify({"msg": "Product removed from cart"}), 200
