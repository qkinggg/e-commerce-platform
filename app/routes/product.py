# app/routes/product.py
from flask import Blueprint, request, jsonify, current_app
from app import mongo
from bson import ObjectId
from werkzeug.utils import secure_filename
import os

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

@product_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})

    if not product:
        return jsonify({"msg": "Product not found"}), 404

    product['_id'] = str(product['_id'])
    return jsonify(product), 200

@product_bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    update_fields = {}

    if 'name' in data:
        update_fields['name'] = data['name']
    if 'description' in data:
        update_fields['description'] = data['description']
    if 'price' in data:
        update_fields['price'] = data['price']
    if 'stock' in data:
        update_fields['stock'] = data['stock']
    if 'image_url' in data:
        update_fields['image_url'] = data['image_url']

    result = mongo.db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        return jsonify({"msg": "Product not found"}), 404

    return jsonify({"msg": "Product updated successfully"}), 200

@product_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})

    if result.deleted_count == 0:
        return jsonify({"msg": "Product not found"}), 404

    return jsonify({"msg": "Product deleted successfully"}), 200

@product_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"msg": "No image file"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"msg": "File uploaded successfully", "file_path": file_path}), 201

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product_bp.route('/list', methods=['GET'])
def list_products():
    # 從products集合中查找所有用戶並返回JSON
    products = mongo.db.products.find()
    result = []
    for product in products:
        product['_id'] = str(product['_id'])
        result.append(product)
    return jsonify(result), 200
