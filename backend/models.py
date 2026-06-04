from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id    = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone      = db.Column(db.String(20))
    address    = db.Column(db.Text)
    role       = db.Column(db.String(20), default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders     = db.relationship('Order', backref='user', lazy=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    restaurant_id = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(150), nullable=False)
    location      = db.Column(db.String(200))
    category      = db.Column(db.String(80))
    rating        = db.Column(db.Float, default=0.0)
    image_url     = db.Column(db.Text)
    description   = db.Column(db.Text)
    is_open       = db.Column(db.Boolean, default=True)
    food_items    = db.relationship('FoodItem', backref='restaurant', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_items=False):
        d = {
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'location': self.location,
            'category': self.category,
            'rating': self.rating,
            'image_url': self.image_url,
            'description': self.description,
            'is_open': self.is_open,
        }
        if include_items:
            d['food_items'] = [item.to_dict() for item in self.food_items]
        return d

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    food_id       = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    name          = db.Column(db.String(150), nullable=False)
    price         = db.Column(db.Float, nullable=False)
    description   = db.Column(db.Text)
    image_url     = db.Column(db.Text)
    category      = db.Column(db.String(80))
    is_available  = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'food_id': self.food_id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'category': self.category,
            'is_available': self.is_available,
        }

class Order(db.Model):
    __tablename__ = 'orders'
    order_id        = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    total_price     = db.Column(db.Float, nullable=False)
    status          = db.Column(db.String(30), default='pending')
    delivery_address = db.Column(db.Text)
    payment_method  = db.Column(db.String(50), default='cash_on_delivery')
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    items           = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_items=False):
        d = {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'total_price': self.total_price,
            'status': self.status,
            'delivery_address': self.delivery_address,
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat(),
        }
        if include_items:
            d['items'] = [i.to_dict() for i in self.items]
        return d

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id      = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    food_id       = db.Column(db.Integer, db.ForeignKey('food_items.food_id'), nullable=False)
    quantity      = db.Column(db.Integer, nullable=False)
    unit_price    = db.Column(db.Float, nullable=False)
    food_item     = db.relationship('FoodItem', lazy=True)

    def to_dict(self):
        return {
            'order_item_id': self.order_item_id,
            'order_id': self.order_id,
            'food_id': self.food_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': round(self.quantity * self.unit_price, 2),
            'food_name': self.food_item.name if self.food_item else None,
            'food_image': self.food_item.image_url if self.food_item else None,
        }
