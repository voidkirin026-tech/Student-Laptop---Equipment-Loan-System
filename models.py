from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication (admin, staff, borrower)"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='borrower')  # admin, staff, borrower
    status = db.Column(db.String(20), default='active')  # active, inactive, disabled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_staff(self):
        """Check if user is staff"""
        return self.role in ['admin', 'staff']
    
    def is_borrower(self):
        """Check if user is borrower"""
        return self.role in ['admin', 'staff', 'borrower']
    
    def can_manage_equipment(self):
        """Check if user can add/edit/delete equipment"""
        return self.role in ['admin', 'staff']
    
    def can_approve_loans(self):
        """Check if user can approve/deny loans"""
        return self.role in ['admin', 'staff']
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'status': self.status
        }

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    program = db.Column(db.String(100))
    year_level = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    loans = db.relationship('Loan', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'program': self.program,
            'year_level': self.year_level,
            'email': self.email,
            'status': self.status
        }

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(200), nullable=False)
    model = db.Column(db.String(100))
    category = db.Column(db.String(100))
    serial_number = db.Column(db.String(100), unique=True)
    condition = db.Column(db.String(50), default='Good')
    availability_status = db.Column(db.String(20), default='Available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    loans = db.relationship('Loan', backref='equipment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Equipment {self.name} ({self.serial_number})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'category': self.category,
            'serial_number': self.serial_number,
            'condition': self.condition,
            'availability_status': self.availability_status
        }

class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    equipment_id = db.Column(db.String(36), db.ForeignKey('equipment.id'), nullable=False)
    date_borrowed = db.Column(db.Date, nullable=False)
    date_due = db.Column(db.Date, nullable=False)
    date_returned = db.Column(db.Date)
    status = db.Column(db.String(20), default='Borrowed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    email_logs = db.relationship('EmailLog', backref='loan', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Loan {self.equipment.name} to {self.student.first_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student': self.student.to_dict() if self.student else None,
            'equipment': self.equipment.to_dict() if self.equipment else None,
            'date_borrowed': self.date_borrowed.isoformat() if self.date_borrowed else None,
            'date_due': self.date_due.isoformat() if self.date_due else None,
            'date_returned': self.date_returned.isoformat() if self.date_returned else None,
            'status': self.status
        }

class Staff(db.Model):
    __tablename__ = 'staff'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(50), default='approver')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Staff {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }

class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    loan_id = db.Column(db.String(36), db.ForeignKey('loans.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    email_type = db.Column(db.String(50), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='sent')
    
    def __repr__(self):
        return f'<EmailLog {self.email_type} to {self.recipient_email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'loan_id': self.loan_id,
            'recipient_email': self.recipient_email,
            'email_type': self.email_type,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'status': self.status
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    action = db.Column(db.String(100), nullable=False)
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.String(36))
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AuditLog {self.action} on {self.table_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ReturnDetail(db.Model):
    """Track return details including damage and fines"""
    __tablename__ = 'return_details'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    loan_id = db.Column(db.String(36), db.ForeignKey('loans.id'), nullable=False, unique=True)
    damage_status = db.Column(db.String(50), default='None')  # None, Minor, Major, Lost
    damage_notes = db.Column(db.Text)
    condition_on_return = db.Column(db.String(50), default='Good')
    days_late = db.Column(db.Integer, default=0)
    late_fine = db.Column(db.Float, default=0.0)
    damage_fine = db.Column(db.Float, default=0.0)
    total_fine = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ReturnDetail {self.loan_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'loan_id': self.loan_id,
            'damage_status': self.damage_status,
            'damage_notes': self.damage_notes,
            'condition_on_return': self.condition_on_return,
            'days_late': self.days_late,
            'late_fine': self.late_fine,
            'damage_fine': self.damage_fine,
            'total_fine': self.total_fine,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DamageLog(db.Model):
    """Track damaged and lost equipment"""
    __tablename__ = 'damage_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    equipment_id = db.Column(db.String(36), db.ForeignKey('equipment.id'), nullable=False)
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    loan_id = db.Column(db.String(36), db.ForeignKey('loans.id'))
    damage_type = db.Column(db.String(50), nullable=False)  # Damage, Lost
    description = db.Column(db.Text)
    reported_by = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Open')  # Open, In Repair, Resolved
    repair_cost = db.Column(db.Float)
    replacement_cost = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    equipment = db.relationship('Equipment', backref='damage_logs')
    student = db.relationship('Student', backref='damage_logs')
    
    def __repr__(self):
        return f'<DamageLog {self.damage_type} for {self.equipment_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'equipment': self.equipment.to_dict() if self.equipment else None,
            'student_id': self.student_id,
            'student': self.student.to_dict() if self.student else None,
            'loan_id': self.loan_id,
            'damage_type': self.damage_type,
            'description': self.description,
            'reported_by': self.reported_by,
            'status': self.status,
            'repair_cost': self.repair_cost,
            'replacement_cost': self.replacement_cost,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

class Reservation(db.Model):
    """Equipment reservation system"""
    __tablename__ = 'reservations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    equipment_id = db.Column(db.String(36), db.ForeignKey('equipment.id'), nullable=False)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Pending, Confirmed, Cancelled, Completed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    
    student = db.relationship('Student', backref='reservations')
    equipment = db.relationship('Equipment', backref='reservations')
    
    def __repr__(self):
        return f'<Reservation {self.student_id} - {self.equipment_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student': self.student.to_dict() if self.student else None,
            'equipment_id': self.equipment_id,
            'equipment': self.equipment.to_dict() if self.equipment else None,
            'date_from': self.date_from.isoformat() if self.date_from else None,
            'date_to': self.date_to.isoformat() if self.date_to else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None
        }
