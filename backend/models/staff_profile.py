from extensions import db

class StaffProfile(db.Model):
    __tablename__ = 'staff_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    experience = db.Column(db.Integer, nullable=True)  # in years
    certifications = db.Column(db.Text, nullable=True)
    emergency_contact = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=True, default='Active')

    # Relationships
    user = db.relationship('User', back_populates='staff_profile', lazy=True)
