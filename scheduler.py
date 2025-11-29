from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from models import db, Loan, Equipment
from email_service import send_overdue_reminder

scheduler = BackgroundScheduler()
app_context = None

def check_overdue_loans():
    """Check for overdue loans and send reminder emails"""
    global app_context
    if not app_context:
        print("App context not available for scheduler")
        return
        
    with app_context.app_context():
        print(f"[{datetime.now()}] Running overdue loan check...")
        
        try:
            # Find all active loans where due date has passed
            today = datetime.utcnow().date()
            overdue_loans = Loan.query.filter(
                Loan.status == 'Borrowed',
                Loan.date_due < today
            ).all()
            
            for loan in overdue_loans:
                days_overdue = (today - loan.date_due).days
                
                # Send reminder email
                success = send_overdue_reminder(
                    student_email=loan.student.email,
                    student_name=f"{loan.student.first_name} {loan.student.last_name}",
                    equipment_name=loan.equipment.name,
                    due_date=loan.date_due.strftime('%Y-%m-%d'),
                    days_overdue=days_overdue,
                    loan_id=loan.id
                )
                
                if success:
                    print(f"Overdue reminder sent to {loan.student.email} for {loan.equipment.name}")
                else:
                    print(f"Failed to send overdue reminder to {loan.student.email}")
            
            if overdue_loans:
                print(f"Processed {len(overdue_loans)} overdue loans")
            else:
                print("No overdue loans found")
                
        except Exception as e:
            print(f"Error in check_overdue_loans: {str(e)}")

def init_scheduler(app):
    """Initialize the APScheduler"""
    global app_context
    app_context = app
    
    scheduler.add_job(
        func=check_overdue_loans,
        trigger="cron",
        hour=8,
        minute=0,
        name="check_overdue_loans",
        misfire_grace_time=900
    )
    
    scheduler.start()
    print("Scheduler started - Daily overdue check at 8:00 AM")

def shutdown_scheduler():
    """Shutdown the scheduler"""
    scheduler.shutdown()
    print("Scheduler shutdown")
