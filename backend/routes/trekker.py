from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.trek import Trek
from models.booking import Booking
from models.notification import Notification
from extensions import db, cache
from utils.decorators import role_required
from datetime import datetime

trekker_bp = Blueprint('trekker', __name__)
@trekker_bp.route('/api/treks', methods=['GET'])
def get_open_treks():
    location = request.args.get('location', '').strip()
    difficulty = request.args.get('difficulty', '').strip()
    duration_days = request.args.get('duration_days', '').strip()
    start_date_str = request.args.get('start_date', '').strip()
    end_date_str = request.args.get('end_date', '').strip()
    status_param = request.args.get('status')  # None if not provided

    # Create dynamic cache key
    cache_key = f"open_treks_{location}_{difficulty}_{duration_days}_{start_date_str}_{end_date_str}_{status_param}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return jsonify(cached_data), 200

    if status_param == '':
        query = Trek.query
    elif status_param is not None:
        query = Trek.query.filter_by(status=status_param)
    else:
        query = Trek.query.filter_by(status='Open')

    if location:
        query = query.filter(Trek.location.ilike(f'%{location}%'))
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if duration_days:
        try:
            query = query.filter_by(duration_days=int(duration_days))
        except ValueError:
            pass
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            query = query.filter(Trek.start_date >= start_date)
        except ValueError:
            pass
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            query = query.filter(Trek.end_date <= end_date)
        except ValueError:
            pass

    treks = query.all()
    res = [{
        'id': t.id,
        'trek_name': t.trek_name,
        'location': t.location,
        'description': t.description,
        'difficulty': t.difficulty,
        'duration_days': t.duration_days,
        'available_slots': t.available_slots,
        'total_slots': t.total_slots,
        'start_date': t.start_date.strftime('%Y-%m-%d'),
        'end_date': t.end_date.strftime('%Y-%m-%d'),
        'status': t.status
    } for t in treks]

    cache.set(cache_key, res, timeout=300)
    return jsonify(res), 200

@trekker_bp.route('/api/treks/<int:id>', methods=['GET'])
def get_trek_detail(id):
    cache_key = f"trek_detail_{id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return jsonify(cached_data), 200

    trek = Trek.query.get_or_404(id)
    res = {
        'id': trek.id,
        'trek_name': trek.trek_name,
        'location': trek.location,
        'description': trek.description,
        'difficulty': trek.difficulty,
        'duration_days': trek.duration_days,
        'available_slots': trek.available_slots,
        'total_slots': trek.total_slots,
        'start_date': trek.start_date.strftime('%Y-%m-%d'),
        'end_date': trek.end_date.strftime('%Y-%m-%d'),
        'status': trek.status
    }
    cache.set(cache_key, res, timeout=300)
    return jsonify(res), 200

@trekker_bp.route('/api/trekker/book/<int:trek_id>', methods=['POST'])
@role_required('TREKKER')
def book_trek(trek_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.is_blacklisted:
        return jsonify({'error': 'Blacklisted users cannot create bookings'}), 403

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    if trek.status != 'Open':
        return jsonify({'error': 'Bookings are only allowed on Open treks'}), 400

    if trek.available_slots <= 0:
        return jsonify({'error': 'No available slots left'}), 400

    # Check duplicate booking
    existing = Booking.query.filter_by(user_id=user_id, trek_id=trek_id).filter(Booking.booking_status != 'Cancelled').first()
    if existing:
        return jsonify({'error': 'You have already booked this trek'}), 400

    data = request.get_json() or {}
    remarks = data.get('remarks', '')

    booking = Booking(
        user_id=user_id,
        trek_id=trek_id,
        booking_status='Booked',
        payment_status='Pending',
        remarks=remarks
    )
    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()

    cache.clear()
    return jsonify({'message': 'Booking successful', 'booking_id': booking.id}), 201

@trekker_bp.route('/api/trekker/bookings', methods=['GET'])
@role_required('TREKKER')
def get_my_bookings():
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id).all()
    res = [{
        'id': b.id,
        'trek_id': b.trek.id,
        'trek_name': b.trek.trek_name,
        'location': b.trek.location,
        'start_date': b.trek.start_date.strftime('%Y-%m-%d'),
        'end_date': b.trek.end_date.strftime('%Y-%m-%d'),
        'booking_date': b.booking_date.strftime('%Y-%m-%d %H:%M'),
        'booking_status': b.booking_status,
        'payment_status': b.payment_status,
        'remarks': b.remarks
    } for b in bookings]
    return jsonify(res), 200

@trekker_bp.route('/api/trekker/cancel/<int:booking_id>', methods=['POST'])
@role_required('TREKKER')
def cancel_booking(booking_id):
    user_id = int(get_jwt_identity())
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    if booking.user_id != user_id:
        return jsonify({'error': 'Forbidden: You do not own this booking'}), 403

    if booking.booking_status == 'Cancelled':
        return jsonify({'error': 'Booking is already cancelled'}), 400

    if booking.booking_status == 'Completed':
        return jsonify({'error': 'Completed bookings cannot be cancelled'}), 400

    booking.booking_status = 'Cancelled'
    trek = booking.trek
    trek.available_slots += 1
    
    db.session.commit()
    cache.clear()

    return jsonify({'message': 'Booking cancelled successfully'}), 200

@trekker_bp.route('/api/trekker/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json() or {}
    if 'name' in data:
        user.name = data['name']
    if 'phone' in data:
        user.phone = data['phone']

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

@trekker_bp.route('/api/trekker/notifications', methods=['GET'])
@jwt_required()
def get_my_notifications():
    user_id = int(get_jwt_identity())
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    res = [{
        'id': n.id,
        'message': n.message,
        'type': n.type,
        'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
        'is_read': n.is_read
    } for n in notifications]
    return jsonify(res), 200

@trekker_bp.route('/api/trekker/notifications/<int:id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(id):
    user_id = int(get_jwt_identity())
    n = Notification.query.get(id)
    if not n or n.user_id != user_id:
        return jsonify({'error': 'Notification not found'}), 404
    n.is_read = True
    db.session.commit()
    return jsonify({'message': 'Notification marked read'}), 200

@trekker_bp.route('/api/trekker/export-history', methods=['POST'])
@role_required('TREKKER')
def trigger_export_history():
    from tasks.celery_worker import export_user_csv_task
    from flask import current_app
    user_id = int(get_jwt_identity())
    try:
        use_redis = current_app.config.get('REDIS_AVAILABLE', False)
        task = export_user_csv_task.delay(user_id)

        if use_redis:
            return jsonify({'message': 'Export task queued. You will be notified when ready.', 'task_id': task.id}), 202
        else:
            export_user_csv_task(user_id)
            return jsonify({'message': 'Export complete. Check your notifications for the download link.'}), 200
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500


