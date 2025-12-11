# 🚀 Equipment Loan System - Quick Start

## Installation (One Click!)

### Requirements
- Windows 7 or later
- Python 3.10+ (download from https://www.python.org/)
- Node.js 16+ (download from https://nodejs.org/)

**Important:** When installing Python and Node.js, make sure to check "Add to PATH"

---

## Installation Steps

### Step 1: Double-click INSTALL.bat

Simply double-click `INSTALL.bat` in the project folder. The script will:
- ✅ Check for Python and Node.js
- ✅ Create Python virtual environment
- ✅ Install Python packages (Flask, SQLAlchemy, etc.)
- ✅ Install Node.js packages (React, Vite, etc.)
- ✅ Load sample data into database
- ✅ Display login credentials

Takes about 2-3 minutes depending on internet speed.

---

## Running the Application

### Option 1: Automatic (Recommended)
Double-click `START.bat` - it will:
- Start Flask backend on http://localhost:5000
- Start React frontend on http://localhost:3000
- Automatically open the app in your browser

### Option 2: Manual (if START.bat doesn't work)
Open two terminals:

**Terminal 1 - Backend:**
```bash
venv\Scripts\activate.bat
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open http://localhost:3000 in your browser

---

## Login Credentials

After running INSTALL.bat, you can log in with:

| Role | Username | Password |
|------|----------|----------|
| Admin | administrator | 655321 |
| Staff | staff1 | 655322 |
| Student | borrower1 | 655323 |

---

## File Structure

```
equipment-loan-system/
├── INSTALL.bat           ← Run this first
├── START.bat             ← Run this to start the app
├── UNINSTALL.bat         ← Run this to clean up
├── app.py                ← Flask backend
├── load_sample_data.py   ← Sample data loader
├── models.py             ← Database models
├── routes.py             ← API endpoints
├── frontend/             ← React application
│   ├── package.json
│   ├── vite.config.js
│   └── src/
└── venv/                 ← Python virtual environment (created by INSTALL.bat)
```

---

## Troubleshooting

### "Python not found"
- Install Python from https://www.python.org/
- During installation, check ✓ "Add Python to PATH"
- Restart your computer after installing

### "Node.js not found"
- Install Node.js from https://nodejs.org/
- During installation, check ✓ "Add to PATH"
- Restart your computer after installing

### "Port 5000 or 3000 already in use"
- Something else is using the port
- Close other applications or change ports in the code
- Or wait a few minutes and try again

### Installation fails
- Delete the `venv` folder
- Delete `frontend/node_modules` folder
- Run INSTALL.bat again

### Database issues
- Run UNINSTALL.bat to clean up
- Run INSTALL.bat again to start fresh

---

## Uninstalling

To remove everything and start over:
Double-click `UNINSTALL.bat` and confirm the removal.

Then run INSTALL.bat again to reinstall.

---

## Need Help?

Check the detailed documentation:
- `INSTALLATION.md` - Detailed setup guide
- `TESTING_GUIDE.md` - How to test the system
- `TROUBLESHOOTING_INDEX.md` - Common issues and fixes

---

**Ready?** Double-click `INSTALL.bat` to get started! 🎉
