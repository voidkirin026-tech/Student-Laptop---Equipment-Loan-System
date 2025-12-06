# Installation Guide - Equipment Loan System

A complete, step-by-step guide to install and run the Equipment Loan System (Flask backend + React frontend) without issues.

## System Architecture Overview

This is a **two-tier application**:

- **Backend:** Python Flask API running on port 5000
  - User authentication & role-based access control (Admin, Staff, Borrower)
  - RESTful API endpoints for Students, Equipment, Loans, Reservations
  - PostgreSQL database
  - APScheduler for automated tasks (daily overdue email notifications at 8 AM)
  - Flask-Mail for email notifications

- **Frontend:** React Single Page Application (SPA) running on port 3000
  - Built with Vite (modern build tool)
  - React Router for navigation
  - AuthContext for user state management
  - DarkModeContext for theme switching
  - Axios for API communication
  - Protected routes with automatic login redirect
  - Pages: Dashboard, Equipment, Students, Loans, Reservations, Reports

---

## Prerequisites

Before starting, ensure you have installed:

- **Python 3.13+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 18+** ([Download](https://www.postgresql.org/download/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Git** (for version control)
- **Text Editor/IDE** (VS Code recommended)

Verify installations by running in your terminal:

```bash
python --version
psql --version
node --version
npm --version
git --version
```

---

## Step 1: Set Up PostgreSQL Database

### Create Database and User

Open **pgAdmin** or use the PostgreSQL command line:

```sql
-- Create database
CREATE DATABASE equipment_loan_db;

-- Create database user
CREATE USER equipment_user WITH PASSWORD 'secure_password_here';

-- Grant permissions
ALTER ROLE equipment_user SET client_encoding TO 'utf8';
ALTER ROLE equipment_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE equipment_user SET default_transaction_deferrable TO on;
ALTER ROLE equipment_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE equipment_loan_db TO equipment_user;
```

**Save these credentials** - you'll need them in Step 3.

### Verify Connection (Optional)

Test the connection using psql:

```bash
psql -U equipment_user -d equipment_loan_db -h localhost
```

---

## Step 2: Clone/Download the Repository

If using Git:

```bash
git clone https://github.com/Nemesis024/Student-Laptop---Equipment-Loan-System.git
cd equipment-loan-system
```

Or extract the provided ZIP file and navigate to the directory.

---

## Step 3: Configure Environment Variables

Create a `.env` file in the **project root** (same level as `app.py`) with the following content:

```env
# Database Configuration (from Step 1)
DATABASE_URL=postgresql://equipment_user:secure_password_here@localhost:5432/equipment_loan_db

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Email Configuration (Optional - for notification emails)
# Gmail: Enable "App Passwords" in your Google Account settings
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@equipmentloan.com
```

**Important:**

- Replace `secure_password_here` with the actual password from Step 1
- For Gmail, generate an [App Password](https://myaccount.google.com/apppasswords), not your regular password
- **Never commit `.env` to version control**

---

## Step 4: Set Up Python Backend

### Create Virtual Environment

Navigate to the project root and create a Python virtual environment:

**Windows (Command Prompt):**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your terminal should show `(venv)` at the beginning of the line.

### Install Python Dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Expected output: All packages install successfully without errors.

**If you get dependency errors:**

- Delete the `venv` folder
- Restart Command Prompt/Terminal
- Repeat steps 4.1-4.2

### Verify Installation

Check that all packages installed correctly:

```bash
pip list
```

Should include: `Flask`, `Flask-SQLAlchemy`, `Flask-Mail`, `Flask-Login`, `APScheduler`, `psycopg2-binary`, `Werkzeug`

---

## Step 5: Initialize the Database

The database tables are created automatically when the Flask app runs. You can optionally populate sample data:

```bash
# Still in the activated virtual environment
python load_sample_data.py
```

This loads:

- Sample students (50+ programs, multiple year levels)
- Sample equipment (Laptops, Tablets, Storage devices)
- Sample loans (historical data for testing)

---

## Step 6: Set Up React Frontend

Navigate to the `frontend` directory:

```bash
cd frontend
```

### Install Node Dependencies

```bash
npm install
```

### Verify Installation 2

Check that Node modules installed:

```bash
npm list
```

Should show: `react`, `react-dom`, `axios`, `react-router-dom`, `vite`

---

## Step 7: Run the Application

### Start the Backend Server

In the **project root** directory (with Python venv activated):

```bash
python app.py
```

Expected output:

```http
WARNING in app.runserver: This is a development server. Do not use it in a production deployment.
Running on http://127.0.0.1:5000
```

**Keep this terminal open** - it runs the backend server.

### Start the Frontend Server (New Terminal)

Open a **new terminal** and navigate to the frontend directory:

```bash
cd frontend
npm run dev
```

Expected output:

```http
VITE v7.2.6 ready in 100 ms
➜  Local:   http://localhost:3000/
```

---

## Step 8: Access the Application

Open your browser and go to:

```http
http://localhost:3000/
```

You'll be redirected to the login page.

### First-Time Login

Use these sample credentials (if you ran `load_sample_data.py`):

- **Username:** `admin`
- **Password:** `admin123`

Or register a new account:

1. Click "Don't have an account? Register here"
2. Fill in the registration form
3. Login with your new credentials

---

## Troubleshooting

### Database connection error

- Verify PostgreSQL is running
- Check `.env` credentials are correct
- Run: `psql -U equipment_user -d equipment_loan_db` to test

### Module not found (Python)

- Verify virtual environment is activated (`venv` shows in terminal)
- Run: `pip install -r requirements.txt` again
- Try: `pip install --upgrade setuptools wheel`

### Port 5000 already in use

- Another Flask app is running
- Option 1: Find and kill the process
- Option 2: Change port in `app.py`: `app.run(port=5001)`

### Port 3000 already in use

- Another Vite app is running
- Vite will auto-increment to 3001, 3002, etc.
- Or: `npm run dev -- --port 3001`

### Email not working

- Check `.env` MAIL_* settings
- For Gmail, generate an [App Password](https://myaccount.google.com/apppasswords)
- Verify SMTP server is accessible from your network

---

## Frontend-Specific Troubleshooting

### Blank page with "Loading..." spinner

**Problem:** Dashboard shows "Loading..." forever
**Solution:**

1. Open browser DevTools (F12) → Console tab
2. Look for red error messages (API fetch errors)
3. Check that backend is running: `curl http://localhost:5000/api/students`
4. Verify `/api` proxy in `frontend/vite.config.js` points to `http://localhost:5000`

### API 401 Unauthorized errors in console

**Problem:** Login appears to work but API calls fail with 401
**Solution:**

1. Verify Flask backend is running on port 5000
2. Check browser cookies are enabled (DevTools → Application → Cookies)
3. Clear cookies and browser cache, try login again
4. Verify `withCredentials: true` in `frontend/src/services/api.js`

### Login redirects to login page immediately

**Problem:** Can't stay logged in after successful login
**Solution:**

1. Check backend is returning user data: Open Network tab (F12), click login, inspect response
2. Verify backend session is working: Backend terminal should show no errors
3. Clear all cookies for localhost
4. Check `AuthContext.jsx` for login state management
5. Try incognito window to start fresh

### Dark mode not persisting

**Problem:** Dark mode toggle doesn't save preference
**Solution:**

1. Check localStorage is enabled in browser settings
2. Verify DevTools → Application → Storage → Local Storage shows entries
3. Clear localStorage: `localStorage.clear()` in console
4. Refresh page and toggle dark mode again
5. Check `DarkModeContext.jsx` implementation

### Page shows "Not authenticated" or redirects to login

**Problem:** Can't access protected pages even after login
**Solution:**

1. Open DevTools Console and check for errors
2. Verify AuthContext initialized: `console.log(user)` in any component
3. Check ProtectedRoute.jsx logic for role-based access
4. Backend may have session timeout - try logging out and back in
5. Verify JWT/session is not expired in Network tab

### API shows correct data but UI doesn't update

**Problem:** Component shows loading state or doesn't render data
**Solution:**

1. Check that `useEffect` hooks are properly set up to call API
2. Verify API response matches expected data structure
3. Look for `null` pointer exceptions in Console
4. Check if state is being set but component not re-rendering
5. Add `console.log()` statements in component to debug

### Buttons don't work or forms submit twice

**Problem:** Submit button appears unresponsive or triggers twice
**Solution:**

1. Check that `disabled={loading}` is on submit button
2. Verify `preventDefault()` is in form submit handler
3. Look for duplicate event listeners in Console
4. Clear browser cache completely
5. Restart dev server: Ctrl+C in terminal, then `npm run dev` again

### Styles not applying or look broken

**Problem:** CSS doesn't load or components look unstyled
**Solution:**

1. Clear browser cache (Ctrl+Shift+Delete)
2. Restart dev server completely
3. Verify CSS imports in component files match actual filenames
4. Check `frontend/src/styles/` folder exists with all CSS files
5. Verify `global.css` is imported in `frontend/src/App.jsx`
6. Check for CSS file path issues in `styles/` directory

### Component shows "useAuth must be used within an AuthProvider"

**Problem:** Error about useAuth outside provider context
**Solution:**

1. Verify all pages wrapped by `<AuthProvider>` in `App.jsx`
2. Check `ProtectedRoute.jsx` properly wraps components
3. Ensure hooks are called inside component function, not conditionally
4. Check for incorrect hook usage patterns

### CORS errors in Network tab

**Problem:** Network requests blocked with CORS error
**Solution:**

1. Verify backend CORS is enabled (check `app.py`)
2. Check `vite.config.js` proxy target: should be `http://localhost:5000`
3. Backend should allow requests from `http://localhost:3000`
4. Clear browser cache and restart both servers

### Getting "Cannot find module" errors

**Problem:** Import errors like "Cannot find module './api'"
**Solution:**

1. Check file exists at path: verify spelling matches exactly
2. Verify file extensions (.jsx, .js, .css) are correct in imports
3. Run `npm install` again to reinstall dependencies
4. Check `frontend/` directory structure matches expected layout
5. Restart dev server: `npm run dev`

### React component not rendering

**Problem:** Component code exists but nothing appears on page
**Solution:**

1. Check component is exported/imported correctly
2. Verify route is defined in `App.jsx`
3. Check browser Console for JavaScript errors
4. Use React DevTools extension to inspect component tree
5. Add `console.log()` at top of component to verify it's called

### Performance issues or app freezes

**Problem:** App becomes slow or unresponsive
**Solution:**

1. Check network requests in DevTools Network tab
2. Look for excessive API calls or long response times
3. Verify backend is responding quickly
4. Check browser memory usage (DevTools → Performance)
5. Clear browser cache and localStorage
6. Try in incognito window to rule out browser extensions

### After updating code, changes don't appear

**Problem:** Made changes to source code but app still shows old version
**Solution:**

1. Stop dev server (Ctrl+C)
2. Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
3. Clear browser cache completely
4. Restart dev server: `npm run dev`
5. Check file was actually saved (look at file timestamp)

---

## Backend-Specific Troubleshooting

### Flask shows "ImportError: cannot import name..."

**Problem:** Python import errors when running `python app.py`
**Solution:**

1. Verify virtual environment is activated
2. Run `pip install -r requirements.txt` again
3. Check imports in Python files match module names
4. Verify all required packages installed: `pip list`

### Shows "blank page with "Frontend shows blank page

**Problem:** Dashboard shows "Loading..." forever
**Solution:**

1. Open browser DevTools (F12) → Console tab
2. Look for red error messages (API fetch errors)
3. Check that backend is running: `curl http://localhost:5000/api/students`
4. Verify `/api` proxy in `frontend/vite.config.js` points to `http://localhost:5000`

### Database tables not created

**Problem:** Getting "table does not exist" errors
**Solution:**

1. Verify `.env` DATABASE_URL is correct
2. Verify PostgreSQL server is running
3. Flask should auto-create tables on first run
4. If not: `python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all()"`
5. Check `models.py` for all model definitions

### Scheduler not running (overdue emails not sending)

**Problem:** Daily overdue check at 8 AM not happening
**Solution:**

1. Check Flask terminal output for "Scheduler started" message
2. Verify APScheduler is installed: `pip list | grep APScheduler`
3. Check system time is set correctly
4. Look for errors in `scheduler.py`
5. Manually trigger: Create loan with past due date and check if email is sent
6. View scheduler logs in Flask terminal

---

## Post-Installation Checklist

- [ ] PostgreSQL running locally
- [ ] `.env` file created with correct credentials
- [ ] Virtual environment activated
- [ ] Python dependencies installed (`pip list`)
- [ ] Node dependencies installed (`npm list`)
- [ ] Backend running on <http://localhost:5000>
- [ ] Frontend running on <http://localhost:3000>
- [ ] Can access login page
- [ ] Can login or register successfully
- [ ] Dashboard loads without errors

---

## Daily Startup Commands

After initial setup, to start the application each day:

**Terminal 1 (Backend):**

```bash
cd /path/to/equipment-loan-system
venv\Scripts\activate
python app.py
```

**Terminal 2 (Frontend):**

```bash
cd /path/to/equipment-loan-system/frontend
npm run dev
```

Then open: `http://localhost:3000/`

---

## Directory Structure

```text
equipment-loan-system/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration management
├── models.py                   # Database models (User, Student, Equipment, Loan, etc.)
├── routes.py                   # API endpoints for Students, Equipment, Loans, Reservations
├── auth_routes.py              # Authentication endpoints (login, register, logout)
├── email_service.py            # Email functionality (checkout, return, overdue notifications)
├── scheduler.py                # Background task scheduler (8 AM daily overdue check)
├── decorators.py               # Custom decorators (staff_required, admin_required, etc.)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── frontend/                   # React frontend (Vite)
│   ├── src/
│   │   ├── App.jsx             # Root component with routing
│   │   ├── main.jsx            # React entry point
│   │   ├── components/         # Reusable components (Navbar, ProtectedRoute)
│   │   ├── context/            # State management (AuthContext, DarkModeContext)
│   │   ├── pages/              # Page components (Login, Dashboard, Equipment, etc.)
│   │   ├── services/           # API service layer (api.js with Axios)
│   │   └── styles/             # CSS stylesheets (global, auth, navbar, dashboard, pages)
│   ├── public/                 # Static assets
│   ├── package.json            # Node.js dependencies
│   ├── vite.config.js          # Vite configuration (proxies to backend on 5000)
│   └── README.md               # Frontend documentation
├── templates/                  # Legacy HTML templates (optional, not used by React)
└── README.md                   # Main project documentation
```

---

## User Roles and Permissions

The system has three user roles:

- **Admin:** Full system access, can manage users and settings
- **Staff:** Can manage equipment, students, and loans
- **Borrower:** Can view available equipment and make reservations

Default admin account (if sample data loaded):

- **Username:** `admin`
- **Password:** `admin123`

---

## Key Features

- **Authentication:** Secure login/registration with password hashing
- **Role-Based Access Control:** Different permissions for Admin, Staff, and Borrower
- **Equipment Management:** Add, edit, delete, and track equipment
- **Loan Management:** Checkout and return tracking
- **Automated Notifications:** Email alerts for overdue items (daily at 8 AM)
- **Dark Mode:** Toggle theme in the navbar
- **Dashboard Analytics:** Real-time statistics and reports
- **Protected Routes:** Automatic redirect to login for unauthorized access

---

## Next Steps After Installation

1. **Change Default Password:** Update the `SECRET_KEY` in `.env` for production
2. **Configure Email:** Set up SMTP credentials for notifications
3. **Load Real Data:** Replace sample data with actual student/equipment records
4. **Review Roles:** Understand Admin, Staff, and Borrower permissions in `models.py`
5. **Test Features:** Try checkout, returns, and email notifications
6. **Review API:** Check `routes.py` and `auth_routes.py` for available endpoints

---

**Last Updated:** December 6, 2025
**Version:** 1.0
