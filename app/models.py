 # app/models.py
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient()
db = client['e_commerce']

class User:
    def __init__(self, email, password, role='user'):
        self.email = email
        self.password = password
        self.role = role

    def save(self):
        user = {
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
        db.users.insert_one(user)

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({"email": email})
    '''
    @staticmethod
    def find_by_id(user_id):
        return db.users.find_one({"_id": ObjectId(user_id)})
    '''
    @staticmethod
    def is_admin(user_id):
        user = User.find_by_email(user_id)
        return user and user.get('role') == 'admin'

class Product:
    def __init__(self, name, description, price, stock, image_url=None):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_url = image_url

    def save(self):
        product = {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image_url": self.image_url
        }
        result = db.products.insert_one(product)
        return result.inserted_id  # 僅返回插入的產品 ID

    @staticmethod
    def find_all():
        return list(db.products.find())

    @staticmethod
    def find_by_id(product_id):
        return db.products.find_one({"_id": ObjectId(product_id)})
    
    @staticmethod
    def update_one(query, update):
        return db.products.update_one(query, update)

    @staticmethod
    def delete_by_id(product_id):
        return db.products.delete_one({"_id": ObjectId(product_id)})

class CartItem:
    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def save(self):
        item = {
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }
        db.cart.insert_one(item)

    @staticmethod
    def find_by_user(user_id):
        return list(db.cart.find({"user_id": user_id}))

    @staticmethod
    def find_one(user_id, product_id):
        return db.cart.find_one({"user_id": user_id, "product_id": product_id})

    @staticmethod
    def update_quantity(user_id, product_id, quantity):
        return db.cart.update_one(
            {"user_id": user_id, "product_id": product_id},
            {"$set": {"quantity": quantity}}
        )

    @staticmethod
    def delete_one(user_id, product_id):
        return db.cart.delete_one({"user_id": user_id, "product_id": product_id})

    @staticmethod
    def delete_all(user_id):
        return db.cart.delete_many({"user_id": user_id})

class Order:
    def __init__(self, user_id, items, total_price, status='pending'):
        self.user_id = user_id
        self.items = items
        self.total_price = total_price
        self.status = status

    def save(self):
        order = {
            "user_id": self.user_id,
            "items": self.items,
            "total_price": self.total_price,
            "status": self.status
        }
        result = db.orders.insert_one(order)
        return result.inserted_id  # 僅返回插入的訂單 ID

    @staticmethod
    def find_all():
        return list(db.orders.find())

    @staticmethod
    def find_by_id_and_user(order_id, user_id):
        return db.orders.find_one({"_id": ObjectId(order_id), "user_id": user_id})

    @staticmethod
    def find_by_id(order_id):
        return db.orders.find_one({"_id": ObjectId(order_id)})

    @staticmethod
    def update_status(order_id, status):
        return db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": status}}
        )
