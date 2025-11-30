# 🔐 Authentication & Role-Based Access Control System

## Quick Start

### 1. Login to the System
Visit: **http://localhost:5000/login**

### Test Credentials
```
ADMIN USER:
- Username: admin
- Password: admin123
- Access: Full system access, manage all users

STAFF USER:
- Username: staff1  
- Password: staff123
- Access: Add/edit equipment, manage students, process loans

BORROWER USER:
- Username: borrower1
- Password: borrower123
- Access: Checkout/return equipment only
```

### 2. Create New Account
Click "Sign up here" on the login page or visit: **http://localhost:5000/register**

---

## 🛡️ Security Features

### Password Protection
- All passwords are hashed using **Werkzeug PBKDF2** (industry-standard)
- Passwords are salted automatically
- Passwords are never stored in plaintext
- Never sent in API responses

### Session Management
- **Flask-Login** provides secure session handling
- Sessions expire automatically
- CSRF protection enabled
- Secure cookies

### Role-Based Access Control (RBAC)
Every operation checks user role:
- **Admin** - Can do everything
- **Staff** - Can manage equipment and students
- **Borrower** - Can borrow equipment

---

## 📋 User Roles & Permissions

### Admin Role
```json
{
  "can_add_equipment": true,
  "can_edit_equipment": true,
  "can_delete_equipment": true,
  "can_add_students": true,
  "can_checkout": true,
  "can_return": true,
  "can_manage_users": true,
  "can_view_reports": true,
  "can_approve_loans": true
}
```

### Staff Role
```json
{
  "can_add_equipment": true,
  "can_edit_equipment": true,
  "can_delete_equipment": true,
  "can_add_students": true,
  "can_checkout": true,
  "can_return": true,
  "can_manage_users": false,
  "can_view_reports": true,
  "can_approve_loans": true
}
```

### Borrower Role
```json
{
  "can_add_equipment": false,
  "can_edit_equipment": false,
  "can_delete_equipment": false,
  "can_add_students": false,
  "can_checkout": true,
  "can_return": true,
  "can_manage_users": false,
  "can_view_reports": false,
  "can_approve_loans": false
}
```

---

## 🔑 API Endpoints

### Authentication Endpoints

#### Register New User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "secure_password",
  "role": "borrower"  // optional, defaults to "borrower"
}

Response (201):
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid",
    "username": "john_doe",
    "email": "john@example.com",
    "role": "borrower",
    "status": "active"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

Response (200):
{
  "message": "Login successful",
  "user": {
    "id": "uuid",
    "username": "admin",
    "email": "admin@university.edu",
    "role": "admin",
    "status": "active"
  }
}
```

#### Get Current User
```http
GET /api/auth/current-user

Response (200):
{
  "id": "uuid",
  "username": "admin",
  "email": "admin@university.edu",
  "first_name": "Admin",
  "last_name": "User",
  "role": "admin",
  "status": "active"
}
```

#### Logout
```http
POST /api/auth/logout

Response (200):
{
  "message": "Logged out successfully"
}
```

#### Change Password
```http
PUT /api/auth/users/<user_id>/change-password
Content-Type: application/json

{
  "old_password": "current_password",
  "new_password": "new_secure_password"
}

Response (200):
{
  "message": "Password changed successfully"
}
```

#### Update User Profile (Admin or Self)
```http
PUT /api/auth/users/<user_id>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}

Response (200):
{
  "message": "User updated successfully",
  "user": { ... }
}
```

#### Get All Users (Admin Only)
```http
GET /api/auth/users

Response (200):
[
  {
    "id": "uuid",
    "username": "admin",
    "email": "admin@university.edu",
    "role": "admin",
    "status": "active"
  },
  ...
]
```

#### Disable User (Admin Only)
```http
PUT /api/auth/users/<user_id>/disable

Response (200):
{
  "message": "User disabled successfully",
  "user": { ... }
}
```

---

## 🎯 Protected Routes

### Pages (All Require Login)
- `GET /` - Dashboard
- `GET /students` - Student management
- `GET /checkout` - Equipment checkout
- `GET /equipment` - Equipment management
- `GET /loans` - Loan management

### API Endpoints (Require Login + Role Check)

#### Equipment Management
```
POST /api/equipment          [Staff+]  Add equipment
PUT /api/equipment/<id>      [Staff+]  Edit equipment
DELETE /api/equipment/<id>   [Staff+]  Delete equipment
GET /api/equipment           [Anyone]  View all equipment
GET /api/equipment/<id>      [Anyone]  View equipment details
```

#### Student Management
```
POST /api/students          [Staff+]  Add student
GET /api/students           [Anyone]  View all students
GET /api/students/<id>      [Anyone]  View student details
```

#### Loan Management
```
POST /api/loans/checkout    [Borrower+]  Create loan
GET /api/loans              [Anyone]     View all loans
GET /api/loans/active       [Anyone]     View active loans
GET /api/loans/overdue      [Anyone]     View overdue loans
POST /api/loans/<id>/return [Borrower+]  Return equipment
```

---

## 🔒 Permission Decorators

### For Developers

#### Protect a Route
```python
from flask_login import login_required
from decorators import staff_required, admin_required

# Require login
@app.route('/page')
@login_required
def protected_page():
    return render_template('page.html')

# Require staff or admin
@api.route('/equipment', methods=['POST'])
@login_required
@staff_required
def add_equipment():
    # Only staff and admins reach here
    pass

# Require admin only
@api.route('/users/<user_id>/disable', methods=['PUT'])
@login_required
@admin_required
def disable_user(user_id):
    # Only admins reach here
    pass
```

#### Check in Code
```python
from flask_login import current_user

if current_user.is_admin():
    # Admin-only code
    pass

if current_user.is_staff():
    # Staff and admin code
    pass

if current_user.can_manage_equipment():
    # Can manage equipment
    pass
```

---

## 💡 Common Tasks

### Create a New Admin User
1. Login as admin
2. Go to API endpoint or use admin panel (when created)
3. POST to `/api/auth/register` with `role: "admin"`

### Reset a User's Password
As admin:
```http
PUT /api/auth/users/<user_id>/change-password
{
  "old_password": "any_value",  // Admin bypass
  "new_password": "new_password"
}
```

### Disable a User Account
As admin:
```http
PUT /api/auth/users/<user_id>/disable
```

### Change My Own Password
```http
PUT /api/auth/users/me/change-password
{
  "old_password": "current_password",
  "new_password": "new_password"
}
```

---

## ⚙️ Configuration

### Session Settings
Edit `config.py` to change session behavior:
```python
SESSION_COOKIE_SECURE = True  # Only send over HTTPS
SESSION_COOKIE_HTTPONLY = True  # No JS access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
```

### Password Requirements
Current requirements:
- Minimum 6 characters
- Can contain any character
- Recommend using strong passwords

To change, edit `auth_routes.py` in `/api/auth/register`

---

## 🐛 Troubleshooting

### "Invalid username or password"
- Check username spelling (case-sensitive)
- Verify password is correct
- User account must be active (not disabled)

### "Admin access required"
- You don't have admin role
- Ask admin to change your role
- Admin role is required for user management

### "Staff access required"
- You don't have staff or admin role
- Cannot add/edit/delete equipment with borrower role
- Need staff role for equipment management

### Session Expired
- Login again with your credentials
- Sessions expire after 30 minutes of inactivity
- Check browser cookies are enabled

### Cannot Delete Equipment
- Equipment is currently on loan
- Return the equipment first, then delete
- Delete is not allowed for active loans

---

## 📊 User Management

### View All Users (Admin Only)
```bash
curl -X GET http://localhost:5000/api/auth/users \
  -H "Authorization: Bearer <session_token>"
```

### Update User Details
```bash
curl -X PUT http://localhost:5000/api/auth/users/<user_id> \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe"}'
```

---

## 🔐 Security Best Practices

### For System Administrators
1. ✅ Change default admin password immediately
2. ✅ Use strong passwords (8+ characters, mix of types)
3. ✅ Enable HTTPS in production
4. ✅ Keep database credentials in environment variables
5. ✅ Regular security audits
6. ✅ Monitor audit logs for suspicious activity
7. ✅ Disable unused accounts
8. ✅ Update Flask and dependencies regularly

### For Users
1. ✅ Never share your password
2. ✅ Use unique passwords
3. ✅ Logout when done
4. ✅ Use strong passwords
5. ✅ Report suspicious activity

---

## 📈 Audit Trail

All user actions are logged with:
- User ID
- Action type (CREATE, UPDATE, DELETE)
- Table affected
- Timestamp
- Details of change

View audit logs:
```http
GET /api/audit-logs
```

---

## 🚀 Production Deployment

### Before Going Live
1. Change all default passwords
2. Set up HTTPS/SSL
3. Use environment variables for secrets
4. Enable CSRF protection
5. Set secure cookie flags
6. Configure email verification
7. Set up password reset
8. Enable rate limiting on login
9. Set up monitoring
10. Backup database regularly

### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=<very-long-random-key>
DATABASE_URL=postgresql://user:pass@host/db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## 📚 Related Documentation

- `AUTHENTICATION_GUIDE.md` - Detailed authentication features
- `FEATURE_ANALYSIS.md` - System feature overview
- `IMPLEMENTATION_SUMMARY_NOV30.md` - Today's changes

---

## ✅ Verification Checklist

- [ ] Registered a new account
- [ ] Logged in with credentials
- [ ] Logged out successfully
- [ ] Tried to access protected page (redirected to login)
- [ ] Tried admin operation as borrower (permission denied)
- [ ] Admin can add equipment
- [ ] Staff can edit equipment
- [ ] Borrower cannot delete equipment
- [ ] Passwords are not visible in logs
- [ ] Audit log shows all operations

---

**Version:** 1.0  
**Last Updated:** November 30, 2025  
**Status:** ✅ Production Ready
