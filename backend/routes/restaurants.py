from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db, Restaurant, FoodItem

restaurants_bp = Blueprint('restaurants', __name__)

def admin_required():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    return None

@restaurants_bp.route('', methods=['GET'])
def list_restaurants():
    q        = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    sort     = request.args.get('sort', 'rating')
    query    = Restaurant.query
    if q:
        query = query.filter(Restaurant.name.ilike(f'%{q}%') | Restaurant.location.ilike(f'%{q}%'))
    if category:
        query = query.filter(Restaurant.category.ilike(f'%{category}%'))
    if sort == 'rating':
        query = query.order_by(Restaurant.rating.desc())
    elif sort == 'name':
        query = query.order_by(Restaurant.name.asc())
    return jsonify([r.to_dict() for r in query.all()])

@restaurants_bp.route('/<int:rid>', methods=['GET'])
def get_restaurant(rid):
    r = Restaurant.query.get_or_404(rid)
    return jsonify(r.to_dict(include_items=True))

@restaurants_bp.route('', methods=['POST'])
@jwt_required()
def create_restaurant():
    err = admin_required()
    if err: return err
    data = request.get_json()
    r = Restaurant(name=data['name'], location=data.get('location'),
                   category=data.get('category'), rating=data.get('rating', 0.0),
                   image_url=data.get('image_url'), description=data.get('description'),
                   is_open=data.get('is_open', True))
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201

@restaurants_bp.route('/<int:rid>', methods=['PUT'])
@jwt_required()
def update_restaurant(rid):
    err = admin_required()
    if err: return err
    r = Restaurant.query.get_or_404(rid)
    data = request.get_json()
    for field in ('name','location','category','rating','image_url','description','is_open'):
        if field in data:
            setattr(r, field, data[field])
    db.session.commit()
    return jsonify(r.to_dict())

@restaurants_bp.route('/<int:rid>', methods=['DELETE'])
@jwt_required()
def delete_restaurant(rid):
    err = admin_required()
    if err: return err
    r = Restaurant.query.get_or_404(rid)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

# --- Food items under a restaurant ---

@restaurants_bp.route('/<int:rid>/items', methods=['GET'])
def list_items(rid):
    items = FoodItem.query.filter_by(restaurant_id=rid).all()
    return jsonify([i.to_dict() for i in items])

@restaurants_bp.route('/<int:rid>/items', methods=['POST'])
@jwt_required()
def create_item(rid):
    err = admin_required()
    if err: return err
    Restaurant.query.get_or_404(rid)
    data = request.get_json()
    item = FoodItem(restaurant_id=rid, name=data['name'], price=data['price'],
                    description=data.get('description'), image_url=data.get('image_url'),
                    category=data.get('category'), is_available=data.get('is_available', True))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@restaurants_bp.route('/items/<int:iid>', methods=['PUT'])
@jwt_required()
def update_item(iid):
    err = admin_required()
    if err: return err
    item = FoodItem.query.get_or_404(iid)
    data = request.get_json()
    for field in ('name','price','description','image_url','category','is_available'):
        if field in data:
            setattr(item, field, data[field])
    db.session.commit()
    return jsonify(item.to_dict())

@restaurants_bp.route('/items/<int:iid>', methods=['DELETE'])
@jwt_required()
def delete_item(iid):
    err = admin_required()
    if err: return err
    item = FoodItem.query.get_or_404(iid)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted'})
