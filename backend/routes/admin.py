from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.staff_profile import StaffProfile
from models.trek import Trek
from models.booking import Booking
from extensions import db, cache
from utils.decorators import role_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/dashboard', methods=['GET'])
@role_required('ADMIN')
def dashboard_stats():
    cache_key = "admin_dashboard_stats"
    cached_stats = cache.get(cache_key)
    if cached_stats:
        return jsonify(cached_stats), 200

    total_treks = Trek.query.count()
    total_staff = User.query.filter_by(role='STAFF').count()
    total_trekkers = User.query.filter_by(role='TREKKER').count()
    total_bookings = Booking.query.count()
    
    active_treks = Trek.query.filter(Trek.status.in_(['Open', 'Approved'])).count()
    completed_treks = Trek.query.filter_by(status='Completed').count()

    stats = {
        'total_treks': total_treks,
        'total_staff': total_staff,
        'total_trekkers': total_trekkers,
        'total_bookings': total_bookings,
        'active_treks': active_treks,
        'completed_treks': completed_treks
    }
    cache.set(cache_key, stats, timeout=300)
    return jsonify(stats), 200

# Staff Management
@admin_bp.route('/api/admin/staff', methods=['POST'])
@role_required('ADMIN')
def add_staff():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    experience = data.get('experience')
    certifications = data.get('certifications')
    emergency_contact = data.get('emergency_contact')

    if not email or not password or not name:
        return jsonify({'error': 'Email, password, and name are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User with this email already exists'}), 400

    user = User(email=email, name=name, phone=phone, role='STAFF')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    profile = StaffProfile(
        user_id=user.id,
        experience=int(experience) if experience else 0,
        certifications=certifications,
        emergency_contact=emergency_contact,
        status='Active'
    )
    db.session.add(profile)
    db.session.commit()
    
    cache.delete("admin_dashboard_stats")
    return jsonify({'message': 'Staff added successfully', 'staff_id': user.id}), 201

@admin_bp.route('/api/admin/staff', methods=['GET'])
@role_required('ADMIN')
def get_staff_list():
    search = request.args.get('search', '').strip()
    query = User.query.filter_by(role='STAFF')
    if search:
        query = query.filter(
            db.or_(
                User.name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                User.phone.ilike(f'%{search}%')
            )
        )
    staff_members = query.all()
    res = []
    for s in staff_members:
        p = s.staff_profile
        res.append({
            'id': s.id,
            'name': s.name,
            'email': s.email,
            'phone': s.phone,
            'is_active': s.is_active,
            'is_blacklisted': s.is_blacklisted,
            'experience': p.experience if p else 0,
            'certifications': p.certifications if p else '',
            'emergency_contact': p.emergency_contact if p else '',
            'profile_status': p.status if p else 'Active'
        })
    return jsonify(res), 200

@admin_bp.route('/api/admin/staff/<int:id>', methods=['PUT'])
@role_required('ADMIN')
def update_staff(id):
    user = User.query.filter_by(id=id, role='STAFF').first()
    if not user:
        return jsonify({'error': 'Staff member not found'}), 404

    data = request.get_json() or {}
    if 'name' in data:
        user.name = data['name']
    if 'phone' in data:
        user.phone = data['phone']

    p = user.staff_profile
    if not p:
        p = StaffProfile(user_id=user.id)
        db.session.add(p)
        
    if 'experience' in data:
        p.experience = int(data['experience']) if data['experience'] else 0
    if 'certifications' in data:
        p.certifications = data['certifications']
    if 'emergency_contact' in data:
        p.emergency_contact = data['emergency_contact']
    if 'profile_status' in data:
        p.status = data['profile_status']

    db.session.commit()
    cache.delete("admin_dashboard_stats")
    return jsonify({'message': 'Staff updated successfully'}), 200

@admin_bp.route('/api/admin/staff/<int:id>', methods=['DELETE'])
@role_required('ADMIN')
def delete_staff(id):
    user = User.query.filter_by(id=id, role='STAFF').first()
    if not user:
        return jsonify({'error': 'Staff member not found'}), 404

    db.session.delete(user)
    db.session.commit()
    cache.delete("admin_dashboard_stats")
    return jsonify({'message': 'Staff deleted successfully'}), 200

@admin_bp.route('/api/admin/staff/<int:id>/status', methods=['PUT'])
@role_required('ADMIN')
def toggle_staff_status(id):
    user = User.query.filter_by(id=id, role='STAFF').first()
    if not user:
        return jsonify({'error': 'Staff member not found'}), 404

    data = request.get_json() or {}
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
    if 'is_blacklisted' in data:
        user.is_blacklisted = bool(data['is_blacklisted'])

    db.session.commit()
    cache.delete("admin_dashboard_stats")
    return jsonify({'message': 'Staff status updated successfully'}), 200

# User Management
@admin_bp.route('/api/admin/users', methods=['GET'])
@role_required('ADMIN')
def get_users():
    search = request.args.get('search', '').strip()
    query = User.query.filter_by(role='TREKKER')
    if search:
        query = query.filter(
            db.or_(
                User.name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                User.phone.ilike(f'%{search}%')
            )
        )
    users = query.all()
    res = [{
        'id': u.id,
        'name': u.name,
        'email': u.email,
        'phone': u.phone,
        'is_active': u.is_active,
        'is_blacklisted': u.is_blacklisted,
        'created_at': u.created_at.strftime('%Y-%m-%d')
    } for u in users]
    return jsonify(res), 200

@admin_bp.route('/api/admin/user/<int:id>/status', methods=['PUT'])
@role_required('ADMIN')
def toggle_user_status(id):
    user = User.query.filter_by(id=id, role='TREKKER').first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json() or {}
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
    if 'is_blacklisted' in data:
        user.is_blacklisted = bool(data['is_blacklisted'])

    db.session.commit()
    cache.delete("admin_dashboard_stats")
    return jsonify({'message': 'User status updated successfully'}), 200

# Trek Management
@admin_bp.route('/api/admin/trek', methods=['POST'])
@role_required('ADMIN')
def create_trek():
    data = request.get_json() or {}
    trek_name = data.get('trek_name')
    location = data.get('location')
    description = data.get('description')
    difficulty = data.get('difficulty')
    duration_days = data.get('duration_days')
    total_slots = data.get('total_slots')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    assigned_staff_id = data.get('assigned_staff_id')

    if not trek_name or not location or not difficulty or not duration_days or not total_slots or not start_date_str or not end_date_str:
        return jsonify({'error': 'Missing required trek fields'}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid dates, expected format YYYY-MM-DD'}), 400

    trek = Trek(
        trek_name=trek_name,
        location=location,
        description=description,
        difficulty=difficulty,
        duration_days=int(duration_days),
        total_slots=int(total_slots),
        available_slots=int(total_slots),
        start_date=start_date,
        end_date=end_date,
        status='Pending',
        assigned_staff_id=int(assigned_staff_id) if assigned_staff_id else None
    )
    db.session.add(trek)
    db.session.commit()

    cache.clear()
    return jsonify({'message': 'Trek created successfully', 'trek_id': trek.id}), 201

@admin_bp.route('/api/admin/trek/<int:id>', methods=['PUT'])
@role_required('ADMIN')
def update_trek(id):
    trek = Trek.query.get(id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    data = request.get_json() or {}
    if 'trek_name' in data: trek.trek_name = data['trek_name']
    if 'location' in data: trek.location = data['location']
    if 'description' in data: trek.description = data['description']
    if 'difficulty' in data: trek.difficulty = data['difficulty']
    if 'duration_days' in data: trek.duration_days = int(data['duration_days'])
    if 'total_slots' in data:
        old_total = trek.total_slots
        new_total = int(data['total_slots'])
        diff = new_total - old_total
        trek.total_slots = new_total
        trek.available_slots = max(0, trek.available_slots + diff)
    if 'start_date' in data:
        trek.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    if 'end_date' in data:
        trek.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    if 'assigned_staff_id' in data:
        trek.assigned_staff_id = int(data['assigned_staff_id']) if data['assigned_staff_id'] else None
    if 'status' in data:
        trek.status = data['status']
        if trek.status == 'Completed':
            for b in trek.bookings:
                if b.booking_status == 'Booked':
                    b.booking_status = 'Completed'

    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Trek updated successfully'}), 200

@admin_bp.route('/api/admin/trek/<int:id>', methods=['DELETE'])
@role_required('ADMIN')
def delete_trek(id):
    trek = Trek.query.get(id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    db.session.delete(trek)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Trek deleted successfully'}), 200

# Bookings Management
@admin_bp.route('/api/admin/bookings', methods=['GET'])
@role_required('ADMIN')
def get_all_bookings():
    search = request.args.get('search', '').strip()
    query = Booking.query
    if search:
        query = query.join(User).join(Trek).filter(
            db.or_(
                User.name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                Trek.trek_name.ilike(f'%{search}%'),
                Trek.location.ilike(f'%{search}%')
            )
        )
    bookings = query.all()
    res = [{
        'id': b.id,
        'user_id': b.user.id,
        'user_name': b.user.name,
        'user_email': b.user.email,
        'user_phone': b.user.phone,
        'trek_id': b.trek.id,
        'trek_name': b.trek.trek_name,
        'location': b.trek.location,
        'booking_date': b.booking_date.strftime('%Y-%m-%d %H:%M'),
        'booking_status': b.booking_status,
        'payment_status': b.payment_status,
        'remarks': b.remarks
    } for b in bookings]
    return jsonify(res), 200

# Dynamic Report Trigger API
@admin_bp.route('/api/admin/reports/trigger', methods=['POST'])
@role_required('ADMIN')
def trigger_monthly_report_run():
    from tasks.celery_worker import monthly_report_task
    from flask import current_app
    from datetime import datetime
    try:
        monthly_report_task()
        filename = f"monthly_report_{datetime.utcnow().strftime('%Y_%m')}.html"
        return jsonify({
            'message': 'Monthly report generated successfully',
            'filename': filename
        }), 200
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500


@admin_bp.route('/api/admin/reports/download/<filename>', methods=['GET'])
@role_required('ADMIN')
def download_report(filename):
    import os
    from flask import send_from_directory, current_app
    reports_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'reports')
    filepath = os.path.join(reports_dir, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Report file not found'}), 404
    return send_from_directory(reports_dir, filename, as_attachment=True, download_name=filename)


# Reports / Analytics APIs
@admin_bp.route('/api/admin/reports/statistics', methods=['GET'])
@role_required('ADMIN')
def report_stats():
    difficulty_data = db.session.query(Trek.difficulty, db.func.count(Trek.id)).group_by(Trek.difficulty).all()
    difficulty_map = {diff: count for diff, count in difficulty_data}

    booking_data = db.session.query(Booking.booking_status, db.func.count(Booking.id)).group_by(Booking.booking_status).all()
    booking_map = {status: count for status, count in booking_data}

    bookings = Booking.query.all()
    monthly_map = {}
    for b in bookings:
        month_str = b.booking_date.strftime('%Y-%m')
        monthly_map[month_str] = monthly_map.get(month_str, 0) + 1

    users = User.query.filter_by(role='TREKKER').all()
    growth_map = {}
    for u in users:
        month_str = u.created_at.strftime('%Y-%m')
        growth_map[month_str] = growth_map.get(month_str, 0) + 1

    return jsonify({
        'difficulty': difficulty_map,
        'bookings': booking_map,
        'monthly_bookings': monthly_map,
        'user_growth': growth_map
    }), 200
