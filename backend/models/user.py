from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='TREKKER')  # ADMIN, STAFF, TREKKER
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', back_populates='user', lazy=True, cascade="all, delete-orphan")
    staff_profile = db.relationship('StaffProfile', back_populates='user', uselist=False, lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', back_populates='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
