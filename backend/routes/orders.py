from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, Order, OrderItem, FoodItem

orders_bp = Blueprint('orders', __name__)

VALID_STATUSES = ('pending', 'accepted', 'preparing', 'out_for_delivery', 'delivered', 'cancelled')

@orders_bp.route('', methods=['POST'])
@jwt_required()
def place_order():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    cart_items = data.get('items', [])
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    total = 0.0
    order_items = []
    for ci in cart_items:
        food = FoodItem.query.get(ci['food_id'])
        if not food or not food.is_available:
            return jsonify({'error': f"Item {ci['food_id']} unavailable"}), 400
        qty = int(ci['quantity'])
        total += food.price * qty
        order_items.append(OrderItem(food_id=food.food_id, quantity=qty, unit_price=food.price))

    order = Order(user_id=user_id, total_price=round(total, 2),
                  delivery_address=data.get('delivery_address'),
                  payment_method=data.get('payment_method', 'cash_on_delivery'))
    db.session.add(order)
    db.session.flush()
    for oi in order_items:
        oi.order_id = order.order_id
        db.session.add(oi)
    db.session.commit()
    return jsonify(order.to_dict(include_items=True)), 201

@orders_bp.route('/my', methods=['GET'])
@jwt_required()
def my_orders():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict(include_items=True) for o in orders])

@orders_bp.route('/<int:oid>', methods=['GET'])
@jwt_required()
def get_order(oid):
    user_id = int(get_jwt_identity())
    claims  = get_jwt()
    order   = Order.query.get_or_404(oid)
    if order.user_id != user_id and claims.get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    return jsonify(order.to_dict(include_items=True))

@orders_bp.route('/<int:oid>/status', methods=['PUT'])
@jwt_required()
def update_status(oid):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    order = Order.query.get_or_404(oid)
    data  = request.get_json()
    status = data.get('status')
    if status not in VALID_STATUSES:
        return jsonify({'error': f'Invalid status. Choose from {VALID_STATUSES}'}), 400
    order.status = status
    db.session.commit()
    return jsonify(order.to_dict())

@orders_bp.route('', methods=['GET'])
@jwt_required()
def all_orders():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Admin only'}), 403
    status = request.args.get('status')
    query  = Order.query.order_by(Order.created_at.desc())
    if status:
        query = query.filter_by(status=status)
    return jsonify([o.to_dict(include_items=True) for o in query.all()])
