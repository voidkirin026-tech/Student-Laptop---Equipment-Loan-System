from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Student, Equipment, Loan, Staff, AuditLog, Reservation, DamageLog, ReturnDetail
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
        
        # Validate year_level if provided (7-9 Junior High, 10-12 Senior High, 1-4 College)
        year_level = data.get('year_level')
        if year_level is not None:
            year_level = int(year_level)
            if not ((7 <= year_level <= 12) or (1 <= year_level <= 4)):
                return jsonify({'error': 'Invalid year level. Use 7-9 (Junior High), 10-12 (Senior High), or 1-4 (College)'}), 400
        
        student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            program=data.get('program'),
            year_level=year_level,
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
    """Get all equipment with pagination support"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # If no pagination params provided, return all for backward compatibility
    if not request.args.get('page'):
        equipment = Equipment.query.all()
        return jsonify([e.to_dict() for e in equipment]), 200
    
    # Return paginated data
    paginated = Equipment.query.paginate(page=page, per_page=per_page)
    return jsonify({
        'items': [e.to_dict() for e in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'per_page': per_page
    }), 200

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

# ===== SEARCH & FILTERING ENDPOINTS =====

@api_bp.route('/search/equipment', methods=['GET'])
def search_equipment():
    """Search equipment by name, model, serial, or category"""
    try:
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '')
        condition = request.args.get('condition', '')
        status = request.args.get('status', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Start with all equipment
        q = Equipment.query
        
        # Apply search query
        if query:
            q = q.filter(
                (Equipment.name.ilike(f'%{query}%')) |
                (Equipment.model.ilike(f'%{query}%')) |
                (Equipment.serial_number.ilike(f'%{query}%'))
            )
        
        # Apply filters
        if category:
            q = q.filter_by(category=category)
        if condition:
            q = q.filter_by(condition=condition)
        if status:
            q = q.filter_by(availability_status=status)
        
        # Paginate results
        paginated = q.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'items': [e.to_dict() for e in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/search/students', methods=['GET'])
def search_students():
    """Search students by name, email, or program"""
    try:
        query = request.args.get('q', '').strip()
        program = request.args.get('program', '')
        year_level = request.args.get('year_level', '')
        status = request.args.get('status', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Start with all students
        q = Student.query
        
        # Apply search query
        if query:
            q = q.filter(
                (Student.first_name.ilike(f'%{query}%')) |
                (Student.last_name.ilike(f'%{query}%')) |
                (Student.email.ilike(f'%{query}%'))
            )
        
        # Apply filters
        if program:
            q = q.filter_by(program=program)
        if year_level:
            q = q.filter_by(year_level=int(year_level))
        if status:
            q = q.filter_by(status=status)
        
        # Paginate results
        paginated = q.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'items': [s.to_dict() for s in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/search/loans', methods=['GET'])
def search_loans():
    """Search loans with filters"""
    try:
        student_id = request.args.get('student_id', '')
        equipment_id = request.args.get('equipment_id', '')
        status = request.args.get('status', '')
        overdue_only = request.args.get('overdue_only', 'false').lower() == 'true'
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Start with all loans
        q = Loan.query
        
        # Apply filters
        if student_id:
            q = q.filter_by(student_id=student_id)
        if equipment_id:
            q = q.filter_by(equipment_id=equipment_id)
        if status:
            q = q.filter_by(status=status)
        if overdue_only:
            today = datetime.utcnow().date()
            q = q.filter(
                (Loan.status == 'Borrowed') &
                (Loan.date_due < today)
            )
        
        # Paginate results
        paginated = q.order_by(Loan.date_borrowed.desc()).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'items': [l.to_dict() for l in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/filters/categories', methods=['GET'])
def get_categories():
    """Get all unique equipment categories for filtering"""
    categories = db.session.query(Equipment.category).distinct().filter(
        Equipment.category.isnot(None)
    ).order_by(Equipment.category).all()
    return jsonify([cat[0] for cat in categories if cat[0]]), 200

@api_bp.route('/filters/conditions', methods=['GET'])
def get_conditions():
    """Get all unique equipment conditions for filtering"""
    conditions = ['Excellent', 'Good', 'Fair', 'Poor', 'Damaged']
    return jsonify(conditions), 200

@api_bp.route('/filters/programs', methods=['GET'])
def get_programs():
    """Get all unique student programs for filtering"""
    programs = db.session.query(Student.program).distinct().filter(
        Student.program.isnot(None)
    ).order_by(Student.program).all()
    return jsonify([prog[0] for prog in programs if prog[0]]), 200

# ===== STUDENT EDIT/DELETE ENDPOINTS =====

@api_bp.route('/students/<student_id>', methods=['PUT'])
@login_required
@staff_required
def update_student(student_id):
    """Update student (staff/admin only)"""
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'first_name' in data:
            student.first_name = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
        if 'email' in data:
            student.email = data['email']
        if 'program' in data:
            student.program = data['program']
        if 'year_level' in data:
            student.year_level = data['year_level']
        if 'status' in data:
            student.status = data['status']
        
        db.session.commit()
        
        log_audit('UPDATE', 'students', student.id, {'updated_fields': data})
        
        return jsonify({
            'message': 'Student updated successfully',
            'student': student.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/students/<student_id>', methods=['DELETE'])
@login_required
@staff_required
def delete_student(student_id):
    """Delete student (staff/admin only)"""
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Check if student has active loans
        active_loans = Loan.query.filter_by(student_id=student_id, status='Borrowed').all()
        if active_loans:
            return jsonify({'error': 'Cannot delete student with active loans'}), 400
        
        student_name = f"{student.first_name} {student.last_name}"
        db.session.delete(student)
        db.session.commit()
        
        log_audit('DELETE', 'students', student_id, {'name': student_name})
        
        return jsonify({
            'message': f'Student "{student_name}" deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ===== RETURN WITH DAMAGE TRACKING =====

@api_bp.route('/loans/<loan_id>/return-with-damage', methods=['POST'])
@login_required
def return_equipment_with_damage(loan_id):
    """Return equipment with damage assessment and fine calculation"""
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        if loan.status == 'Returned':
            return jsonify({'error': 'Equipment already returned'}), 400
        
        data = request.get_json()
        damage_status = data.get('damage_status', 'None')  # None, Minor, Major, Lost
        damage_notes = data.get('damage_notes', '')
        new_condition = data.get('new_condition', 'Good')
        
        # Calculate late fine (e.g., $5 per day overdue)
        today = datetime.utcnow().date()
        days_late = max(0, (today - loan.date_due).days)
        late_fine = days_late * 5.00
        
        # Update loan
        loan.date_returned = today
        loan.status = 'Returned'
        
        # Update equipment
        equipment = Equipment.query.get(loan.equipment_id)
        equipment.availability_status = 'Available'
        
        # Update condition if damaged
        if damage_status != 'None':
            if damage_status == 'Lost':
                equipment.condition = 'Damaged'
            else:
                equipment.condition = new_condition
        
        db.session.commit()
        
        # Send return confirmation with damage/fine info
        send_return_confirmation(
            student_email=loan.student.email,
            student_name=f"{loan.student.first_name} {loan.student.last_name}",
            equipment_name=equipment.name,
            loan_id=loan.id,
            damage_status=damage_status,
            late_fine=late_fine,
            days_late=days_late
        )
        
        # Log action
        log_audit('UPDATE', 'loans', loan.id, {
            'action': 'return_with_damage',
            'date_returned': loan.date_returned.isoformat(),
            'damage_status': damage_status,
            'damage_notes': damage_notes,
            'new_condition': new_condition,
            'days_late': days_late,
            'late_fine': late_fine
        })
        
        return jsonify({
            'message': 'Equipment returned successfully',
            'loan': loan.to_dict(),
            'damage_assessment': {
                'damage_status': damage_status,
                'damage_notes': damage_notes,
                'new_condition': new_condition,
                'days_late': days_late,
                'late_fine': late_fine
            }
        }), 200
        
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

# ==================== RESERVATIONS ====================

@api_bp.route('/reservations', methods=['POST'])
@login_required
def create_reservation():
    """Create a new reservation"""
    data = request.get_json()
    
    # Validation
    if not all(k in data for k in ['student_id', 'equipment_id', 'date_from', 'date_to']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if student exists
    student = Student.query.get(data['student_id'])
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Check if equipment exists
    equipment = Equipment.query.get(data['equipment_id'])
    if not equipment:
        return jsonify({'error': 'Equipment not found'}), 404
    
    # Check for conflicts
    from datetime import datetime as dt
    date_from = dt.fromisoformat(data['date_from']).date()
    date_to = dt.fromisoformat(data['date_to']).date()
    
    conflicts = Reservation.query.filter(
        Reservation.equipment_id == data['equipment_id'],
        Reservation.status.in_(['Pending', 'Confirmed']),
        db.or_(
            db.and_(Reservation.date_from <= date_from, Reservation.date_to >= date_from),
            db.and_(Reservation.date_from <= date_to, Reservation.date_to >= date_to),
            db.and_(Reservation.date_from >= date_from, Reservation.date_to <= date_to)
        )
    ).first()
    
    if conflicts:
        return jsonify({'error': 'Equipment is already reserved for this period'}), 409
    
    # Create reservation
    reservation = Reservation(
        student_id=data['student_id'],
        equipment_id=data['equipment_id'],
        date_from=date_from,
        date_to=date_to,
        notes=data.get('notes', '')
    )
    
    db.session.add(reservation)
    db.session.commit()
    
    # Log audit
    log_audit('CREATE', 'Reservation', reservation.id, {'action': 'Reservation created'})
    
    return jsonify(reservation.to_dict()), 201

@api_bp.route('/reservations', methods=['GET'])
@login_required
def get_reservations():
    """Get all reservations with filtering"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    student_id = request.args.get('student_id')
    equipment_id = request.args.get('equipment_id')
    
    query = Reservation.query
    
    if status:
        query = query.filter_by(status=status)
    if student_id:
        query = query.filter_by(student_id=student_id)
    if equipment_id:
        query = query.filter_by(equipment_id=equipment_id)
    
    query = query.order_by(Reservation.created_at.desc())
    reservations = query.paginate(page=page, per_page=20)
    
    return jsonify({
        'data': [r.to_dict() for r in reservations.items],
        'total': reservations.total,
        'pages': reservations.pages
    }), 200

@api_bp.route('/reservations/<reservation_id>', methods=['GET'])
@login_required
def get_reservation(reservation_id):
    """Get specific reservation"""
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    return jsonify(reservation.to_dict()), 200

@api_bp.route('/reservations/<reservation_id>', methods=['PUT'])
@login_required
@staff_required
def update_reservation(reservation_id):
    """Update reservation"""
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    
    data = request.get_json()
    
    if 'status' in data:
        reservation.status = data['status']
        if data['status'] == 'Confirmed':
            reservation.confirmed_at = datetime.utcnow()
    
    if 'notes' in data:
        reservation.notes = data['notes']
    
    db.session.commit()
    log_audit('UPDATE', 'Reservation', reservation_id, {'status': data.get('status')})
    
    return jsonify(reservation.to_dict()), 200

@api_bp.route('/reservations/<reservation_id>', methods=['DELETE'])
@login_required
@staff_required
def delete_reservation(reservation_id):
    """Delete reservation"""
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    
    db.session.delete(reservation)
    db.session.commit()
    log_audit('DELETE', 'Reservation', reservation_id, {'action': 'Reservation deleted'})
    
    return jsonify({'message': 'Reservation deleted successfully'}), 200

# ==================== DAMAGE LOGS ====================

@api_bp.route('/damage-logs', methods=['POST'])
@login_required
@staff_required
def create_damage_log():
    """Create damage log entry"""
    data = request.get_json()
    
    if not all(k in data for k in ['equipment_id', 'student_id', 'damage_type', 'description']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verify references
    equipment = Equipment.query.get(data['equipment_id'])
    student = Student.query.get(data['student_id'])
    
    if not equipment or not student:
        return jsonify({'error': 'Equipment or Student not found'}), 404
    
    damage_log = DamageLog(
        equipment_id=data['equipment_id'],
        student_id=data['student_id'],
        loan_id=data.get('loan_id'),
        damage_type=data['damage_type'],
        description=data['description'],
        reported_by=current_user.username,
        repair_cost=data.get('repair_cost', 0),
        replacement_cost=data.get('replacement_cost', 0)
    )
    
    # Update equipment status if lost
    if data['damage_type'] == 'Lost':
        equipment.availability_status = 'Lost'
        equipment.condition = 'Lost'
    elif data['damage_type'] == 'Damage':
        equipment.condition = 'Damaged'
    
    db.session.add(damage_log)
    db.session.commit()
    
    log_audit('CREATE', 'DamageLog', damage_log.id, {'damage_type': data['damage_type']})
    
    return jsonify(damage_log.to_dict()), 201

@api_bp.route('/damage-logs', methods=['GET'])
@login_required
def get_damage_logs():
    """Get all damage logs"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    damage_type = request.args.get('damage_type')
    equipment_id = request.args.get('equipment_id')
    
    query = DamageLog.query
    
    if status:
        query = query.filter_by(status=status)
    if damage_type:
        query = query.filter_by(damage_type=damage_type)
    if equipment_id:
        query = query.filter_by(equipment_id=equipment_id)
    
    query = query.order_by(DamageLog.created_at.desc())
    logs = query.paginate(page=page, per_page=20)
    
    return jsonify({
        'data': [l.to_dict() for l in logs.items],
        'total': logs.total,
        'pages': logs.pages
    }), 200

@api_bp.route('/damage-logs/<log_id>', methods=['PUT'])
@login_required
@staff_required
def update_damage_log(log_id):
    """Update damage log status"""
    log = DamageLog.query.get(log_id)
    if not log:
        return jsonify({'error': 'Damage log not found'}), 404
    
    data = request.get_json()
    
    if 'status' in data:
        log.status = data['status']
        if data['status'] == 'Resolved':
            log.resolved_at = datetime.utcnow()
    
    if 'repair_cost' in data:
        log.repair_cost = data['repair_cost']
    if 'replacement_cost' in data:
        log.replacement_cost = data['replacement_cost']
    
    db.session.commit()
    log_audit('UPDATE', 'DamageLog', log_id, {'status': data.get('status')})
    
    return jsonify(log.to_dict()), 200

# ==================== REPORTING ====================

@api_bp.route('/reports/equipment-usage', methods=['GET'])
@login_required
def equipment_usage_report():
    """Equipment usage statistics"""
    equipment_stats = db.session.query(
        Equipment.id,
        Equipment.name,
        db.func.count(Loan.id).label('total_loans'),
        db.func.count(db.case([(Loan.status == 'Borrowed', 1)])).label('active_loans')
    ).outerjoin(Loan).group_by(Equipment.id, Equipment.name).all()
    
    data = [{
        'equipment_id': stat[0],
        'equipment_name': stat[1],
        'total_loans': stat[2],
        'active_loans': stat[3]
    } for stat in equipment_stats]
    
    return jsonify(data), 200

@api_bp.route('/reports/most-borrowed', methods=['GET'])
@login_required
def most_borrowed_report():
    """Most borrowed equipment report"""
    limit = request.args.get('limit', 10, type=int)
    
    most_borrowed = db.session.query(
        Equipment.id,
        Equipment.name,
        Equipment.category,
        db.func.count(Loan.id).label('loan_count')
    ).join(Loan).group_by(Equipment.id, Equipment.name, Equipment.category)\
     .order_by(db.func.count(Loan.id).desc()).limit(limit).all()
    
    data = [{
        'equipment_id': item[0],
        'equipment_name': item[1],
        'category': item[2],
        'loan_count': item[3]
    } for item in most_borrowed]
    
    return jsonify(data), 200

@api_bp.route('/reports/user-activity/<user_id>', methods=['GET'])
@login_required
def user_activity_report(user_id):
    """Get user borrowing history and statistics"""
    student = Student.query.get(user_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    loans = Loan.query.filter_by(student_id=user_id).all()
    damage_logs = DamageLog.query.filter_by(student_id=user_id).all()
    
    total_borrowed = len(loans)
    active_loans = len([l for l in loans if l.status == 'Borrowed'])
    overdue_loans = len([l for l in loans if l.date_due < datetime.utcnow().date() and l.status == 'Borrowed'])
    damage_count = len([d for d in damage_logs if d.damage_type == 'Damage'])
    lost_count = len([d for d in damage_logs if d.damage_type == 'Lost'])
    
    return jsonify({
        'student_id': user_id,
        'student_name': f"{student.first_name} {student.last_name}",
        'program': student.program,
        'total_borrowed': total_borrowed,
        'active_loans': active_loans,
        'overdue_loans': overdue_loans,
        'damage_count': damage_count,
        'lost_count': lost_count,
        'loans': [l.to_dict() for l in loans]
    }), 200

@api_bp.route('/reports/damage-summary', methods=['GET'])
@login_required
def damage_summary_report():
    """Damage and loss report summary"""
    damage_logs = DamageLog.query.all()
    
    total_damage = len([d for d in damage_logs if d.damage_type == 'Damage'])
    total_lost = len([d for d in damage_logs if d.damage_type == 'Lost'])
    total_cost = sum([d.repair_cost or 0 for d in damage_logs]) + \
                sum([d.replacement_cost or 0 for d in damage_logs])
    open_issues = len([d for d in damage_logs if d.status == 'Open'])
    
    return jsonify({
        'total_damage_reports': total_damage,
        'total_lost_items': total_lost,
        'total_estimated_cost': total_cost,
        'open_issues': open_issues,
        'by_status': {
            'Open': len([d for d in damage_logs if d.status == 'Open']),
            'In Repair': len([d for d in damage_logs if d.status == 'In Repair']),
            'Resolved': len([d for d in damage_logs if d.status == 'Resolved'])
        },
        'details': [d.to_dict() for d in damage_logs]
    }), 200

@api_bp.route('/reports/overdue-loans', methods=['GET'])
@login_required
def overdue_loans_report():
    """Get overdue loans report"""
    today = datetime.utcnow().date()
    overdue = Loan.query.filter(
        Loan.status == 'Borrowed',
        Loan.date_due < today
    ).all()
    
    data = []
    for loan in overdue:
        days_overdue = (today - loan.date_due).days
        data.append({
            'loan_id': loan.id,
            'student': loan.student.to_dict() if loan.student else None,
            'equipment': loan.equipment.to_dict() if loan.equipment else None,
            'date_borrowed': loan.date_borrowed.isoformat(),
            'date_due': loan.date_due.isoformat(),
            'days_overdue': days_overdue,
            'daily_fine': 5.0,
            'fine_amount': days_overdue * 5.0
        })
    
    return jsonify({
        'total_overdue': len(data),
        'total_fines': sum([item['fine_amount'] for item in data]),
        'loans': data
    }), 200
