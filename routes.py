from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Student, Equipment, Loan, Staff, AuditLog
from email_service import send_checkout_email, send_return_confirmation
from decorators import staff_required, admin_required, borrower_required
import uuid

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ===== STUDENTS ENDPOINTS =====

@api_bp.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

@api_bp.route('/students', methods=['POST'])
@login_required
@staff_required
def create_student():
    """Create a new student (staff/admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('first_name') or not data.get('last_name') or not data.get('email'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            program=data.get('program'),
            year_level=data.get('year_level'),
            email=data['email'],
            status=data.get('status', 'active')
        )
        
        db.session.add(student)
        db.session.commit()
        
        # Log action
        log_audit('CREATE', 'students', student.id, {'student': data})
        
        return jsonify(student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict()), 200

# ===== EQUIPMENT ENDPOINTS =====

@api_bp.route('/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment"""
    equipment = Equipment.query.all()
    return jsonify([e.to_dict() for e in equipment]), 200

@api_bp.route('/equipment', methods=['POST'])
@login_required
@staff_required
def create_equipment():
    """Create new equipment (staff/admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Equipment name is required'}), 400
        
        equipment = Equipment(
            name=data['name'],
            model=data.get('model'),
            category=data.get('category'),
            serial_number=data.get('serial_number'),
            condition=data.get('condition', 'Good'),
            availability_status=data.get('availability_status', 'Available')
        )
        
        db.session.add(equipment)
        db.session.commit()
        
        log_audit('CREATE', 'equipment', equipment.id, {'equipment': data})
        
        return jsonify(equipment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/equipment/available', methods=['GET'])
def get_available_equipment():
    """Get only available equipment"""
    equipment = Equipment.query.filter_by(availability_status='Available').all()
    return jsonify([e.to_dict() for e in equipment]), 200

@api_bp.route('/equipment/<equipment_id>', methods=['GET'])
def get_equipment_detail(equipment_id):
    """Get specific equipment details"""
    equipment = Equipment.query.get(equipment_id)
    if not equipment:
        return jsonify({'error': 'Equipment not found'}), 404
    return jsonify(equipment.to_dict()), 200

@api_bp.route('/equipment/<equipment_id>', methods=['PUT'])
@login_required
@staff_required
def update_equipment(equipment_id):
    """Update equipment (staff/admin only)"""
    try:
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            equipment.name = data['name']
        if 'model' in data:
            equipment.model = data['model']
        if 'category' in data:
            equipment.category = data['category']
        if 'serial_number' in data:
            equipment.serial_number = data['serial_number']
        if 'condition' in data:
            equipment.condition = data['condition']
        if 'availability_status' in data:
            equipment.availability_status = data['availability_status']
        
        db.session.commit()
        
        log_audit('UPDATE', 'equipment', equipment.id, {'updated_fields': data})
        
        return jsonify({
            'message': 'Equipment updated successfully',
            'equipment': equipment.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/equipment/<equipment_id>', methods=['DELETE'])
@login_required
@staff_required
def delete_equipment(equipment_id):
    """Delete equipment (staff/admin only)"""
    try:
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        # Check if equipment is on loan
        active_loans = Loan.query.filter_by(equipment_id=equipment_id, status='Borrowed').all()
        if active_loans:
            return jsonify({'error': 'Cannot delete equipment that is currently on loan'}), 400
        
        equipment_name = equipment.name
        db.session.delete(equipment)
        db.session.commit()
        
        log_audit('DELETE', 'equipment', equipment_id, {'name': equipment_name})
        
        return jsonify({
            'message': f'Equipment "{equipment_name}" deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ===== LOANS ENDPOINTS =====

@api_bp.route('/loans/checkout', methods=['POST'])
@login_required
@borrower_required
def checkout_equipment():
    """Create a new loan (checkout equipment)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['student_id', 'equipment_id', 'date_due']
        if not all(field in data for field in required):
            return jsonify({'error': f'Missing required fields: {", ".join(required)}'}), 400
        
        # Check if student exists
        student = Student.query.get(data['student_id'])
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Check if equipment exists
        equipment = Equipment.query.get(data['equipment_id'])
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        # Check if equipment is available
        if equipment.availability_status != 'Available':
            return jsonify({'error': 'Equipment is not available'}), 400
        
        # Create loan
        loan = Loan(
            student_id=data['student_id'],
            equipment_id=data['equipment_id'],
            date_borrowed=datetime.utcnow().date(),
            date_due=datetime.strptime(data['date_due'], '%Y-%m-%d').date(),
            status='Borrowed'
        )
        
        # Update equipment status
        equipment.availability_status = 'On Loan'
        
        db.session.add(loan)
        db.session.commit()
        
        # Send confirmation email
        send_checkout_email(
            student_email=student.email,
            student_name=f"{student.first_name} {student.last_name}",
            equipment_name=equipment.name,
            due_date=loan.date_due.strftime('%Y-%m-%d'),
            loan_id=loan.id
        )
        
        # Log action
        log_audit('CREATE', 'loans', loan.id, {
            'student_id': data['student_id'],
            'equipment_id': data['equipment_id'],
            'date_due': data['date_due']
        })
        
        return jsonify({
            'message': 'Equipment checked out successfully',
            'loan': loan.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/loans', methods=['GET'])
def get_loans():
    """Get all loans"""
    loans = Loan.query.all()
    return jsonify([l.to_dict() for l in loans]), 200

@api_bp.route('/loans/active', methods=['GET'])
def get_active_loans():
    """Get only active loans"""
    loans = Loan.query.filter_by(status='Borrowed').all()
    return jsonify([l.to_dict() for l in loans]), 200

@api_bp.route('/loans/overdue', methods=['GET'])
def get_overdue_loans():
    """Get overdue loans"""
    today = datetime.utcnow().date()
    overdue_loans = Loan.query.filter(
        Loan.status == 'Borrowed',
        Loan.date_due < today
    ).all()
    return jsonify([l.to_dict() for l in overdue_loans]), 200

@api_bp.route('/loans/<loan_id>/return', methods=['POST'])
def return_equipment(loan_id):
    """Return equipment"""
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        if loan.status == 'Returned':
            return jsonify({'error': 'Equipment already returned'}), 400
        
        # Update loan
        loan.date_returned = datetime.utcnow().date()
        loan.status = 'Returned'
        
        # Update equipment status
        equipment = Equipment.query.get(loan.equipment_id)
        equipment.availability_status = 'Available'
        
        db.session.commit()
        
        # Send return confirmation email
        send_return_confirmation(
            student_email=loan.student.email,
            student_name=f"{loan.student.first_name} {loan.student.last_name}",
            equipment_name=equipment.name,
            loan_id=loan.id
        )
        
        # Log action
        log_audit('UPDATE', 'loans', loan.id, {'action': 'return', 'date_returned': loan.date_returned.isoformat()})
        
        return jsonify({
            'message': 'Equipment returned successfully',
            'loan': loan.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/loans/<loan_id>', methods=['GET'])
def get_loan_detail(loan_id):
    """Get loan details"""
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404
    return jsonify(loan.to_dict()), 200

# ===== STAFF ENDPOINTS =====

@api_bp.route('/staff', methods=['GET'])
def get_staff():
    """Get all staff"""
    staff = Staff.query.all()
    return jsonify([s.to_dict() for s in staff]), 200

@api_bp.route('/staff', methods=['POST'])
def create_staff():
    """Create new staff member"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400
        
        staff = Staff(
            name=data['name'],
            email=data['email'],
            role=data.get('role', 'approver')
        )
        
        db.session.add(staff)
        db.session.commit()
        
        log_audit('CREATE', 'staff', staff.id, {'staff': data})
        
        return jsonify(staff.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ===== UTILITY ENDPOINTS =====

def log_audit(action, table_name, record_id, details):
    """Log an audit entry"""
    try:
        audit_log = AuditLog(
            action=action,
            table_name=table_name,
            record_id=record_id,
            details=details
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging audit: {str(e)}")

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@api_bp.route('/audit-logs', methods=['GET'])
def get_audit_logs():
    """Get audit logs"""
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return jsonify([l.to_dict() for l in logs]), 200
