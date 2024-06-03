# app/routes/product.py
from flask import Blueprint, request, jsonify
from app import mongo

product_bp = Blueprint('product', __name__)

@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')
    image_url = data.get('image_url')

    if not name or not price or not stock:
        return jsonify({"msg": "Missing required fields"}), 400
    # 將產品數據插入到 MongoDB 的 products 集合中，並獲取插入的產品 ID。
    product_id = mongo.db.products.insert_one({
        "name": name,
        "description": description,
        "price": price,
        "stock": stock,
        "image_url": image_url
    }).inserted_id
    # 返回一個包含成功消息和產品 ID 的 JSON 響應
    return jsonify({"msg": "Product added successfully", "id": str(product_id)}), 201

@product_bp.route('/list', methods=['GET'])
def list_products():
    # 從products集合中查找所有用戶並返回JSON
    products = mongo.db.products.find()
    result = []
    for product in products:
        product['_id'] = str(product['_id'])
        result.append(product)
    return jsonify(result), 200
