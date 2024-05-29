 # app/models.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product:
    def __init__(self, name, description, price, stock, image_url):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_url = image_url

class Cart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.products = []

class Order:
    def __init__(self, user_id, products, total_price, status='processing'):
        self.user_id = user_id
        self.products = products
        self.total_price = total_price
        self.status = status
        self.created_at = datetime.now()
        