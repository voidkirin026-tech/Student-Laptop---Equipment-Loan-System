# Quick Reference - New Features

## 📋 What Was Added

### 3 New Database Models

1. **Reservation** - Equipment booking system
2. **DamageLog** - Damage/loss incident tracking
3. **ReturnDetail** - Enhanced return details with fines

### 13 New API Endpoints

#### Reservations (5)

```sql
POST   /api/reservations              - Create reservation
GET    /api/reservations              - List all (with filters)
GET    /api/reservations/<id>         - Get one
PUT    /api/reservations/<id>         - Update
DELETE /api/reservations/<id>         - Cancel
```

#### Damage Logs (3)

```sql
POST   /api/damage-logs               - Report damage/loss
GET    /api/damage-logs               - List all (with filters)
PUT    /api/damage-logs/<id>          - Update status
```

#### Reports (5)

```sql
GET    /api/reports/equipment-usage   - Usage stats
GET    /api/reports/most-borrowed     - Top items
GET    /api/reports/user-activity/<id>- User history
GET    /api/reports/damage-summary    - Damage report
GET    /api/reports/overdue-loans     - Overdue items
```

---

## 🔐 Authentication & Authorization

All endpoints require login.

### Staff-Only Operations

- `PUT /api/reservations/<id>` - Update reservation
- `DELETE /api/reservations/<id>` - Cancel reservation
- `POST /api/damage-logs` - Report damage
- `PUT /api/damage-logs/<id>` - Update damage status

### Accessible to All Logged-In Users

- All GET endpoints (view only)
- `POST /api/reservations` - Create reservation

---

## 💡 Usage Examples

### Create a Reservation

```python
# Python requests example
import requests

payload = {
    "student_id": "student-uuid",
    "equipment_id": "laptop-uuid",
    "date_from": "2024-01-20",
    "date_to": "2024-01-25",
    "notes": "Project work"
}

response = requests.post(
    "http://localhost:5000/api/reservations",
    json=payload,
    headers={"Authorization": "Bearer token"}
)
print(response.json())  # Returns created reservation
```

### Report Equipment Damage

```python
payload = {
    "equipment_id": "laptop-uuid",
    "student_id": "student-uuid",
    "damage_type": "Damage",
    "description": "Screen has cracked",
    "repair_cost": 150.00
}

response = requests.post(
    "http://localhost:5000/api/damage-logs",
    json=payload,
    headers={"Authorization": "Bearer token"}
)
```

### Get Equipment Usage Report

```python
response = requests.get(
    "http://localhost:5000/api/reports/equipment-usage",
    headers={"Authorization": "Bearer token"}
)

# Returns: [
#   {
#     "equipment_id": "...",
#     "equipment_name": "Dell Laptop",
#     "total_loans": 25,
#     "active_loans": 2
#   },
#   ...
# ]
```

### Get User Activity

```python
response = requests.get(
    f"http://localhost:5000/api/reports/user-activity/{student_id}",
    headers={"Authorization": "Bearer token"}
)

# Returns: {
#   "student_name": "John Doe",
#   "total_borrowed": 10,
#   "active_loans": 1,
#   "overdue_loans": 0,
#   "damage_count": 1,
#   "lost_count": 0,
#   "loans": [...]
# }
```

---

## 🗂️ Model Relationships

```text
Reservation ─┬─→ Student
             └─→ Equipment

DamageLog ─┬─→ Equipment
           ├─→ Student
           └─→ Loan (optional)

ReturnDetail → Loan
```

---

## 🔍 Filtering Examples

### Filter Reservations by Status

```sql
GET /api/reservations?status=Pending
GET /api/reservations?status=Confirmed
```

### Filter Damage Logs by Type

```sql
GET /api/damage-logs?damage_type=Damage
GET /api/damage-logs?damage_type=Lost
GET /api/damage-logs?status=Open
```

### Get Most Borrowed (limit)

```sql
GET /api/reports/most-borrowed?limit=5
GET /api/reports/most-borrowed?limit=20
```

---

## ⚙️ Configuration

No new configuration required! All features use existing:

- Database connection (config.py)
- Authentication system (Flask-Login)
- Authorization decorators (@login_required, @staff_required)
- Audit logging (existing log_audit function)

---

## 📊 Data Formats

### Reservation Status Flow

```text
Pending → Confirmed → Completed
       → Cancelled
```

### Damage Status Flow

```text
Open → In Repair → Resolved
```

### Equipment Conditions

```text
Excellent → Good → Fair → Poor → Damaged → Lost
```

---

## 🐛 Common Errors

### 409 Conflict on Reservation

**Cause:** Equipment already reserved for dates
**Solution:** Check GET /api/reservations?equipment_id=X for existing reservations

### 404 Not Found

**Cause:** Invalid student/equipment ID
**Solution:** Verify IDs exist before making request

### 401 Unauthorized

**Cause:** Not authenticated or token expired
**Solution:** Login first, then include auth token in headers

---

## 📈 Performance Tips

1. **Use Pagination**: Default 20 items per page

   ```sql
   GET /api/reservations?page=1
   ```

2. **Filter Early**: Don't fetch all then filter

   ```sql
   GET /api/damage-logs?status=Open
   ```

3. **Aggregate Reports**: Use /reports endpoints instead of manual calculation

4. **Index Foreign Keys**: Database already optimized for common queries

---

## 🚀 Deployment Checklist

- [ ] Update code from repository
- [ ] Backup database (just in case)
- [ ] Restart Flask application
- [ ] Tables auto-created on startup (no migration needed)
- [ ] Test authentication is working
- [ ] Verify first reservation can be created
- [ ] Check damage report form works
- [ ] Confirm report endpoints return data

---

## 📚 Full Documentation

For complete details, see:

- **NEW_FEATURES_API.md** - Full API specification
- **IMPLEMENTATION_SUMMARY.md** - Technical summary
- **models.py** - Model definitions and relationships
- **routes.py** - Endpoint implementations

---

## 🎯 Next Steps

### Frontend Development

- Reservation booking calendar
- Damage report form
- Report dashboards

### Enhancements

- Email notifications for reservations
- Fine payment tracking
- Equipment maintenance scheduling

---

## 📞 Support

All endpoints return JSON with:

- **200 OK**: Success
- **201 Created**: Resource created
- **400 Bad Request**: Missing/invalid fields
- **404 Not Found**: Resource not found
- **409 Conflict**: Conflict (e.g., double booking)
- **401 Unauthorized**: Not authenticated
- **403 Forbidden**: Insufficient permissions

Error responses include `{"error": "description"}` for debugging.
