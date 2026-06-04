from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db, User, Restaurant, FoodItem
import bcrypt
import os

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from routes.auth        import auth_bp
    from routes.restaurants import restaurants_bp
    from routes.orders      import orders_bp

    app.register_blueprint(auth_bp,        url_prefix='/api/v1/auth')
    app.register_blueprint(restaurants_bp, url_prefix='/api/v1/restaurants')
    app.register_blueprint(orders_bp,      url_prefix='/api/v1/orders')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    if User.query.count() > 0:
        return

    # Admin user
    admin_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode()
    admin = User(name='Admin', email='admin@foodhub.com', password_hash=admin_hash,
                 phone='01700000000', address='Dhaka, Bangladesh', role='admin')

    # Demo customer
    cust_hash = bcrypt.hashpw(b'customer123', bcrypt.gensalt()).decode()
    customer = User(name='Rahim Uddin', email='rahim@example.com', password_hash=cust_hash,
                    phone='01711111111', address='Mirpur, Dhaka', role='customer')

    db.session.add_all([admin, customer])

    restaurants = [
        Restaurant(name='Kacchi Bhai', location='Dhanmondi, Dhaka', category='Biryani',
                   rating=4.8, description='Authentic Dhaka-style kacchi biryani since 1980.',
                   image_url='https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80'),
        Restaurant(name='Pizza Haus', location='Gulshan, Dhaka', category='Pizza',
                   rating=4.5, description='Wood-fired Neapolitan pizzas with premium toppings.',
                   image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&q=80'),
        Restaurant(name='Burger Nation', location='Banani, Dhaka', category='Burgers',
                   rating=4.3, description='Smash burgers and loaded fries, made fresh daily.',
                   image_url='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&q=80'),
        Restaurant(name='Momo House', location='Uttara, Dhaka', category='Chinese',
                   rating=4.6, description='Handmade momos and noodles from a Tibetan recipe.',
                   image_url='https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=800&q=80'),
        Restaurant(name='Mezban', location='Old Dhaka', category='BBQ',
                   rating=4.7, description='Traditional mezban beef and seekh kebab platter.',
                   image_url='https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=800&q=80'),
        Restaurant(name='Sushi Zen', location='Bashundhara, Dhaka', category='Japanese',
                   rating=4.4, description='Omakase rolls and fresh sashimi in a calm setting.',
                   image_url='https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&q=80'),
    ]
    db.session.add_all(restaurants)
    db.session.flush()

    menus = {
        0: [  # Kacchi Bhai
            ('Mutton Kacchi Biryani', 320, 'Slow-cooked dum biryani with tender mutton',
             'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80', 'Main'),
            ('Beef Tehari', 250, 'Spiced beef and rice cooked together',
             'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=600&q=80', 'Main'),
            ('Borhani (Large)', 60, 'Spiced yoghurt drink, pairs perfectly with biryani',
             'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=600&q=80', 'Drinks'),
            ('Firni', 80, 'Chilled rice-milk pudding topped with pistachios',
             'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&q=80', 'Dessert'),
        ],
        1: [  # Pizza Haus
            ('Margherita', 450, 'San Marzano tomato, fresh mozzarella, basil',
             'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80', 'Pizza'),
            ('Pepperoni', 550, 'Double pepperoni, mozzarella, tomato sauce',
             'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600&q=80', 'Pizza'),
            ('BBQ Chicken', 580, 'Pulled chicken, red onion, BBQ drizzle',
             'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&q=80', 'Pizza'),
            ('Garlic Bread', 150, 'Toasted with garlic butter and herbs',
             'https://images.unsplash.com/photo-1619531038896-f2b1f4eba25e?w=600&q=80', 'Sides'),
        ],
        2: [  # Burger Nation
            ('Classic Smash Burger', 380, 'Double smash patty, American cheese, special sauce',
             'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&q=80', 'Burgers'),
            ('Crispy Chicken Burger', 350, 'Buttermilk fried chicken, slaw, sriracha mayo',
             'https://images.unsplash.com/photo-1586816001966-79b736744398?w=600&q=80', 'Burgers'),
            ('Loaded Cheese Fries', 180, 'Crispy fries drenched in cheese sauce and jalapeños',
             'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&q=80', 'Sides'),
            ('Chocolate Shake', 200, 'Thick handspun milkshake',
             'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80', 'Drinks'),
        ],
        3: [  # Momo House
            ('Chicken Momo (8 pcs)', 180, 'Steamed dumplings with ginger-garlic filling',
             'https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=600&q=80', 'Momo'),
            ('Beef Fried Momo (8 pcs)', 220, 'Pan-fried with spicy dipping sauce',
             'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=600&q=80', 'Momo'),
            ('Thukpa Noodle Soup', 200, 'Tibetan broth with vegetables and egg noodles',
             'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&q=80', 'Noodles'),
            ('Butter Tea', 80, 'Traditional salted butter tea',
             'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=600&q=80', 'Drinks'),
        ],
        4: [  # Mezban
            ('Mezban Beef Full Plate', 400, 'Slow-cooked beef with rice and salad',
             'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=600&q=80', 'Main'),
            ('Seekh Kebab (6 pcs)', 280, 'Minced beef skewers with mint chutney',
             'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600&q=80', 'BBQ'),
            ('Shami Kebab (4 pcs)', 200, 'Spiced lentil and beef patties',
             'https://images.unsplash.com/photo-1630409351217-bc4fa6422075?w=600&q=80', 'BBQ'),
            ('Lassi (Sweet)', 70, 'Chilled yoghurt drink',
             'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=600&q=80', 'Drinks'),
        ],
        5: [  # Sushi Zen
            ('Salmon Sashimi (6 pcs)', 650, 'Premium Norwegian salmon, soy and wasabi',
             'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=600&q=80', 'Sashimi'),
            ('Dragon Roll (8 pcs)', 750, 'Shrimp tempura, avocado, spicy tuna on top',
             'https://images.unsplash.com/photo-1617196034183-421b4040ed20?w=600&q=80', 'Rolls'),
            ('Edamame', 200, 'Steamed salted soybeans',
             'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=600&q=80', 'Starters'),
            ('Miso Soup', 150, 'Traditional dashi broth with tofu and wakame',
             'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&q=80', 'Soups'),
        ],
    }

    for idx, r in enumerate(restaurants):
        for (name, price, desc, img, cat) in menus[idx]:
            db.session.add(FoodItem(restaurant_id=r.restaurant_id, name=name,
                                    price=price, description=desc, image_url=img, category=cat))

    db.session.commit()
    print("✅ Seed data loaded")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
