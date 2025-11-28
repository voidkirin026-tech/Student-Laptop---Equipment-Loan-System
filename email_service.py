from flask_mail import Mail, Message
from models import db, EmailLog
from datetime import datetime

mail = Mail()

def send_checkout_email(student_email, student_name, equipment_name, due_date, loan_id):
    """Send checkout confirmation email to student"""
    try:
        subject = f"Equipment Checkout Confirmation - {equipment_name}"
        body = f"""
Dear {student_name},

This is to confirm that you have borrowed the following equipment:

Equipment: {equipment_name}
Due Date: {due_date}

Please ensure to return the equipment by the due date. If you need an extension, 
please contact the IT department as soon as possible.

Best regards,
IT Equipment Loan System
        """
        
        msg = Message(subject=subject, recipients=[student_email], body=body)
        mail.send(msg)
        
        # Log the email
        email_log = EmailLog(
            loan_id=loan_id,
            recipient_email=student_email,
            email_type='checkout_confirmation',
            status='sent'
        )
        db.session.add(email_log)
        db.session.commit()
        
        return True
    except Exception as e:
        print(f"Error sending checkout email: {str(e)}")
        # Log failed email attempt
        email_log = EmailLog(
            loan_id=loan_id,
            recipient_email=student_email,
            email_type='checkout_confirmation',
            status='failed'
        )
        db.session.add(email_log)
        db.session.commit()
        return False

def send_overdue_reminder(student_email, student_name, equipment_name, due_date, days_overdue, loan_id):
    """Send overdue reminder email to student"""
    try:
        subject = f"OVERDUE NOTICE - Please Return {equipment_name}"
        body = f"""
Dear {student_name},

This is a reminder that the following equipment is overdue:

Equipment: {equipment_name}
Due Date: {due_date}
Days Overdue: {days_overdue}

Please return this equipment immediately to the IT department. 
Failure to return equipment may result in disciplinary action.

If you have already returned this item, please disregard this notice.

Best regards,
IT Equipment Loan System
        """
        
        msg = Message(subject=subject, recipients=[student_email], body=body)
        mail.send(msg)
        
        # Log the email
        email_log = EmailLog(
            loan_id=loan_id,
            recipient_email=student_email,
            email_type='overdue_reminder',
            status='sent'
        )
        db.session.add(email_log)
        db.session.commit()
        
        return True
    except Exception as e:
        print(f"Error sending overdue reminder: {str(e)}")
        email_log = EmailLog(
            loan_id=loan_id,
            recipient_email=student_email,
            email_type='overdue_reminder',
            status='failed'
        )
        db.session.add(email_log)
        db.session.commit()
        return False

def send_return_confirmation(student_email, student_name, equipment_name, loan_id):
    """Send return confirmation email"""
    try:
        subject = f"Equipment Return Confirmed - {equipment_name}"
        body = f"""
Dear {student_name},

This is to confirm that your return of the following equipment has been recorded:

Equipment: {equipment_name}

Thank you for using the IT Equipment Loan System.

Best regards,
IT Equipment Loan System
        """
        
        msg = Message(subject=subject, recipients=[student_email], body=body)
        mail.send(msg)
        
        email_log = EmailLog(
            loan_id=loan_id,
            recipient_email=student_email,
            email_type='return_confirmation',
            status='sent'
        )
        db.session.add(email_log)
        db.session.commit()
        
        return True
    except Exception as e:
        print(f"Error sending return confirmation: {str(e)}")
        email_log = EmailLog(
            loan_id=loan_id,
            recipient_email=student_email,
            email_type='return_confirmation',
            status='failed'
        )
        db.session.add(email_log)
        db.session.commit()
        return False
