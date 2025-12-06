# GitHub Deployment Guide - Equipment Loan System

Deploy to production using GitHub Actions, Heroku, Vercel, or Railway.

---

## Option 1: GitHub Actions + Heroku (Recommended)

### Step 1: Prepare Repository

1. **Create GitHub repository:**

   ```bash
   git init
   git add .
   git commit -m "Initial commit: Equipment Loan System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/equipment-loan-system.git
   git push -u origin main
   ```

2. **Create `.gitignore` in root:**

   ```text
   venv/
   __pycache__/
   .env
   .DS_Store
   *.pyc
   node_modules/
   dist/
   .env.local
   ```

3. **Create `.env.production` (DO NOT commit):**

   ```env
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-production-key-change-this
   FLASK_ENV=production
   FLASK_DEBUG=False
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

### Step 2: Create Heroku App

1. **Install Heroku CLI:**

   ```bash
   # Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
   # Or: choco install heroku-cli
   ```

2. **Login and create app:**

   ```bash
   heroku login
   heroku create equipment-loan-system
   ```

3. **Add PostgreSQL addon:**

   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables:**

   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set MAIL_SERVER=smtp.gmail.com
   heroku config:set MAIL_PORT=587
   heroku config:set MAIL_USE_TLS=True
   heroku config:set MAIL_USERNAME=your-email@gmail.com
   heroku config:set MAIL_PASSWORD=your-app-password
   ```

### Step 3: Create Deployment Files

1. **Create `Procfile` in root:**

   ```text
   web: python app.py
   ```

2. **Create `runtime.txt` in root:**

   ```text
   python-3.13.0
   ```

3. **Update `requirements.txt` to include Gunicorn:**

   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

4. **Update `Procfile`:**

   ```text
   web: gunicorn app:app
   ```

### Step 4: GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Heroku

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: equipment-loan-system
          heroku_email: your-email@gmail.com
      
      - name: Run migrations
        run: |
          heroku run python -m flask db upgrade
```

### Step 5: Deploy

```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

GitHub Actions will automatically deploy to Heroku!

**Access:** <https://equipment-loan-system.herokuapp.com>

---

## Option 2: Railway.app (Easier)

### Step 1: Connect Repository

1. Go to <https://railway.app>
2. Sign in with GitHub
3. Click "Create New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository

### Step 2: Configure Services

1. **Add PostgreSQL:**
   - Click "Add Service"
   - Select "PostgreSQL"
   - Railway generates DATABASE_URL automatically

2. **Configure Flask app:**
   - Click "Add Service"
   - Select "GitHub Repo"
   - Choose your repo

### Step 3: Set Environment Variables

In Railway dashboard:

```env
FLASK_ENV = production
SECRET_KEY = your-secret-key
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your-email
MAIL_PASSWORD = your-password
```

### Step 4: Deploy

Just push to GitHub! Railway automatically deploys.

**Access:** <https://your-app.railway.app>

---

## Option 3: Vercel (Frontend Only) + Railway (Backend)

### Step 1: Deploy Backend (Railway)

See Option 2 above

### Step 2: Deploy Frontend

1. Go to <https://vercel.com>
2. Click "New Project"
3. Import your GitHub repository
4. Set build command: `cd frontend && npm run build`
5. Set output directory: `frontend/dist`
6. Add environment variable:

   ```env
   VITE_API_URL=https://your-backend.railway.app
   ```

### Step 3: Update Frontend Config

Create `frontend/.env.production`:

```env
VITE_API_URL=https://your-backend.railway.app/api
```

Update `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = process.env.VITE_API_URL || '/api';
```

---

## Option 4: Docker Deployment (Scalable)

### Step 1: Create Dockerfile

Create `Dockerfile` in root:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Build frontend
RUN cd frontend && npm install && npm run build

# Expose port
EXPOSE 5000

# Set environment
ENV FLASK_ENV=production

# Run app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.9'

services:
  db:
    image: postgres:18-alpine
    environment:
      POSTGRES_DB: equipment_loan_db
      POSTGRES_USER: equipment_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://equipment_user:${DB_PASSWORD}@db:5432/equipment_loan_db
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
      MAIL_SERVER: ${MAIL_SERVER}
      MAIL_PORT: ${MAIL_PORT}
      MAIL_USERNAME: ${MAIL_USERNAME}
      MAIL_PASSWORD: ${MAIL_PASSWORD}
    depends_on:
      - db
    volumes:
      - ./:/app

volumes:
  postgres_data:
```

### Step 3: Deploy to DigitalOcean/AWS

```bash
docker-compose up -d
```

---

## Production Checklist

Before deploying:

### Backend

- [ ] Change `SECRET_KEY` to secure random value
- [ ] Set `FLASK_DEBUG=False`
- [ ] Set `FLASK_ENV=production`
- [ ] Configure real email service (Gmail App Passwords)
- [ ] Set up PostgreSQL backups
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring (Sentry, LogRocket)
- [ ] Enable rate limiting
- [ ] Set up logging

### Frontend

- [ ] Build production bundle: `npm run build`
- [ ] Update API URL to production backend
- [ ] Enable analytics
- [ ] Configure error tracking
- [ ] Test all features
- [ ] Verify mobile responsiveness

### Security

- [ ] Set `SECURE_COOKIES=True`
- [ ] Set `SECURE_HSTS=True`
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Monitor error logs

### Database

- [ ] Regular backups configured
- [ ] Slow query logging
- [ ] Index optimization
- [ ] Connection pool sizing
- [ ] Monitoring setup

---

## Post-Deployment Testing

### 1. Health Checks

```bash
curl https://your-app.herokuapp.com/api/health
```

Should return: `{"status": "ok"}`

### 2. Authentication

```bash
curl -X POST https://your-app.herokuapp.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 3. Load Test

```bash
# Small load test
locust -f locustfile.py --host=https://your-app.herokuapp.com -u 10 -r 1
```

### 4. SSL Certificate

Verify HTTPS:

```bash
curl -I https://your-app.herokuapp.com
# Should show: HTTP/2 200
# And certificate is valid
```

---

## Monitoring & Maintenance

### Heroku Logs

```bash
heroku logs -t
heroku logs --tail
```

### Database Backups

```bash
# Create backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download

# Restore
heroku pg:backups:restore
```

### Update Dependencies

```bash
# Check for updates
pip list --outdated
npm outdated

# Update
pip install --upgrade -r requirements.txt
npm update
```

### Monitor Performance

1. Enable New Relic (Heroku addon):

   ```bash
   heroku addons:create newrelic:wayne
   ```

2. View logs:

   ```bash
   heroku logs -n 100
   ```

3. Check dyno hours:

   ```bash
   heroku ps
   ```

---

## Custom Domain Setup

### Heroku

```bash
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com
```

Update DNS:

```text
CNAME www.yourdomain.com → equipment-loan-system.herokuapp.com
```

### Railway/Vercel

1. Go to dashboard
2. Settings → Domains
3. Add your domain
4. Update DNS records

---

## Troubleshooting Deployment

### Issue: "H14 No web processes running"

```bash
# Solution: Restart dyno
heroku dyno:restart
```

### Issue: "Database connection failed"

```bash
# Check config
heroku config | grep DATABASE_URL

# Verify connection
heroku pg:psql < script.sql
```

### Issue: Static files not loading

```bash
# Solution: Build frontend first
npm run build
```

### Issue: Email not sending

```bash
# Check config
heroku config | grep MAIL_

# Test SMTP
python -c "from email_service import test_mail; test_mail()"
```

---

## Continuous Deployment

### GitHub Actions Workflow

File: `.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        run: pytest test_app.py -v
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Build frontend
        run: |
          cd frontend
          npm install
          npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: equipment-loan-system
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

---

## Environment Variables for Different Stages

### Development (.env)

```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=postgresql://...localhost
SECRET_KEY=dev-key-change-in-production
```

### Staging (.env.staging)

```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://...staging
SECRET_KEY=staging-key-change
```

### Production (.env.production)

```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://...production
SECRET_KEY=production-key-very-secure
```

---

## Summary

| Option | Difficulty | Cost | Setup Time |
|--------|-----------|------|-----------|
| Heroku | Medium | Free-$25/mo | 30 min |
| Railway | Easy | Free-$5/mo | 15 min |
| Vercel + Railway | Easy | Free | 20 min |
| Docker | Hard | Variable | 1+ hour |

**Recommendation:** Start with Railway for simplicity, upgrade to Docker for scale.

---

**Deployment Status:** Ready
**Next:** Choose deployment option and follow steps above
**Support:** Check Heroku/Railway/Vercel documentation for detailed guides
