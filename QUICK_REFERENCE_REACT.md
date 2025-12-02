# Quick Reference Card

## Installation & Running (3 Steps)

```bash
# Step 1: Install dependencies (one-time)
cd frontend
npm install

# Step 2: Run Flask backend (Terminal 1)
python app.py

# Step 3: Run React frontend (Terminal 2)
npm run dev
```

**Then open:** <http://localhost:3000>

## Project Structure

```text
frontend/
├── src/
│   ├── components/      # Navbar, ProtectedRoute
│   ├── context/         # Auth, DarkMode
│   ├── pages/           # 8 page components
│   ├── services/        # api.js (38+ methods)
│   ├── styles/          # 5 CSS files
│   ├── App.jsx
│   └── main.jsx
├── public/index.html
├── package.json
├── vite.config.js
└── README.md
```

## Pages Available

| Path | Component | Features |
|------|-----------|----------|
| /login | Login.jsx | Email/password login |
| /register | Register.jsx | User registration |
| /dashboard | Dashboard.jsx | Home page, quick links |
| /equipment | Equipment.jsx | Equipment list, CRUD |
| /students | Students.jsx | Student list, CRUD |
| /loans | Loans.jsx | Loan management |
| /reservations | Reservations.jsx | Reservation list |
| /reports | Reports.jsx | 5 analytics tabs |

## API Services (38+ Methods)

```javascript
// Authentication
authService.login(email, password)
authService.register(email, password, full_name, student_id, phone)
authService.logout()
authService.getCurrentUser()

// Equipment (6 methods)
equipmentService.getAll()
equipmentService.getById(id)
equipmentService.create(data)
equipmentService.update(id, data)
equipmentService.delete(id)
equipmentService.getAvailable()

// Students (6 methods)
studentService.getAll()
studentService.getById(id)
studentService.create(data)
studentService.update(id, data)
studentService.delete(id)
studentService.getProfile()

// Loans (7 methods)
loanService.getAll()
loanService.checkout(data)
loanService.returnItem(loan_id, data)
loanService.renew(id)
loanService.getOverdue()
// ... more

// Reservations (5 methods)
reservationService.getAll()
reservationService.create(data)
reservationService.cancel(id)
reservationService.getByEquipment(equipment_id)
reservationService.getByStudent(student_id)

// Reports (5 methods)
reportService.getEquipmentStatus()
reportService.getLoanActivity()
reportService.getOverdueAnalysis()
reportService.getDamageAnalysis()
reportService.getStudentActivity()
```

## Using Context Hooks

```javascript
// Authentication
const { user, login, register, logout, isAuthenticated } = useAuth();

// Dark Mode
const { isDarkMode, toggleDarkMode } = useDarkMode();
```

## Creating a New Page

```jsx
// 1. Create src/pages/NewPage.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

export const NewPage = () => {
  const { user } = useAuth();
  
  return <div>Your content here</div>;
};

// 2. Import in App.jsx
import { NewPage } from './pages/NewPage';

// 3. Add route in App.jsx
<Route path="/newpage" element={
  <ProtectedRoute>
    <Navbar />
    <NewPage />
  </ProtectedRoute>
} />

// 4. Add link in Navbar.jsx
<Link to="/newpage">New Page</Link>
```

## Adding an API Call

```javascript
// 1. Add method to api.js (src/services/api.js)
export const newService = {
  getAll: () => api.get('/new-endpoint'),
  getById: (id) => api.get(`/new-endpoint/${id}`),
};

// 2. Use in component
import { newService } from '../services/api';

export const MyPage = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    newService.getAll()
      .then(response => setData(response.data))
      .catch(error => console.error(error));
  }, []);
  
  return <div>{/* render data */}</div>;
};
```

## CSS Variables (for Theming)

```css
:root {
  --primary-color: #3498db;
  --secondary-color: #2ecc71;
  --danger-color: #e74c3c;
  --warning-color: #f39c12;
  --dark-bg: #1a1a1a;
  --light-bg: #f5f5f5;
  --text-dark: #333;
  --text-light: #666;
  --border-color: #ddd;
}

/* Use in CSS */
button {
  background-color: var(--primary-color);
  color: var(--text-dark);
}

/* Dark mode */
body.dark-mode button {
  background-color: var(--dark-bg);
  color: var(--text-light);
}
```

## Common npm Commands

```bash
npm run dev          # Start dev server (port 3000)
npm run build        # Build for production
npm run preview      # Preview production build
npm install          # Install dependencies
npm install package  # Add new package
npm uninstall pkg    # Remove package
```

## Environment

| Component | Port | URL |
|-----------|------|-----|
| React Frontend | 3000 | <http://localhost:3000> |
| Flask Backend | 5000 | <http://localhost:5000> |
| API Proxy | 3000 | <http://localhost:3000/api/*> |
| Database | 5432 | PostgreSQL (local) |

## Dark Mode

- **Toggle Button:** Click 🌙/☀️ in navbar
- **Persistence:** Saved in localStorage
- **CSS Selector:** `body.dark-mode`
- **HTML Attribute:** `[data-theme="dark"]`
- **Detection:** System preference on first load

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 in use | `npm run dev -- --port 3001` |
| API 401 errors | Check login, restart backend |
| Page not updating | Clear cache, restart dev server |
| Dark mode not working | Check localStorage enabled |
| Components not rendering | Check browser console errors |
| API not responding | Verify Flask running on 5000 |

## File Extensions

- `.jsx` - React components
- `.js` - JavaScript (API services, utilities)
- `.css` - Styling
- `.html` - HTML templates
- `.json` - Configuration (package.json)

## Component Pattern

```jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useDarkMode } from '../context/DarkModeContext';
import { serviceMethod } from '../services/api';
import '../styles/component.css';

export const ComponentName = () => {
  const { user } = useAuth();
  const { isDarkMode } = useDarkMode();
  const [state, setState] = useState(null);
  
  useEffect(() => {
    // Fetch data
    serviceMethod()
      .then(res => setState(res.data))
      .catch(err => console.error(err));
  }, []);
  
  return (
    <div className={isDarkMode ? 'dark-mode' : ''}>
      {/* JSX content */}
    </div>
  );
};
```

## Git Commands

```bash
git status                    # See changes
git add .                    # Stage all changes
git commit -m "message"      # Commit changes
git push                     # Push to remote
git pull                     # Pull from remote
```

## Documentation Files

- `frontend/README.md` - Complete frontend guide
- `REACT_QUICK_START.md` - Installation & setup
- `REACT_FRONTEND_SUMMARY.md` - What was built
- `REACT_IMPLEMENTATION_CHECKLIST.md` - Features checklist
- `SYSTEM_ARCHITECTURE.md` - Full system diagram
- `SESSION_COMPLETION_SUMMARY.md` - Session summary

## Key Files

| File | Purpose |
|------|---------|
| src/App.jsx | Router and app setup |
| src/main.jsx | React entry point |
| src/components/ProtectedRoute.jsx | Auth wrapper |
| src/context/AuthContext.jsx | User state |
| src/context/DarkModeContext.jsx | Theme state |
| src/services/api.js | API methods |
| styles/global.css | Theme variables |
| vite.config.js | Dev server config |
| package.json | Dependencies |

## Testing Checklist

- [ ] Frontend loads at localhost:3000
- [ ] Can login with credentials
- [ ] Dashboard displays after login
- [ ] Dark mode toggle works
- [ ] Dark mode persists on refresh
- [ ] Navigation links work
- [ ] Equipment page loads data
- [ ] Students page loads data
- [ ] Logout redirects to login
- [ ] Protected routes redirect unauthenticated users

---

**Quick Start: `cd frontend && npm install && npm run dev`**

Then open <http://localhost:3000> ✨
