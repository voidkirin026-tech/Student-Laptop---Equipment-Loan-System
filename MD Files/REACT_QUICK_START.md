# React Frontend - Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Install Node.js

If you don't have Node.js installed:

1. Go to <https://nodejs.org/>
2. Download the LTS version (18.x or 20.x)
3. Run the installer and follow prompts
4. Verify installation:

```bash
node --version
npm --version
```

### Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
```

This installs:

- React 18.2.0
- React Router 6.20.0
- Axios 1.6.0
- Vite 5.0.0

### Step 3: Start Development Server

```bash
npm run dev
```

You should see:

```text
➜  Local:   http://localhost:3000/
```

## Running the Full System

### Terminal 1: Flask Backend

```bash
# From project root
python app.py
# Server runs on http://localhost:5000
```

### Terminal 2: React Frontend

```bash
# From frontend folder
npm run dev
# App opens at http://localhost:3000
```

## First Login

### Test Credentials

After the backend creates the database, use:

- **Email:** <test@example.com>
- **Password:** password123

Or register a new account using the Sign Up link.

## What You Can Do

1. **Login/Register** - Create accounts and authenticate
2. **Dashboard** - View home page with quick links
3. **Equipment** - Browse all equipment inventory
4. **Students** - View student list
5. **Loans** - Manage equipment loans
6. **Reservations** - View reservations
7. **Reports** - View analytics (5 different reports)
8. **Dark Mode** - Toggle 🌙/☀️ in navbar

## API Communication

The frontend automatically:

- Sends requests to `http://localhost:3000/api/*`
- Vite proxies these to `http://localhost:5000/api/*`
- Manages Flask session cookies
- Handles authentication and redirects

## Troubleshooting

### Port 3000 already in use

```bash
npm run dev -- --port 3001
```

### Flask backend not connecting

- Make sure Flask is running on port 5000
- Check console for error messages
- Verify firewall isn't blocking port 5000

### Page shows "Loading..." forever

- Check browser console (F12) for errors
- Verify Flask backend is running
- Clear browser cache and refresh

### Dark mode not working

- Check localStorage is enabled in browser
- Try clearing browser cache
- Check browser console for errors

## Project Structure

```text
frontend/
├── src/
│   ├── components/     # Navbar, ProtectedRoute
│   ├── context/        # Auth & dark mode
│   ├── pages/          # 8 page components
│   ├── services/       # API communication
│   ├── styles/         # CSS styling
│   ├── App.jsx        # Router setup
│   └── main.jsx       # React entry point
├── public/
│   └── index.html     # HTML template
├── package.json       # Dependencies
└── vite.config.js     # Vite configuration
```

## Common Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install new package
npm install package-name
```

## Making Changes

### Add a New Page

1. Create file in `src/pages/PageName.jsx`
2. Import in `src/App.jsx`
3. Add route in App.jsx
4. Add link in `src/components/Navbar.jsx`

### Modify Styles

- Edit CSS files in `src/styles/`
- Changes auto-reload with Vite

### Change Dark Mode Colors

Edit CSS variables in `src/styles/global.css`:

```css
:root {
  --primary-color: #3498db;
  --secondary-color: #2ecc71;
  /* ... more colors ... */
}
```

## Next Steps

1. ✅ Install Node.js
2. ✅ Run `npm install` in frontend folder
3. ✅ Run `npm run dev` to start dev server
4. ✅ Test login and navigation
5. ⬜ Add more features as needed
6. ⬜ Build for production when ready

## Documentation

- **frontend/README.md** - Comprehensive documentation
- **REACT_FRONTEND_SUMMARY.md** - Implementation details
- Parent README.md - Backend documentation

## Support

Check the browser console (F12) for error messages. Most issues are:

- Flask backend not running
- Node.js not installed
- Port conflicts
- Stale cache

Clear cache and refresh if pages don't update.

---

**You're all set! Start the Flask backend and React frontend, then navigate to <http://localhost:3000>** 🚀
