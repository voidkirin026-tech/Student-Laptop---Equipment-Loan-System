# React Frontend - Student Laptop & Equipment Loan System

This is a modern React frontend for the Student Laptop & Equipment Loan System, replacing the Flask Jinja2 templates with a single-page application (SPA).

## Project Structure

```text
frontend/
├── public/
│   └── index.html              # HTML entry point with React root
├── src/
│   ├── components/             # Reusable React components
│   │   ├── Navbar.jsx         # Navigation bar with dark mode toggle
│   │   └── ProtectedRoute.jsx  # Route wrapper for authentication
│   ├── context/                # React Context for state management
│   │   ├── AuthContext.jsx     # Authentication state and methods
│   │   └── DarkModeContext.jsx # Dark mode state management
│   ├── pages/                  # Full page components
│   │   ├── Login.jsx           # Login page
│   │   ├── Register.jsx        # Registration page
│   │   ├── Dashboard.jsx       # Home/dashboard page
│   │   ├── Equipment.jsx       # Equipment list and management
│   │   ├── Students.jsx        # Student management
│   │   ├── Loans.jsx           # Loan management
│   │   ├── Reservations.jsx    # Reservation management
│   │   └── Reports.jsx         # Reports and analytics
│   ├── services/               # API communication layer
│   │   └── api.js              # Axios instance and API methods
│   ├── styles/                 # CSS stylesheets
│   │   ├── global.css          # Global styles and variables
│   │   ├── auth.css            # Authentication page styles
│   │   ├── navbar.css          # Navigation bar styles
│   │   ├── dashboard.css       # Dashboard styles
│   │   └── pages.css           # Page and component styles
│   ├── App.jsx                 # Root component with routing
│   └── main.jsx                # React entry point
├── package.json                # Dependencies and scripts
├── vite.config.js             # Vite bundler configuration
└── README.md                   # This file
```

## Getting Started

### Prerequisites

- **Node.js** 16+ (download from <https://nodejs.org/>)
- **npm** 8+ (comes with Node.js)
- **Flask backend** running on <http://localhost:5000>

### Installation

1. Navigate to the frontend directory:

```bash
cd frontend
```

1. Install dependencies:

```bash
npm install
```

1. Start the development server:

```bash
npm run dev
```

The app will open at <http://localhost:3000> and automatically proxy API requests to <http://localhost:5000>.

## Available Scripts

- `npm run dev` - Start development server (port 3000)
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint (if configured)

## Key Features

### Authentication

- Login and registration with email/password
- Session-based authentication (Flask-Login)
- Protected routes with automatic redirect to login
- User context available throughout app

### Dark Mode

- Toggle dark/light mode via navbar button
- Persistent preference stored in localStorage
- Automatic system preference detection
- Smooth transitions between themes

### API Integration

- Centralized API service layer using Axios
- Request/response interceptors for error handling
- Automatic session handling with credentials
- CSRF token support

### State Management

- React Context API for authentication
- React Context API for dark mode
- Hooks (useState, useEffect, useContext) for component state

### Routing

- React Router v6 for client-side routing
- Protected routes with role checking
- Automatic redirects for unauthorized access

## Architecture

### Context Providers

**AuthContext** (`src/context/AuthContext.jsx`)

- Manages user authentication state
- Provides login, register, logout methods
- Checks auth status on app initialization
- Hook: `useAuth()`

**DarkModeContext** (`src/context/DarkModeContext.jsx`)

- Manages dark mode preference
- Persists to localStorage
- Hook: `useDarkMode()`

### API Service Layer

The `api.js` service exports multiple service objects:

- `authService` - login, register, logout, getCurrentUser
- `equipmentService` - CRUD for equipment
- `studentService` - Student management
- `loanService` - Loan operations
- `reservationService` - Reservations
- `damageService` - Damage logs
- `reportService` - Analytics reports

All services use the configured Axios instance with:

- Base URL: `/api` (proxied to Flask backend)
- Credentials: included in requests
- Error handling: 401 redirects to login

### Protected Routes

Use `<ProtectedRoute>` component to protect pages:

```jsx
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Navbar />
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

Optional role checking:

```jsx
<ProtectedRoute requiredRole="admin">
  <AdminPage />
</ProtectedRoute>
```

## Styling

### CSS Architecture

- **global.css** - CSS variables, resets, base styles
- **auth.css** - Login/register page styling
- **navbar.css** - Navigation and top bar
- **dashboard.css** - Home page layout
- **pages.css** - Data tables, forms, reports

### Dark Mode 2

- CSS variables defined in `:root`
- Dark mode class applied to `document.body`
- All components use CSS variables for theme consistency
- Smooth transitions between light and dark modes

### Responsive Design

- Mobile-first approach
- Media queries for tablet/desktop layouts
- Flexbox and grid for layouts
- Touch-friendly button sizes

## API Endpoints Used

The frontend communicates with these Flask API endpoints:

### Authentication 2

- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register
- `POST /api/auth/logout` - Logout
- `GET /api/auth/current-user` - Get logged-in user

### Equipment

- `GET /api/equipment` - List all
- `GET /api/equipment/:id` - Get one
- `POST /api/equipment` - Create
- `PUT /api/equipment/:id` - Update
- `DELETE /api/equipment/:id` - Delete

### Students

- `GET /api/students` - List all
- `GET /api/students/:id` - Get one
- `POST /api/students` - Create
- `PUT /api/students/:id` - Update
- `DELETE /api/students/:id` - Delete

### Loans

- `GET /api/loans` - List all
- `POST /api/loans/checkout` - Checkout equipment
- `POST /api/loans/:id/return` - Return equipment
- `POST /api/loans/:id/renew` - Renew loan

### Reservations

- `GET /api/reservations` - List all
- `POST /api/reservations` - Create
- `DELETE /api/reservations/:id` - Cancel

### Reports

- `GET /api/reports/equipment-status` - Equipment report
- `GET /api/reports/loan-activity` - Loans report
- `GET /api/reports/overdue-analysis` - Overdue items
- `GET /api/reports/damage-analysis` - Damage records

## Development Workflow

### Adding a New Page

1. Create component in `src/pages/ComponentName.jsx`
2. Import in `src/App.jsx`
3. Add route in App.jsx
4. Add navigation link in `src/components/Navbar.jsx`

### Adding a New API Service

1. Add methods to appropriate service in `src/services/api.js`
2. Use in components via imports and hooks

### Styling a Component

1. Create or update CSS file in `src/styles/`
2. Import CSS at top of component
3. Use class names for styling
4. Support dark mode with `body.dark-mode` selectors

## Troubleshooting

### Port 3000 already in use

```bash
# Kill process on port 3000 (macOS/Linux)
lsof -ti:3000 | xargs kill -9

# Or use a different port (Windows PowerShell)
npm run dev -- --host localhost --port 3001
```

### API requests returning 401

- Check if Flask backend is running on port 5000
- Check login credentials
- Verify Flask session is working with cookies

### Dark mode not persisting

- Check browser localStorage is enabled
- Clear browser cache and try again
- Check browser console for errors

### CSS not updating

- Restart dev server
- Clear browser cache
- Check CSS imports in component files

## Deployment

Build for production:

```bash
npm run build
```

This creates an optimized bundle in `dist/` folder.

## Future Enhancements

- [ ] Add form validation and error messages
- [ ] Implement search/filter functionality
- [ ] Add pagination to data tables
- [ ] Create dashboard statistics/charts
- [ ] Add equipment availability calendar
- [ ] Implement email notifications
- [ ] Add user profile management
- [ ] Implement advanced reporting with charts
- [ ] Add export to PDF/Excel functionality
- [ ] Improve mobile responsiveness

## Dependencies

- **react** (18.2.0) - UI library
- **react-dom** (18.2.0) - React rendering
- **react-router-dom** (6.20.0) - Client-side routing
- **axios** (1.6.0) - HTTP client
- **vite** (5.0.0) - Build tool and dev server

## Notes

- The app uses React Hooks (functional components only)
- State management is simple with Context API
- No complex state library (Redux) is needed currently
- All styling is plain CSS (no Tailwind or Bootstrap)
- API calls use async/await pattern
- Error handling is centralized in API interceptors

## Support

For issues with the backend API, see `../AUTHENTICATION_GUIDE.md` and `../README.md` in the parent directory.
