# Quick Troubleshooting Reference - One-Page Cheat Sheet

## 🆘 Problem? Check Here First

### Frontend Blank Page / Loading Forever

```text
1. Press F12 → Console tab
2. Look for RED errors
3. Is backend running? curl http://localhost:5000/api/students
4. Restart: Stop npm, clear cache, npm run dev
```

### Login Not Working / 401 Errors

```text
1. Backend running on 5000?
2. Check network tab - see login response?
3. Clear cookies: Ctrl+Shift+Delete
4. Try incognito window
5. Check vite.config.js proxy: target: 'http://localhost:5000'
```

### Port Already in Use

```text
Backend (5000): Change port in app.py: app.run(port=5001)
Frontend (3000): npm run dev -- --port 3001
```

### API Errors in Console

```text
401 = Not authenticated → Login
404 = Not found → Check API endpoint
500 = Server error → Check backend terminal
CORS error → Check proxy in vite.config.js
```

### Dark Mode Not Working

```text
1. DevTools → Application → Storage → Local Storage
2. localStorage.clear()
3. Refresh page, toggle dark mode
4. Check DarkModeContext.jsx
```

### Styles Not Loading

```text
1. Ctrl+Shift+Delete (hard clear browser cache)
2. Stop dev server (Ctrl+C)
3. Restart: npm run dev
4. Check CSS imports in components
```

### Button Doesn't Work / Form Submits Twice

```text
1. Check button: disabled={loading}
2. Check form: preventDefault() in handler
3. Clear cache completely
4. Restart dev server
```

### Component Shows "Loading..." Forever

```text
1. Check useEffect dependencies
2. Verify API endpoint exists
3. Look for infinite loops
4. Check error handling in try-catch
```

### Backend Errors

**ImportError:**

```text
1. Activate venv: venv\Scripts\activate
2. pip install -r requirements.txt
3. pip list (verify all packages there)
```

**Database Error:**

```text
1. PostgreSQL running?
2. Check .env DATABASE_URL
3. User/password correct?
4. Test: psql -U equipment_user -d equipment_loan_db
```

**No tables in database:**

```bash
python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all()"
```

---

## 🚀 Startup Commands

```bash
# Terminal 1 - Backend
cd /path/to/equipment-loan-system
venv\Scripts\activate
python app.py
# Should show: Running on http://127.0.0.1:5000

# Terminal 2 - Frontend
cd frontend
npm run dev
# Should show: Local: http://localhost:3000
```

---

## 🔧 Debug Checklist

**When something breaks:**

- [ ] Is backend running? (check terminal)
- [ ] Is frontend running? (check terminal)
- [ ] Open DevTools F12 → Console (look for red errors)
- [ ] Check Network tab (see API responses?)
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Check backend terminal for Python errors
- [ ] Restart both servers
- [ ] Try incognito/private window
- [ ] Check `.env` file exists with correct values
- [ ] Verify PostgreSQL running

---

## 📍 Key Ports

- **Backend API:** <http://localhost:5000> (Flask)
- **Frontend UI:** <http://localhost:3000> (Vite)
- **PostgreSQL:** localhost:5432
- **Login:** <http://localhost:3000/login>

---

## 📁 Important Files

**If frontend broken:**

- `frontend/vite.config.js` - Check proxy to 5000
- `frontend/src/services/api.js` - API configuration
- `frontend/src/App.jsx` - Routes and Provider setup

**If backend broken:**

- `app.py` - Main app
- `models.py` - Database models
- `routes.py` - API endpoints
- `.env` - Configuration

**If database broken:**

- `.env` - DATABASE_URL setting
- `models.py` - Table definitions

---

## 🔐 Default Login (if sample data loaded)

```text
Username: admin
Password: admin123
```

---

## 📊 Health Check

```bash
# Backend health
curl http://localhost:5000/api/students

# Should return JSON array of students
# If connection refused → backend not running
# If 401 → not authenticated
# If 500 → check backend terminal
```

---

## 🆘 When All Else Fails

1. **Nuclear option - Full reset:**

   ```bash
   # Backend
   deactivate
   rm -rf venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   
   # Frontend (new terminal)
   rm -rf node_modules
   npm install
   npm run dev
   ```

2. **Browser reset:**
   - Ctrl+Shift+Delete (clear all data)
   - Close all tabs
   - Close browser completely
   - Open fresh browser
   - Go to <http://localhost:3000>

3. **Check logs:**
   - Backend: Look at terminal output for errors
   - Frontend: F12 → Console for errors
   - Database: Check PostgreSQL server status

---

## 📞 Support Resources

1. **INSTALLATION.md** - Full setup guide
2. **BUG_SCAN_REPORT.md** - Known issues and fixes
3. **FRONTEND_TROUBLESHOOTING_SUMMARY.md** - Detailed frontend issues
4. **frontend/README.md** - Frontend documentation
5. **README.md** - Project overview

---

**Last Updated:** December 6, 2025
**Version:** 1.0
