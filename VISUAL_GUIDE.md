# Equipment Loan System - Visual Guide & User Flow

## 🎯 User Journey Map

### IT Staff User Flow

```
┌─────────────────┐
│   IT Staff      │
│   Logs In       │
└────────┬────────┘
         │
         ▼
    ┌────────────────────────────────────────┐
    │   Main Dashboard                       │
    │  ┌──────────────────────────────────┐  │
    │  │ 📊 Key Statistics                │  │
    │  │ • Total Equipment: 6             │  │
    │  │ • Available: 4                   │  │
    │  │ • Active Loans: 2                │  │
    │  │ • Overdue: 1                     │  │
    │  └──────────────────────────────────┘  │
    └────────┬─────────────────────────────┘
             │
    ┌────────┴──────────┬─────────────────┐
    │                   │                 │
    ▼                   ▼                 ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│ Checkout    │  │ Manage       │  │ View Loans   │
│ Equipment   │  │ Equipment    │  │ & Returns    │
└─────────────┘  └──────────────┘  └──────────────┘
    │                   │                 │
    ▼                   ▼                 ▼
Select    Add New    View Active
Student   Equipment  Loans
Select    View       Mark as
Equipment  Inventory  Returned
Set Due    Track
Date       Condition
Submit
```

---

## 📱 System Pages

### 1. Dashboard (`/`)
```
┌────────────────────────────────────────────┐
│  Equipment Loan System          [Menu]     │
├────────────────────────────────────────────┤
│                                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐     │
│  │ Total   │ │Available│ │ Active  │     │
│  │Equipment│ │Equipment│ │ Loans   │     │
│  │    6    │ │    4    │ │    2    │     │
│  └─────────┘ └─────────┘ └─────────┘     │
│                                            │
│  ┌─────────────────────────────────────┐  │
│  │  ⚠️ Overdue Items (1)               │  │
│  ├─────────────────────────────────────┤  │
│  │ Student │ Equipment │ Due │ Days  │  │
│  │ Carlos  │ HDD       │11/14│ 5 day│  │
│  │ [Return]                           │  │
│  └─────────────────────────────────────┘  │
│                                            │
│  ┌─────────────────────────────────────┐  │
│  │  Recent Loans                       │  │
│  ├─────────────────────────────────────┤  │
│  │ Student │ Equipment │ Due │ Status │  │
│  │ Maria   │ MacBook   │12/14│Borrowed│ │
│  │ Juan    │ iPad      │12/10│Borrowed│ │
│  └─────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

### 2. Checkout Equipment (`/checkout`)
```
┌────────────────────────────────────────────┐
│  Equipment Loan System          [Menu]     │
├────────────────────────────────────────────┤
│                                            │
│  Checkout Equipment                        │
│  ┌──────────────────────────────────────┐  │
│  │ Student: [▼ Select Student]          │  │
│  │          □ Juan Dela Cruz            │  │
│  │          □ Maria Santos              │  │
│  │          □ Carlos Reyes              │  │
│  │                                       │  │
│  │ Equipment: [▼ Select Equipment]       │  │
│  │          □ MacBook Pro                │  │
│  │          □ Dell XPS 13                │  │
│  │          □ External HDD               │  │
│  │                                       │  │
│  │ Due Date: [📅 2025-12-15]             │  │
│  │                                       │  │
│  │ [Checkout Equipment] [Clear]          │  │
│  └──────────────────────────────────────┘  │
│                                            │
│ ✅ Success Message:                        │ 
│  Equipment checked out! Email sent.        │
└────────────────────────────────────────────┘
```

### 3. Manage Equipment (`/equipment`)
```
┌────────────────────────────────────────────┐
│  Equipment Loan System          [Menu]     │
├────────────────────────────────────────────┤
│                                            │
│  Equipment Management                      │
│  [+ Add New Equipment]                     │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Add New Equipment (Toggle View)      │  │
│  │ Name: [MacBook Pro]                  │  │
│  │ Category: [Laptop]                   │  │
│  │ Serial: [MLB123456]                  │  │
│  │ Condition: [Good ▼]                  │  │
│  │ [Add] [Cancel]                       │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Equipment Inventory                  │  │
│  ├──────────────────────────────────────┤  │
│  │ Name │ Category │ Serial │ Condition │  │
│  │ MacBook│Laptop │MLB123│Good          │  │
│  │ iPad  │Tablet │IPAD1 │Good           │  │
│  │ HDD   │Storage│WD2TB │Good           │  │
│  │ [Edit] [Edit] [Edit]                 │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

### 4. View Loans (`/loans`)
```
┌────────────────────────────────────────────┐
│  Equipment Loan System          [Menu]     │
├────────────────────────────────────────────┤
│                                            │
│  [All] [Active] [Overdue] [Returned]       │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Loan Management                      │  │
│  ├──────────────────────────────────────┤  │
│  │ Student │Equipment│Borrowed│Due    │  │
│  │ Maria   │MacBook  │11/28   │12/14 │  │
│  │ [Return]                             │  │
│  │                                      │  │
│  │ Juan    │iPad     │11/23   │12/10 │  │
│  │ [Return]                             │  │
│  │                                      │  │
│  │ Carlos  │HDD      │10/29   │11/14 │  │
│  │ OVERDUE ⚠️  [Return]                │  │
│  │                                      │  │
│  │ Ana     │Dell XPS │11/08   │11/18 │  │
│  │ Returned    ✓                       │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

---

## 🔄 System Process Flows

### Checkout Process
```
Start
  │
  ▼
IT Staff selects:
┌─────────────────────┐
│ • Student           │
│ • Equipment         │
│ • Due Date          │
└─────────────────────┘
  │
  ▼
System validates:
┌─────────────────────┐
│ • Student exists?   │
│ • Equipment exists? │
│ • Equipment free?   │
│ • Date valid?       │
└─────────────────────┘
  │
  ├─ ❌ Validation fails → Show error
  │
  ▼ ✅ Valid
Create Loan record:
  • student_id
  • equipment_id
  • date_borrowed
  • date_due
  • status = "Borrowed"
  │
  ▼
Update Equipment:
  • status = "On Loan"
  │
  ▼
Send Email:
  • To: student email
  • Type: checkout_confirmation
  • Include: equipment name, due date
  │
  ▼
Log Audit:
  • Action: CREATE
  • Table: loans
  • Details: checkout info
  │
  ▼
End - Show success
```

### Return Process
```
Start
  │
  ▼
IT Staff clicks "Return"
  │
  ▼
Confirm action
  │
  ├─ Cancel → Return to list
  │
  ▼ Confirm
Update Loan:
  • date_returned = today
  • status = "Returned"
  │
  ▼
Update Equipment:
  • status = "Available"
  │
  ▼
Send Email:
  • To: student email
  • Type: return_confirmation
  • Include: equipment name
  │
  ▼
Log Audit:
  • Action: UPDATE
  • Table: loans
  • Details: return info
  │
  ▼
End - Show success
```

### Daily Overdue Check
```
8:00 AM Daily
  │
  ▼
Scheduler triggers
  │
  ▼
Query database:
Find all loans where:
  • status = "Borrowed"
  • date_due < today
  │
  ▼
For each overdue loan:
  ├─ Calculate days overdue
  ├─ Get student email
  ├─ Get equipment name
  ├─ Send reminder email
  ├─ Log email attempt
  └─ Continue loop
  │
  ▼
Report:
  • X overdue reminders sent
  • Y failed to send
  │
  ▼
End - Next check tomorrow
```

---

## 📊 Database Relationships

```
┌──────────────┐         ┌──────────────┐
│   Student    │         │  Equipment   │
├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │
│ first_name   │         │ name         │
│ last_name    │         │ category     │
│ email        │         │ serial       │
│ status       │         │ status       │
└──────────────┘         └──────────────┘
       ▲                          ▲
       │                          │
       │                          │
       └────────────┬─────────────┘
                    │
                    │ FK
                    │
            ┌───────▼────────┐
            │     Loan       │
            ├────────────────┤
            │ id (PK)        │
            │ student_id(FK) │
            │ equipment_id   │
            │ date_borrowed  │
            │ date_due       │
            │ date_returned  │
            │ status         │
            └────────────────┘
                    │
                    │ 1:N
                    │
            ┌───────▼────────────┐
            │   Email_Log        │
            ├────────────────────┤
            │ id (PK)            │
            │ loan_id (FK)       │
            │ recipient_email    │
            │ email_type         │
            │ sent_at            │
            │ status             │
            └────────────────────┘
```

---

## 🔐 Data Flow

### Request-Response Cycle

```
1. User Action
   │
   ▼
   User clicks "Checkout Equipment"

2. Frontend (JavaScript)
   │
   ▼
   GET /api/students → Display dropdown
   GET /api/equipment/available → Show available items

3. User Submits Form
   │
   ▼
   POST /api/loans/checkout with:
   {
     "student_id": "uuid",
     "equipment_id": "uuid",
     "date_due": "2025-12-31"
   }

4. Backend Processing
   │
   ├─ Validate input
   ├─ Check student exists
   ├─ Check equipment exists
   ├─ Check equipment available
   ├─ Create loan record (DB)
   ├─ Update equipment status (DB)
   ├─ Send confirmation email (SMTP)
   ├─ Log audit entry (DB)
   └─ Return success

5. Frontend Response
   │
   ▼
   Display success message
   Refresh equipment list
   Clear form

6. Database Writes
   │
   ├─ INSERT loans table
   ├─ UPDATE equipment table
   ├─ INSERT email_logs table
   └─ INSERT audit_logs table
```

---

## 📈 System Capacity

```
Maximum Items:
Equipment: 10,000+
Students: 10,000+
Loans: 100,000+

Concurrent Users: 100+
Daily Emails: 5,000+
Daily Transactions: 10,000+

Response Times:
Checkout: < 1s
Email send: 1-5s
Page load: < 2s
Overdue check: < 10s
```

---

## 🎯 Key Decision Points in Flow

### At Checkout
```
❓ Equipment available?
├─ No → Reject checkout, show error
└─ Yes → Proceed with checkout
```

### At Return
```
❓ Loan exists and not returned?
├─ No → Show error
└─ Yes → Process return
```

### At Scheduled Check
```
❓ Loan past due?
├─ No → Skip
└─ Yes → Send reminder email
```

---

## 📝 Status Values

### Equipment Status
```
Available ──────────────────► On Loan
   ▲                              │
   │                              │
   └──────── (After Return) ──────┘
```

### Loan Status
```
Borrowed ───────────────────► Returned
   │                              │
   └─ (Never changes back) ───────┘
```

---

## 🔔 Email Workflow

```
Event: Checkout
  │
  ├─ Trigger: Checkout API called
  ├─ To: Student email
  ├─ Template: Checkout confirmation
  ├─ Include: Equipment, Due date
  ├─ Send via: SMTP
  └─ Log: email_logs table

Event: Overdue Check (Daily 8 AM)
  │
  ├─ Trigger: APScheduler
  ├─ Check: All overdue loans
  ├─ For each:
  │  ├─ To: Student email
  │  ├─ Template: Overdue reminder
  │  ├─ Include: Equipment, Days overdue
  │  ├─ Send via: SMTP
  │  └─ Log: email_logs table

Event: Return
  │
  ├─ Trigger: Return API called
  ├─ To: Student email
  ├─ Template: Return confirmation
  ├─ Include: Equipment name
  ├─ Send via: SMTP
  └─ Log: email_logs table
```

---

## 🎓 System Learning Highlights

### Frontend Technologies Used
- HTML5 (Semantic markup)
- CSS3 (Responsive design, Flexbox, Grid)
- JavaScript (AJAX, DOM manipulation, Event handling)

### Backend Technologies Used
- Python (OOP, decorators, modules)
- Flask (Web framework, routing, templates)
- SQLAlchemy (ORM, relationships, queries)

### Database Concepts
- Normalization (6 tables, no redundancy)
- Foreign keys (Referential integrity)
- Relationships (1:N between tables)
- Constraints (NOT NULL, UNIQUE)

### System Concepts
- REST API design
- Email service integration
- Background task scheduling
- Audit logging
- Status tracking

---

This visual guide helps understand the complete system flow from user action through database storage and background processing.

