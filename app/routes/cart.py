# app/routes/cart.py
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import mongo
from app.models import Product, CartItem
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
    product = Product.find_by_id(product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    cart_item = CartItem.find_one(user_id, product_id)
    if cart_item:
        CartItem.update_quantity(user_id, product_id, cart_item['quantity'] + quantity)
    else:
        new_item = CartItem(user_id, product_id, quantity)
        new_item.save()

    return jsonify({"msg": "Product added to cart"}), 201

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    token = None
    if user_id:
        token = get_jwt()['jti']  # 確保這裡獲取的是正確的 JWT token
    # 查找用戶購物車中的所有項目
    cart_items = CartItem.find_by_user(user_id)
    result = []

    for item in cart_items:
        product = Product.find_by_id(item["product_id"])
        if product:
            item_data = {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "product_name": product["name"],
                "product_price": product["price"],
                "product_image": product.get('image_url', 'default.png')  # 使用默認圖片名
            }
            result.append(item_data)

    return render_template('cart.html', cart_items=result, current_user=user_id, access_token=token )

@cart_bp.route('/update', methods=['POST'])
@jwt_required()
def update_cart_item():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    user_id = get_jwt_identity()

    if not product_id or not quantity:
        return jsonify({"msg": "Missing product_id or quantity"}), 400

    product = Product.find_by_id(product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    if quantity <= 0:
        CartItem.delete_one(user_id, product_id)
        return jsonify({"msg": "Product removed from cart"}), 200

    CartItem.update_quantity(user_id, product_id, quantity)
    return jsonify({"msg": "Cart updated successfully"}), 200

@cart_bp.route('/remove', methods=['POST'])
@jwt_required()
def remove_from_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = get_jwt_identity()

    if not product_id:
        return jsonify({"msg": "Missing product_id"}), 400

    result = CartItem.delete_one(user_id, product_id)

    if result.deleted_count == 0:
        return jsonify({"msg": "Product not found in cart"}), 404

    return jsonify({"msg": "Product removed from cart"}), 200
