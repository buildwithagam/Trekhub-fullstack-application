from datetime import datetime
from extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    booking_status = db.Column(db.String(20), nullable=False, default='Booked')  # Booked, Cancelled, Completed
    payment_status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending, Paid, Failed
    remarks = db.Column(db.String(255), nullable=True)

    # Relationships
    user = db.relationship('User', back_populates='bookings', lazy=True)
    trek = db.relationship('Trek', back_populates='bookings', lazy=True)
