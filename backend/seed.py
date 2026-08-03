import os
from datetime import datetime
from extensions import db
from models.user import User
from models.trek import Trek
from models.booking import Booking
from models.staff_profile import StaffProfile

def seed_data():
    # Admin User
    admin = User.query.filter_by(email='admin@tma.com').first()
    if not admin:
        admin = User(
            name='TMA Administrator',
            email='admin@tma.com',
            role='ADMIN',
            is_active=True,
            is_blacklisted=False
        )
        admin.set_password('pass123')
        db.session.add(admin)
        db.session.commit()
        print("Autoseeded admin user: admin@tma.com / pass123")
        
    # Sample Staff User
    staff = User.query.filter_by(email='staff@tma.com').first()
    if not staff:
        staff = User(
            name='Trek Guide 1',
            email='staff@tma.com',
            phone='9876543210',
            role='STAFF',
            is_active=True,
            is_blacklisted=False
        )
        staff.set_password('pass123')
        db.session.add(staff)
        db.session.commit()

        # Create Staff Profile
        profile = StaffProfile(
            user_id=staff.id,
            experience=5,
            certifications='Advanced Mountaineering Course (HMI), Wilderness First Aid',
            emergency_contact='Emergency Contact (9999999999)',
            status='Active'
        )
        db.session.add(profile)
        db.session.commit()
        print("Autoseeded staff user: staff@tma.com / pass123")
        
    # Sample Trekker User
    trekker = User.query.filter_by(email='trekker@tma.com').first()
    if not trekker:
        trekker = User(
            name='John Trekker',
            email='trekker@tma.com',
            phone='1234567890',
            role='TREKKER',
            is_active=True,
            is_blacklisted=False
        )
        trekker.set_password('pass123')
        db.session.add(trekker)
        db.session.commit()
        print("Autoseeded trekker user: trekker@tma.com / pass123")
        
    # Sample Trek
    if Trek.query.count() == 0 and staff:
        t1 = Trek(
            trek_name='Kashmir Great Lakes',
            location='Srinagar, Kashmir',
            description='The Kashmir Great Lakes Trek is arguably the most beautiful trek in India. It climbs to high altitude lakes that are turquoise, green and blue.',
            difficulty='Moderate',
            duration_days=7,
            total_slots=15,
            available_slots=15,
            start_date=datetime(2026, 8, 10),
            end_date=datetime(2026, 8, 17),
            status='Open',
            assigned_staff_id=staff.id
        )
        t2 = Trek(
            trek_name='Valley of Flowers',
            location='Chamoli, Uttarakhand',
            description='A legendary trail that leads to the Valley of Flowers National Park, a UNESCO World Heritage Site filled with rare alpine blooms.',
            difficulty='Easy',
            duration_days=6,
            total_slots=20,
            available_slots=20,
            start_date=datetime(2026, 8, 1),
            end_date=datetime(2026, 8, 7),
            status='Open',
            assigned_staff_id=staff.id
        )
        t3 = Trek(
            trek_name='Roopkund Mystery Lake',
            location='Garhwal, Uttarakhand',
            description='Roopkund is a high altitude glacial lake in the Uttarakhand state of India. It lies in the lap of Trishul massif.',
            difficulty='Hard',
            duration_days=8,
            total_slots=10,
            available_slots=10,
            start_date=datetime(2026, 9, 15),
            end_date=datetime(2026, 9, 23),
            status='Pending',
            assigned_staff_id=staff.id
        )
        db.session.add_all([t1, t2, t3])
        db.session.commit()
        print("Autoseeded sample treks")
