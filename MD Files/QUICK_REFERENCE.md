# Equipment Loan System - Quick Reference

## System Workflow

```text
1. IT Staff Logs In
   ↓
2. Adds Equipment (if new)
   ↓
3. Student Requests Equipment
   ↓
4. IT Staff Checks Out Equipment
   → Equipment Status: Available → On Loan
   → Confirmation Email Sent to Student
   ↓
5. Daily at 8 AM - Overdue Check
   → System finds loans past due date
   → Sends reminder emails to students
   ↓
6. Student Returns Equipment
   → Equipment Status: On Loan → Available
   → Return Confirmation Email Sent
```

## Quick Commands

### Start Application

```bash
# Windows
cd "c:\Users\Josef Michael\Desktop\Student Laptop & Equipment Loan System"
venv\Scripts\activate
python app.py

# Linux/Mac
source venv/bin/activate
python app.py
```

Then open: <http://localhost:5000>

### Access System

```http
Dashboard: http://localhost:5000
API Health: http://localhost:5000/api/health
```

### Load Sample Data

```bash
python load_sample_data.py
```

### Test Email

Edit email_service.py to test sending an email directly.

## System Pages

| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | <http://localhost:5000/> | View statistics, overdue items, recent loans |
| Checkout | <http://localhost:5000/checkout> | Log equipment checkout |
| Equipment | <http://localhost:5000/equipment> | Manage inventory |
| Loans | <http://localhost:5000/loans> | View all loans, filter by status |

## API Quick Reference

```bash
# Get all equipment
GET /api/equipment

# Create equipment
POST /api/equipment
{
  "name": "MacBook Pro",
  "category": "Laptop",
  "serial_number": "ABC123"
}

# Checkout equipment
POST /api/loans/checkout
{
  "student_id": "student-uuid",
  "equipment_id": "equipment-uuid",
  "date_due": "2025-12-31"
}

# Return equipment
POST /api/loans/{loan_id}/return

# Get overdue loans
GET /api/loans/overdue

# Get active loans
GET /api/loans/active
```

## Database Important Tables

### Loans Status Values

- `Borrowed` - Equipment currently checked out
- `Returned` - Equipment has been returned

### Equipment Status Values

- `Available` - Equipment ready for checkout
- `On Loan` - Equipment currently checked out

### Email Types Logged

- `checkout_confirmation` - Sent when equipment is checked out
- `return_confirmation` - Sent when equipment is returned
- `overdue_reminder` - Sent daily for overdue items

## Configuration Files

### `.env` - Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/equipment_loan_db
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
SECRET_KEY=your-secret-key
```

### `config.py` - Application Settings

- Database settings
- Email settings
- Flask configuration
- Development/Production modes

## Common Issues & Solutions

### Issue: "Equipment is not available"

**Cause**: Equipment status is "On Loan"
**Solution**: Wait for item to be returned or use available item

### Issue: Emails not sending

**Cause**: SMTP settings incorrect
**Solution**:

1. Check `.env` configuration
2. Verify email credentials
3. Check if SMTP port is correct (587 for Gmail)
4. Enable "Less secure apps" in Gmail

### Issue: Scheduler not running

**Cause**: Flask environment not set to development
**Solution**: Check FLASK_ENV=development in `.env`

### Issue: Database connection failed

**Cause**: PostgreSQL not running or URL wrong
**Solution**:

1. Start PostgreSQL service
2. Verify DATABASE_URL in `.env`
3. Ensure database exists

## Features Summary

✅ Equipment checkout logging with form validation
✅ Automatic status updates (Available ↔ On Loan)
✅ Email notifications (checkout, return, overdue)
✅ Daily scheduled overdue checking at 8:00 AM
✅ Loan tracking and history
✅ Equipment inventory management
✅ Category dropdown with custom category support
✅ Dashboard with real-time statistics
✅ Audit trail of all actions
✅ Email delivery logging
✅ Multiple filter views (All, Active, Overdue, Returned)
✅ Proper error handling and user feedback
✅ Browser-friendly page titles
✅ Data validation throughout

## Performance Expectations

- Checkout: < 1 second
- Page load: < 2 seconds
- Email sending: 1-5 seconds
- Overdue check: < 10 seconds (daily)

## User Roles

### IT Staff

- Add equipment
- Log checkouts
- Process returns
- View all loans
- Monitor overdue items

### System Administrator

- View audit logs
- Configure settings
- Manage staff accounts
- View statistics

## Important Notes

1. **Overdue emails sent daily at 8:00 AM** (configurable)
2. **Email delivery is logged** in email_logs table
3. **All actions audited** in audit_logs table
4. **Database backups recommended** before production
5. **Change SECRET_KEY** before production deployment

## Presentation Talking Points

1. **System Purpose**: Automate equipment checkout and tracking
2. **Key Features**: Automatic status updates, email notifications, scheduled overdue checks
3. **Architecture**: Flask backend, PostgreSQL database, APScheduler for tasks
4. **Database Design**: Normalized schema with audit trail
5. **Automation**: Daily overdue checking and email dispatch
6. **User Experience**: Intuitive web interface for all functions
7. **Scalability**: Can handle many students, equipment, and loans
8. **Reliability**: Email logging, audit trail, error handling

---

**For detailed setup: See SETUP_GUIDE.md**
**For complete documentation: See README.md**
