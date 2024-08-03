# app/routes/product.py
from flask import Blueprint, request, jsonify, current_app
from app import mongo
from app.models import Product
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

    product = Product(name=name, description=description, price=price, stock=stock, image_url=image_url)
    if not product:
        return jsonify({"msg": "Product not found"}), 404
    product_id = product.save()

    return jsonify({"msg": "Product added successfully", "id": str(product_id)}), 201

@product_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.find_by_id(ObjectId(product_id))
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

    result = Product.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        return jsonify({"msg": "Product not found"}), 404

    return jsonify({"msg": "Product updated successfully"}), 200

@product_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = Product.delete_by_id(ObjectId(product_id))

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
    products = Product.find_all()
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products), 200