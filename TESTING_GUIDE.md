# Testing Guide - Equipment Loan System

## Quick Start Testing

### Prerequisites

- Backend running on <http://localhost:5000>
- Frontend running on <http://localhost:3000>
- PostgreSQL running
- Sample data loaded

---

## 1. Manual Testing Walkthrough (15 minutes)

### Phase 1: Authentication Testing (3 min)

**Test 1.1: Register New User

1. Go to <http://localhost:3000>
2. Click "Sign up here" link
3. Fill in form:
   - Email: `testuser@example.com`
   - Password: `TestPassword123`
   - Name: `Test User`
4. Click Register
5. ✅ Should see success message and redirect to login

**Test 1.2: Login with New User

1. Enter credentials from 1.1
2. Click Login
3. ✅ Should see Dashboard page
4. ✅ Username should appear in navbar

**Test 1.3: Login with Admin Account

1. Logout (click name in navbar)
2. Login with:
   - Username: `admin`
   - Password: `admin123`
3. ✅ Should have full access to all pages

### Phase 2: Equipment Management (4 min)

**Test 2.1: View Equipment

1. Click "Equipment" in navbar
2. ✅ Should see list of equipment
3. ✅ Each item shows: Name, Model, Category, Condition, Status

**Test 2.2: Add Equipment (Admin/Staff only)

1. Click "Add Equipment" button
2. Fill in:
   - Name: `Test Laptop`
   - Model: `HP Pavilion`
   - Category: `Laptop`
   - Serial: `TEST12345`
   - Condition: `Good`
3. Click Add
4. ✅ Should appear in list immediately

**Test 2.3: Edit Equipment

1. Click Edit on any equipment
2. Change Condition to `Fair`
3. Click Save
4. ✅ Equipment list should update

**Test 2.4: Delete Equipment

1. Try to delete an available equipment
2. ✅ Should delete successfully
3. Try to delete equipment "On Loan"
4. ✅ Should show error: "Cannot delete equipment on loan"

### Phase 3: Student Management (2 min)

**Test 3.1: View Students

1. Click "Students" in navbar
2. ✅ Should see list of students with programs

**Test 3.2: Add Student

1. Click "Add Student" button
2. Fill in:
   - First Name: `John`
   - Last Name: `Doe`
   - Email: `john@example.com`
   - Program: `Computer Science`
   - Year: `2`
3. Click Add
4. ✅ Should appear in list

### Phase 4: Loan Management (4 min)

**Test 4.1: Create Loan (Checkout)

1. Click "Loans" in navbar
2. Click "New Loan" button
3. Fill in:
   - Student: Select from dropdown
   - Equipment: Select available item
   - Due Date: Select future date
4. Click Checkout
5. ✅ Loan appears in "Active Loans" list
6. ✅ Equipment status changes to "On Loan"

**Test 4.2: View Loan Details

1. Click on any active loan
2. ✅ Should show: Student, Equipment, Due Date, Status
3. ✅ Should have "Return" button

**Test 4.3: Return Equipment

1. Click "Return" on any loan
2. Select Condition from dropdown
3. Optional: Add notes
4. Click Return
5. ✅ Equipment status changes back to "Available"
6. ✅ Loan moves to "Returned" list

**Test 4.4: Overdue Detection

1. Check dashboard for overdue loans
2. ✅ Should show red badge for overdue items
3. ✅ Shows days overdue calculation

### Phase 5: Dashboard (2 min)

**Test 5.1: Statistics

1. Go to Dashboard
2. ✅ Should show:
   - Total equipment
   - Available count
   - Active loans
   - Overdue count

**Test 5.2: Quick Links

1. Click each quick link
2. ✅ Should navigate to correct page

### Phase 6: Dark Mode (0 min)

**Test 6.1: Toggle Dark Mode

1. Click theme toggle in navbar
2. ✅ Page colors should invert
3. Refresh page
4. ✅ Dark mode should persist

### Phase 7: Permissions (3 min)

**Test 7.1: Admin Access*

1. Login as admin
2. ✅ Can access: Equipment, Students, Loans, Dashboard
3. ✅ Can Add, Edit, Delete

**Test 7.2: Staff Access

1. Create staff user (Admin → Users → Add Staff)
2. Login as staff
3. ✅ Can manage equipment and students
4. ✅ Can create loans

**Test 7.3: Borrower Access

1. Create borrower user
2. Login as borrower
3. ✅ Can view dashboard
4. ✅ Can view loans (own only)
5. ✅ Cannot add/edit/delete

---

## 2. Automated Testing Setup

### Unit Tests (Python - pytest)

Create `test_app.py`:

```python
import pytest
from app import create_app
from models import db, User, Equipment, Loan, Student

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 201

def test_login_user(client, app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
    
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.status_code == 200

def test_equipment_crud(client, app):
    # Create
    response = client.post('/api/equipment', json={
        'name': 'Test Laptop',
        'model': 'HP',
        'category': 'Laptop'
    })
    assert response.status_code == 201

def test_loan_checkout(client, app):
    # Setup: Create student and equipment
    response = client.post('/api/loans', json={
        'student_id': 'student123',
        'equipment_id': 'equip123',
        'date_borrowed': '2025-01-01',
        'date_due': '2025-02-01'
    })
    assert response.status_code == 201
```

**Run tests:**

```bash
pip install pytest pytest-cov
pytest test_app.py -v --cov
```

### Frontend Tests (Jest/React Testing Library)

```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest
```

---

## 3. Performance Testing

### Load Testing

**Using Apache Bench:**

```bash
pip install locust
```

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class EquipmentUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_equipment(self):
        self.client.get("/api/equipment")
    
    @task
    def get_loans(self):
        self.client.get("/api/loans")
    
    @task
    def dashboard(self):
        self.client.get("/")
```

Run load test:

```bash
locust -f locustfile.py --host=http://localhost:5000
```

### Stress Testing

Check under load:

- 100 concurrent users
- 1000 requests/minute
- API response times
- Database connection pool

---

## 4. Security Testing

### Test Cases

**4.1: SQL Injection

```text
Try: ' OR '1'='1
Expected: ✅ Should be blocked (SQLAlchemy ORM)
```

**4.2: XSS Attack

```text
Try: <script>alert('XSS')</script>
Expected: ✅ Should be escaped
```

**4.3: Password Hashing

```python
# Verify passwords are hashed
user = User.query.first()
assert user.password_hash != 'plaintext_password'
assert user.check_password('testpass123') == True
```

**4.4: CSRF Protection

```text
Expected: ✅ CSRF tokens in forms
```

---

## 5. Browser Compatibility Testing

### Desktop Browsers

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome 120+ | ✅ Full | Primary target |
| Firefox 121+ | ✅ Full | All features work |
| Safari 17+ | ✅ Full | CSS Grid support |
| Edge 120+ | ✅ Full | Chromium-based |

### Mobile Browsers (See Mobile Testing Section)

---

## 6. Test Results Checklist

### Authentication

- [ ] Register new user
- [ ] Login with correct password
- [ ] Login with wrong password (fails)
- [ ] Logout works
- [ ] Session persists across pages
- [ ] Unauthorized access redirects to login

### Equipment Management

- [ ] View equipment list
- [ ] Add equipment (staff/admin)
- [ ] Edit equipment
- [ ] Delete available equipment
- [ ] Cannot delete equipment on loan
- [ ] Condition dropdown works
- [ ] Category dropdown works

### Student Management

- [ ] View students
- [ ] Add student
- [ ] Edit student
- [ ] Delete student
- [ ] Email validation works

### Loan Management

- [ ] Create loan (checkout)
- [ ] Return equipment
- [ ] Overdue detection works
- [ ] Late fees calculated correctly
- [ ] Equipment status updates
- [ ] Can filter by status

### UI/UX

- [ ] Dark mode toggle
- [ ] Dark mode persists
- [ ] Responsive on desktop
- [ ] Forms validate input
- [ ] Error messages display
- [ ] Loading spinners show
- [ ] Navigation works

### Performance

- [ ] Page loads < 2 seconds
- [ ] Dashboard updates quickly
- [ ] No memory leaks
- [ ] No excessive API calls

### Security

- [ ] Passwords hashed
- [ ] Sessions secure
- [ ] No SQL injection
- [ ] No XSS attacks
- [ ] CSRF protected

---

## 7. Common Issues & Solutions

### Issue: Tests fail with database error

```text
Solution:
1. Ensure PostgreSQL running
2. Check test config uses in-memory SQLite
3. Verify test database exists
```

### Issue: Frontend tests fail to find components

```text
Solution:
1. Check component exports
2. Verify import paths
3. Run: npm install (reinstall deps)
```

### Issue: Load test shows slow response times

```text
Solution:
1. Check database indexes
2. Profile slow queries
3. Add caching
4. Scale horizontally
```

---

## Testing Command Reference

```bash
# Python tests
pytest test_app.py -v
pytest test_app.py --cov

# Frontend tests
npm test
npm run test:coverage

# Load testing
locust -f locustfile.py --host=http://localhost:5000 -u 100 -r 10

# Manual testing
curl http://localhost:5000/api/equipment
curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}'
```

---

**Testing Status:** Ready for full testing cycle
**Est. Time:** 30-45 minutes for complete manual test
**Recommendation:** Run tests before each deployment
