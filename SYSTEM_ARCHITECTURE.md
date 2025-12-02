# Complete System Architecture

## Overview

The Student Laptop & Equipment Loan System now consists of a modern full-stack application with a Flask backend and a React frontend.

```text
┌─────────────────────────────────────────────────────────┐
│                   CLIENT BROWSER (Port 3000)             │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │         React Single-Page Application             │   │
│  │  - Login/Register Pages                           │   │
│  │  - Dashboard (home)                               │   │
│  │  - Equipment Management                           │   │
│  │  - Student Management                             │   │
│  │  - Loan Management                                │   │
│  │  - Reservation Management                         │   │
│  │  - Reports & Analytics                            │   │
│  │  - Dark Mode Toggle                               │   │
│  └──────────────────────────────────────────────────┘   │
│                         ↓                                │
│         (HTTP Requests to /api/*)                       │
└─────────────────────────────────────────────────────────┘
         ↓
    Vite Dev Server Proxy
         ↓
┌─────────────────────────────────────────────────────────┐
│              FLASK BACKEND (Port 5000)                   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │            Flask Application (app.py)             │   │
│  │  - Flask-Login authentication                     │   │
│  │  - Session management                             │   │
│  │  - CSRF protection                                │   │
│  └──────────────────────────────────────────────────┘   │
│                         ↓                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │        REST API Endpoints (41+ total)             │   │
│  │  - /api/auth/* (5 endpoints)                      │   │
│  │  - /api/equipment/* (6 endpoints)                 │   │
│  │  - /api/students/* (6 endpoints)                  │   │
│  │  - /api/loans/* (8 endpoints)                     │   │
│  │  - /api/reservations/* (5 endpoints)              │   │
│  │  - /api/damage-logs/* (5 endpoints)               │   │
│  │  - /api/reports/* (5 endpoints)                   │   │
│  └──────────────────────────────────────────────────┘   │
│                         ↓                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │       SQLAlchemy ORM (models.py)                  │   │
│  │  - User (authentication)                          │   │
│  │  - Student                                         │   │
│  │  - Equipment                                       │   │
│  │  - Loan                                            │   │
│  │  - Reservation                                     │   │
│  │  - DamageLog                                       │   │
│  │  - ReturnDetail                                    │   │
│  └──────────────────────────────────────────────────┘   │
│                         ↓                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │       PostgreSQL Database                         │   │
│  │  - users                                           │   │
│  │  - students                                        │   │
│  │  - equipment                                       │   │
│  │  - loans                                           │   │
│  │  - reservations                                    │   │
│  │  - damage_logs                                     │   │
│  │  - return_details                                  │   │
│  │  - and more...                                     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Frontend Architecture (React)

```text
src/
├── App.jsx
│   └── BrowserRouter
│       ├── DarkModeProvider (Context)
│       └── AuthProvider (Context)
│           └── Routes
│               ├── Public Routes
│               │   ├── /login → Login.jsx
│               │   └── /register → Register.jsx
│               └── Protected Routes
│                   ├── /dashboard → Navbar + Dashboard.jsx
│                   ├── /equipment → Navbar + Equipment.jsx
│                   ├── /students → Navbar + Students.jsx
│                   ├── /loans → Navbar + Loans.jsx
│                   ├── /reservations → Navbar + Reservations.jsx
│                   └── /reports → Navbar + Reports.jsx
│
├── components/
│   ├── Navbar.jsx (global navigation + dark mode toggle)
│   └── ProtectedRoute.jsx (route protection wrapper)
│
├── context/
│   ├── AuthContext.jsx (user authentication state)
│   └── DarkModeContext.jsx (dark/light mode state)
│
├── pages/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│   ├── Equipment.jsx
│   ├── Students.jsx
│   ├── Loans.jsx
│   ├── Reservations.jsx
│   └── Reports.jsx
│
├── services/
│   └── api.js
│       ├── Axios instance
│       ├── authService (4 methods)
│       ├── equipmentService (6 methods)
│       ├── studentService (6 methods)
│       ├── loanService (7 methods)
│       ├── reservationService (5 methods)
│       ├── damageService (5 methods)
│       └── reportService (5 methods)
│
└── styles/
    ├── global.css (variables, resets, utilities)
    ├── auth.css (login/register pages)
    ├── navbar.css (navigation)
    ├── dashboard.css (home page)
    └── pages.css (data pages, tables, tabs)
```

## Backend Architecture (Flask)

```text
app.py (main application)
├── Flask app initialization
├── Database setup
├── Route registration
└── Error handlers

routes.py (41+ endpoints)
├── auth_routes.py
│   └── 5 endpoints (login, register, logout, etc.)
├── Equipment endpoints (6)
├── Student endpoints (6)
├── Loan endpoints (8)
├── Reservation endpoints (5)
├── Damage log endpoints (5)
└── Report endpoints (5)

models.py (SQLAlchemy models)
├── User (Flask-Login)
├── Student
├── Equipment
├── Loan
├── Reservation
├── DamageLog
└── ReturnDetail

config.py (configuration)
├── Database URL
├── Secret keys
├── Flask settings

decorators.py (custom decorators)
├── @staff_required
├── @admin_required
└── @borrower_required

email_service.py (email notifications)
scheduler.py (background tasks)
```

## Data Flow

### User Authentication Flow

```text
1. User enters credentials in React Login page
2. React sends POST to /api/auth/login via axios
3. Flask validates credentials against database
4. Flask-Login creates session
5. Flask returns user data + sets session cookie
6. React stores in AuthContext
7. React redirects to /dashboard
```

### Data Retrieval Flow (Example: Equipment List)

```text
1. User navigates to /equipment page
2. Equipment.jsx useEffect calls equipmentService.getAll()
3. axios GET /api/equipment is sent
4. Vite proxy routes to Flask http://localhost:5000/api/equipment
5. Flask queries PostgreSQL database
6. Flask returns JSON array of equipment
7. React displays in table
```

### Dark Mode Flow

```text
1. User clicks 🌙 button in Navbar
2. Navbar calls toggleDarkMode() from DarkModeContext
3. Context updates isDarkMode state
4. Context updates document classes and attributes
5. CSS uses [data-theme="dark"] selector
6. All components automatically render dark styles
7. Preference saved to localStorage
```

## Technology Stack

### Frontend

- **React 18.2.0** - UI library with hooks
- **React Router 6.20.0** - Client-side routing
- **Axios 1.6.0** - HTTP client
- **Vite 5.0.0** - Build tool and dev server
- **Plain CSS** - Styling

### Backend

- **Flask 3.0.0** - Web framework
- **SQLAlchemy** - ORM
- **Flask-Login** - Authentication
- **Flask-Mail** - Email
- **APScheduler** - Scheduled tasks
- **PostgreSQL** - Database

## API Endpoint Categories

### Authentication (5)

- POST /api/auth/login
- POST /api/auth/register
- POST /api/auth/logout
- GET /api/auth/current-user
- Additional endpoints

### Equipment (6)

- GET /api/equipment (list all)
- GET /api/equipment/:id (get one)
- POST /api/equipment (create)
- PUT /api/equipment/:id (update)
- DELETE /api/equipment/:id (delete)
- GET /api/equipment/available (get available)

### Students (6)

- GET /api/students
- GET /api/students/:id
- POST /api/students
- PUT /api/students/:id
- DELETE /api/students/:id
- GET /api/students/profile

### Loans (8)

- GET /api/loans
- GET /api/loans/:id
- POST /api/loans (create)
- PUT /api/loans/:id (update)
- POST /api/loans/checkout
- POST /api/loans/:id/return
- POST /api/loans/:id/renew
- GET /api/loans/overdue

### Reservations (5)

- GET /api/reservations
- GET /api/reservations/:id
- POST /api/reservations
- DELETE /api/reservations/:id
- GET /api/reservations/equipment/:id
- GET /api/reservations/student/:id

### Damage Logs (5)

- GET /api/damage-logs
- GET /api/damage-logs/:id
- POST /api/damage-logs
- GET /api/damage-logs/loan/:id
- GET /api/damage-logs/student/:id

### Reports (5)

- GET /api/reports/equipment-status
- GET /api/reports/loan-activity
- GET /api/reports/overdue-analysis
- GET /api/reports/damage-analysis
- GET /api/reports/student-activity

## Database Schema

```text
users
├── id (PK)
├── email (unique)
├── password_hash
├── full_name
├── role (student, staff, admin)
└── created_at

students
├── id (PK)
├── user_id (FK to users)
├── student_id (unique)
├── phone
├── academic_year
└── created_at

equipment
├── id (PK)
├── name
├── category
├── status (available, checked_out, maintenance, damaged)
├── serial_number
├── cost_value
└── created_at

loans
├── id (PK)
├── student_id (FK)
├── equipment_id (FK)
├── checkout_date
├── expected_return_date
├── actual_return_date
├── status (active, returned, overdue, lost)
└── created_at

reservations
├── id (PK)
├── student_id (FK)
├── equipment_id (FK)
├── reservation_date
├── status (pending, confirmed, cancelled)
└── created_at

damage_logs
├── id (PK)
├── loan_id (FK)
├── student_id (FK)
├── damage_type
├── description
├── estimated_cost
└── created_at

return_details
├── id (PK)
├── loan_id (FK)
├── condition
├── notes
└── created_at
```

## Security Features

### Frontend 2

- Protected routes with ProtectedRoute wrapper
- Session-based authentication via Flask-Login
- CSRF token support
- Secure cookie handling
- Clear error messages without exposing details

### Backend 2

- Flask-Login session management
- Password hashing with Werkzeug
- CSRF protection
- Role-based access control (@staff_required, etc.)
- Input validation
- SQL injection prevention via SQLAlchemy

## Development Workflow

### Start Development

```bash
# Terminal 1: Flask Backend
python app.py          # Runs on http://localhost:5000

# Terminal 2: React Frontend
cd frontend
npm install            # One-time setup
npm run dev           # Runs on http://localhost:3000
```

### Make Changes

- Edit React components → auto-reload via Vite HMR
- Edit Flask code → manual restart required
- Edit CSS → auto-reload
- Edit Flask routes → manual restart

### Debug

- Browser DevTools (F12) for React debugging
- Network tab to inspect API calls
- Flask terminal for server logs
- React console for component state

## Deployment

### Development

- Frontend: Vite dev server on port 3000
- Backend: Flask dev server on port 5000

### Production

```bash
# Build React
npm run build          # Creates dist/ folder

# Deploy options:
# 1. Serve React static files from Flask
# 2. Deploy to Vercel, Netlify, etc.
# 3. Use Docker containers
# 4. Deploy Flask to cloud (AWS, Azure, Heroku)
```

## Performance Considerations

### Frontend 3

- Vite provides fast builds and HMR
- React DevTools Profiler for optimization
- CSS is plain (no runtime overhead)
- Axios requests are cached by browser

### Backend 3

- SQLAlchemy lazy loading for efficiency
- Database indexes on frequently queried columns
- API responses limited to necessary fields
- Pagination ready for large datasets

## Monitoring & Logging

### Frontend 4

- Browser console for errors
- Network tab for API calls
- React DevTools extension
- LocalStorage for dark mode preference

### Backend 4

- Flask logs in terminal
- Email logs for notifications
- Database query logs available
- Error stack traces in Flask

## Future Enhancements

### Frontend 5

- [ ] Form validation with error messages
- [ ] Search and filter functionality
- [ ] Pagination for large datasets
- [ ] Dashboard statistics/charts
- [ ] Modal dialogs for confirmations
- [ ] Toast notifications
- [ ] Advanced data grid features
- [ ] File uploads for images
- [ ] Unit and E2E tests

### Backend 5

- [ ] GraphQL API option
- [ ] Webhook notifications
- [ ] Advanced reporting with exports
- [ ] API rate limiting
- [ ] Comprehensive logging
- [ ] Database backup automation
- [ ] Performance monitoring
- [ ] Cache layer (Redis)

## Support & Troubleshooting

### Common Issues

1. **Port conflicts** - Change port in vite.config.js
2. **CORS errors** - Check proxy configuration
3. **API 401 errors** - Verify login and session
4. **Dark mode not working** - Clear localStorage
5. **Page not updating** - Clear browser cache

### Resources

- Backend: `../README.md`
- Frontend: `frontend/README.md`
- Quick Start: `REACT_QUICK_START.md`
- Implementation: `REACT_FRONTEND_SUMMARY.md`
- Checklist: `REACT_IMPLEMENTATION_CHECKLIST.md`

---

**Complete system is ready for development, testing, and deployment!**
