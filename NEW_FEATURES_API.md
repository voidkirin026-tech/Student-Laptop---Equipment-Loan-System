# New Features Implementation - API Documentation

## Overview

This document details all new features implemented to complete the Student Laptop & Equipment Loan System.

## New Database Models

### 1. ReturnDetail Model

Tracks detailed information about equipment returns, including damage assessment and fines.

**Fields:**

- `id` (String, Primary Key)
- `loan_id` (String, Foreign Key to Loan)
- `damage_status` (String): None, Minor, Major, Lost
- `damage_notes` (Text)
- `condition_on_return` (String)
- `days_late` (Integer)
- `late_fine` (Float)
- `damage_fine` (Float)
- `total_fine` (Float)
- `created_at` (DateTime)

### 2. DamageLog Model

Comprehensive tracking of damaged and lost equipment incidents.

**Fields:**

- `id` (String, Primary Key)
- `equipment_id` (String, Foreign Key)
- `student_id` (String, Foreign Key)
- `loan_id` (String, Foreign Key - optional)
- `damage_type` (String): Damage, Lost
- `description` (Text)
- `reported_by` (String)
- `status` (String): Open, In Repair, Resolved
- `repair_cost` (Float)
- `replacement_cost` (Float)
- `created_at` (DateTime)
- `resolved_at` (DateTime)

### 3. Reservation Model

Equipment reservation booking system to prevent double-booking.

**Fields:**

- `id` (String, Primary Key)
- `student_id` (String, Foreign Key)
- `equipment_id` (String, Foreign Key)
- `date_from` (Date)
- `date_to` (Date)
- `status` (String): Pending, Confirmed, Cancelled, Completed
- `notes` (Text)
- `created_at` (DateTime)
- `confirmed_at` (DateTime)

## New API Endpoints

### Reservations Endpoints

#### POST /api/reservations

Create a new equipment reservation.

**Request Body:**

```json
{
  "student_id": "uuid",
  "equipment_id": "uuid",
  "date_from": "2024-01-15",
  "date_to": "2024-01-20",
  "notes": "Optional notes about the reservation"
}
```

**Response:** 201 Created

```json
{
  "id": "uuid",
  "student_id": "uuid",
  "equipment_id": "uuid",
  "date_from": "2024-01-15",
  "date_to": "2024-01-20",
  "status": "Pending",
  "notes": "Optional notes",
  "created_at": "2024-01-10T10:30:00",
  "confirmed_at": null
}
```

**Conflict Detection:**

- Automatically checks for overlapping reservations
- Returns 409 Conflict if equipment is already reserved

#### GET /api/reservations

List all reservations with optional filtering.

**Query Parameters:**

- `page` (int): Page number for pagination (default: 1)
- `status` (string): Filter by status (Pending, Confirmed, Cancelled, Completed)
- `student_id` (string): Filter by student
- `equipment_id` (string): Filter by equipment

**Response:** 200 OK

```json
{
  "data": [
    {
      "id": "uuid",
      "student_id": "uuid",
      "student": { ... },
      "equipment_id": "uuid",
      "equipment": { ... },
      "date_from": "2024-01-15",
      "date_to": "2024-01-20",
      "status": "Pending",
      "notes": "...",
      "created_at": "2024-01-10T10:30:00",
      "confirmed_at": null
    }
  ],
  "total": 15,
  "pages": 1
}
```

#### GET /api/reservations/<reservation_id>

Get a specific reservation.

**Response:** 200 OK (same structure as POST response)

#### PUT /api/reservations/<reservation_id>

Update reservation status or notes.

**Request Body:**

```json
{
  "status": "Confirmed",
  "notes": "Updated notes"
}
```

**Response:** 200 OK (updated reservation)

**Role Requirements:** Staff only

#### DELETE /api/reservations/<reservation_id>

Cancel/delete a reservation.

**Response:** 200 OK

```json
{
  "message": "Reservation deleted successfully"
}
```

**Role Requirements:** Staff only

---

### Damage Logs Endpoints

#### POST /api/damage-logs

Create a new damage/loss report.

**Request Body:**

```json
{
  "equipment_id": "uuid",
  "student_id": "uuid",
  "loan_id": "uuid (optional)",
  "damage_type": "Damage|Lost",
  "description": "Detailed description of damage",
  "repair_cost": 50.00,
  "replacement_cost": 200.00
}
```

**Response:** 201 Created

```json
{
  "id": "uuid",
  "equipment_id": "uuid",
  "equipment": { ... },
  "student_id": "uuid",
  "student": { ... },
  "loan_id": "uuid",
  "damage_type": "Damage",
  "description": "Screen cracked",
  "reported_by": "admin_username",
  "status": "Open",
  "repair_cost": 50.00,
  "replacement_cost": null,
  "created_at": "2024-01-10T10:30:00",
  "resolved_at": null
}
```

**Side Effects:**

- Automatically updates equipment status to "Damaged" or "Lost"
- Creates audit log entry

#### GET /api/damage-logs

List all damage logs with filtering.

**Query Parameters:**

- `page` (int): Page number (default: 1)
- `status` (string): Filter by status (Open, In Repair, Resolved)
- `damage_type` (string): Filter by type (Damage, Lost)
- `equipment_id` (string): Filter by equipment

**Response:** 200 OK

```json
{
  "data": [ ... ],
  "total": 10,
  "pages": 1
}
```

#### PUT /api/damage-logs/<log_id>

Update damage log status or costs.

**Request Body:**

```json
{
  "status": "In Repair",
  "repair_cost": 75.00,
  "replacement_cost": null
}
```

**Response:** 200 OK (updated log)

**Role Requirements:** Staff only

---

### Reporting Endpoints

#### GET /api/reports/equipment-usage

Get equipment usage statistics.

**Response:** 200 OK

```json
[
  {
    "equipment_id": "uuid",
    "equipment_name": "Dell Laptop",
    "total_loans": 25,
    "active_loans": 2
  },
  ...
]
```

#### GET /api/reports/most-borrowed

Get most borrowed equipment report.

**Query Parameters:**

- `limit` (int): Number of items to return (default: 10)

**Response:** 200 OK

```json
[
  {
    "equipment_id": "uuid",
    "equipment_name": "Dell Laptop",
    "category": "Laptop",
    "loan_count": 25
  },
  ...
]
```

#### GET /api/reports/user-activity/<user_id>

Get detailed user activity and borrowing history.

**Response:** 200 OK

```json
{
  "student_id": "uuid",
  "student_name": "John Doe",
  "program": "Computer Science",
  "total_borrowed": 10,
  "active_loans": 1,
  "overdue_loans": 0,
  "damage_count": 1,
  "lost_count": 0,
  "loans": [
    {
      "id": "uuid",
      "equipment_id": "uuid",
      "date_borrowed": "2024-01-05",
      "date_due": "2024-01-12",
      "date_returned": null,
      "status": "Borrowed"
    },
    ...
  ]
}
```

#### GET /api/reports/damage-summary

Get comprehensive damage and loss report.

**Response:** 200 OK

```json
{
  "total_damage_reports": 5,
  "total_lost_items": 2,
  "total_estimated_cost": 650.00,
  "open_issues": 3,
  "by_status": {
    "Open": 3,
    "In Repair": 1,
    "Resolved": 3
  },
  "details": [
    {
      "id": "uuid",
      "equipment_id": "uuid",
      "student_id": "uuid",
      "damage_type": "Damage",
      "description": "Screen cracked",
      "status": "Open",
      "repair_cost": 50.00,
      "created_at": "2024-01-10T10:30:00"
    },
    ...
  ]
}
```

#### GET /api/reports/overdue-loans

Get overdue loans with fine calculations.

**Response:** 200 OK

```json
{
  "total_overdue": 5,
  "total_fines": 125.00,
  "loans": [
    {
      "loan_id": "uuid",
      "student": { ... },
      "equipment": { ... },
      "date_borrowed": "2024-01-01",
      "date_due": "2024-01-08",
      "days_overdue": 2,
      "daily_fine": 5.00,
      "fine_amount": 10.00
    },
    ...
  ]
}
```

---

## Authentication & Authorization

All new endpoints require authentication (`@login_required`).

### Role-Based Access

| Endpoint | Public | Borrower | Staff | Admin |
|----------|--------|----------|-------|-------|
| POST /reservations | ❌ | ✅ | ✅ | ✅ |
| GET /reservations | ❌ | ✅ | ✅ | ✅ |
| GET /reservations/id | ❌ | ✅ | ✅ | ✅ |
| PUT /reservations/id | ❌ | ❌ | ✅ | ✅ |
| DELETE /reservations/id | ❌ | ❌ | ✅ | ✅ |
| POST /damage-logs | ❌ | ❌ | ✅ | ✅ |
| GET /damage-logs | ❌ | ✅ | ✅ | ✅ |
| PUT /damage-logs/id | ❌ | ❌ | ✅ | ✅ |
| GET /reports/* | ❌ | ✅ | ✅ | ✅ |

---

## Error Responses

### 400 Bad Request

```json
{
  "error": "Missing required fields"
}
```

### 404 Not Found

```json
{
  "error": "Equipment not found"
}
```

### 409 Conflict

```json
{
  "error": "Equipment is already reserved for this period"
}
```

### 401 Unauthorized

```json
{
  "error": "Unauthorized access"
}
```

---

## Database Updates Required

Run the following to create the new tables in your database:

```sql
-- The app.py will automatically create these tables when initialized
-- with db.create_all()
```

After deploying the updated code, the Flask app will automatically:

1. Create the `return_details` table
2. Create the `damage_logs` table
3. Create the `reservations` table

---

## Usage Examples

### Create a Reservation

```bash
curl -X POST http://localhost:5000/api/reservations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "student_id": "123e4567-e89b-12d3-a456-426614174000",
    "equipment_id": "550e8400-e29b-41d4-a716-446655440000",
    "date_from": "2024-01-20",
    "date_to": "2024-01-25",
    "notes": "Needed for project"
  }'
```

### Report Damage

```bash
curl -X POST http://localhost:5000/api/damage-logs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "equipment_id": "550e8400-e29b-41d4-a716-446655440000",
    "student_id": "123e4567-e89b-12d3-a456-426614174000",
    "damage_type": "Damage",
    "description": "Screen has visible cracks",
    "repair_cost": 150.00
  }'
```

### Get Usage Report

```bash
curl -X GET "http://localhost:5000/api/reports/equipment-usage" \
  -H "Authorization: Bearer <token>"
```

---

## Integration Notes

- All endpoints are secured with Flask-Login authentication
- Staff-only operations enforce `@staff_required` decorator
- Audit logging is automatically performed for all mutations
- Pagination defaults to 20 items per page
- Fine calculation: $5.00 per day for overdue equipment
- Equipment condition automatically updated when damage is reported
