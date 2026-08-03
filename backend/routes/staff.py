from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.trek import Trek
from models.booking import Booking
from extensions import db, cache
from utils.decorators import role_required

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/api/staff/treks', methods=['GET'])
@role_required('STAFF')
def get_assigned_treks():
    staff_id = int(get_jwt_identity())
    treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()
    res = []
    for t in treks:
        participant_count = Booking.query.filter_by(trek_id=t.id, booking_status='Booked').count()
        res.append({
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
            'status': t.status,
            'participant_count': participant_count
        })
    return jsonify(res), 200

@staff_bp.route('/api/staff/trek/<int:trek_id>', methods=['PUT'])
@role_required('STAFF')
def update_assigned_trek(trek_id):
    staff_id = int(get_jwt_identity())
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    if trek.assigned_staff_id != staff_id:
        return jsonify({'error': 'Forbidden: You are not assigned to this trek'}), 403

    data = request.get_json() or {}
    
    if 'available_slots' in data:
        new_avail = int(data['available_slots'])
        if new_avail < 0 or new_avail > trek.total_slots:
            return jsonify({'error': f'Available slots must be between 0 and {trek.total_slots}'}), 400
        trek.available_slots = new_avail

    if 'status' in data:
        new_status = data['status']
        if new_status not in ['Pending', 'Approved', 'Open', 'Closed', 'Completed']:
            return jsonify({'error': 'Invalid status'}), 400
        trek.status = new_status
        if new_status == 'Completed':
            bookings = Booking.query.filter_by(trek_id=trek.id, booking_status='Booked').all()
            for b in bookings:
                b.booking_status = 'Completed'

    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Trek updated successfully'}), 200

@staff_bp.route('/api/staff/trek/<int:trek_id>/participants', methods=['GET'])
@role_required('STAFF')
def get_trek_participants(trek_id):
    staff_id = int(get_jwt_identity())
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    if trek.assigned_staff_id != staff_id:
        return jsonify({'error': 'Forbidden: You are not assigned to this trek'}), 403

    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    res = []
    for b in bookings:
        u = b.user
        res.append({
            'booking_id': b.id,
            'user_id': u.id,
            'name': u.name,
            'email': u.email,
            'phone': u.phone,
            'booking_date': b.booking_date.strftime('%Y-%m-%d %H:%M'),
            'booking_status': b.booking_status,
            'payment_status': b.payment_status,
            'remarks': b.remarks
        })
    return jsonify(res), 200
