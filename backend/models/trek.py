from datetime import datetime
from extensions import db

class Trek(db.Model):
    __tablename__ = 'treks'
    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Moderate, Hard
    duration_days = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending, Approved, Open, Closed, Completed
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', back_populates='trek', lazy=True, cascade="all, delete-orphan")
    assigned_staff = db.relationship('User', foreign_keys=[assigned_staff_id], backref='assigned_treks', lazy=True)
