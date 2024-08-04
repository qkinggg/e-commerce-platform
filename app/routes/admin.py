# app/routes/admin.py
from functools import wraps
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Product, Order, User

admin_bp = Blueprint('admin', __name__)
def admin_required(fn):
    @wraps(fn)  # 確保被裝飾函數的元數據被保留
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        if not User.is_admin(user_id):
            return jsonify({"msg": "Admins only!"}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/products', methods=['GET'])
@admin_required
def admin_list_products():
    products = Product.find_all()
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products), 200

@admin_bp.route('/orders', methods=['GET'])
@admin_required
def admin_list_orders():
    orders = Order.find_all()
    for order in orders:
        order['_id'] = str(order['_id'])
    return jsonify(orders), 200

@admin_bp.route('/product/<product_id>', methods=['DELETE'])
@admin_required
def admin_delete_product(product_id):
    result = Product.delete_by_id(product_id)

    if result.deleted_count == 0:
        return jsonify({"msg": "Product not found"}), 404

    return jsonify({"msg": "Product deleted successfully"}), 200

@admin_bp.route('/order/<order_id>', methods=['PUT'])
@admin_required
def admin_update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({"msg": "Missing status field"}), 400

    result = Order.update_status(order_id, new_status)

    if result.matched_count == 0:
        return jsonify({"msg": "Order not found"}), 404

    return jsonify({"msg": f"Order status updated to {new_status}"}), 200