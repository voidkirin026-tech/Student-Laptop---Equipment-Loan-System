from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db = SQLAlchemy()

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
