# Render Deployment Guide for Django TODO API

This guide walks you through deploying the Django TODO API to Render as a Docker Web Service with a PostgreSQL database.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Production Settings Updates](#production-settings-updates)
3. [Step-by-Step Render Deployment](#step-by-step-render-deployment)
4. [Environment Variables Configuration](#environment-variables-configuration)
5. [Database Integration](#database-integration)
6. [Verification & Troubleshooting](#verification--troubleshooting)

---

## Prerequisites

- Active GitHub account with the project repository pushed
- Render account (sign up at [render.com](https://render.com))
- Generated Django SECRET_KEY for production

### Generate a Secure Django SECRET_KEY

Run this in your local terminal:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output — you'll need it for the environment variables on Render.

---

## Production Settings Updates

### ✅ Already Updated in This Project

The project's `settings.py` has been updated with production-ready configurations:

**1. Environment Variable Support:**

```python
# SECRET_KEY - loads from DJANGO_SECRET_KEY environment variable
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-your-secret-key-change-in-production'
)

# DEBUG - defaults to False for production safety
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

# ALLOWED_HOSTS - accepts comma-separated values
ALLOWED_HOSTS_ENV = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',')]
```

**2. Database Support:**

```python
# Uses PostgreSQL via DATABASE_URL when deployed to Render
# Falls back to SQLite locally
import dj_database_url

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

**3. Static Files with WhiteNoise:**

```python
# WhiteNoise handles static files without separate nginx
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file serving
    ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**4. Security Headers (Production Only):**

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    # ... other security settings
```

### ✅ Dependencies Added

Updated `requirements.txt` includes:

```
whitenoise==6.6.0        # Static file serving
dj-database-url==2.1.0   # PostgreSQL support
```

### ✅ Build Script Created

`render-build.sh` defines the build steps:

```bash
#!/bin/bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## Step-by-Step Render Deployment

### Step 1: Push Code to GitHub

Ensure your project is pushed to GitHub:

```bash
git add .
git commit -m "Update production settings for Render deployment"
git push origin main
```

Files committed:
- Updated `todo_api/settings.py`
- Updated `requirements.txt` (with whitenoise, dj-database-url)
- New `render-build.sh`
- `Dockerfile` (already present)

### Step 2: Sign In to Render Dashboard

1. Go to [render.com](https://render.com)
2. Click **"Sign in"** → Use your GitHub account
3. Grant Render permission to access your repositories

### Step 3: Create a New PostgreSQL Database

1. In Render dashboard, click **"New +"** in top-right
2. Select **"PostgreSQL"**
3. Configure:
   - **Name:** `todo-api-db`
   - **Database:** `todo_api`
   - **User:** `todouser`
   - **Region:** Choose closest to your location
   - **PostgreSQL Version:** 15 (or latest)
   - **Pricing Plan:** Free tier (if available)
4. Click **"Create Database"**
5. **⚠️ Important:** Wait for the database to finish provisioning (~2 minutes)
6. Copy the **Internal Database URL** (you'll use this shortly)

**Example URL format:**
```
postgresql://todouser:password123@dpg-xxx-xxx.oregon-postgres.render.com:5432/todo_api
```

### Step 4: Create a New Web Service

1. In Render dashboard, click **"New +"** in top-right
2. Select **"Web Service"**
3. Configure:

#### 4a: Repository Connection
- **GitHub Repository:** Select your TODO API repository
- Click **"Connect"** to authorize Render to deploy from your repo

#### 4b: Service Configuration
- **Name:** `todo-api` (this becomes your Render URL)
- **Region:** Same as database (for latency)
- **Runtime:** Select **"Docker"** (not "Python")
- **Branch:** `main`

#### 4c: Docker Configuration
- **Dockerfile Path:** `Dockerfile` (default)
- **Docker Command:** Leave empty (uses CMD from Dockerfile)

#### 4d: Build Command
Render needs to run migrations and collect static files before starting:

```bash
bash render-build.sh
```

**Note:** This executes the build steps from `render-build.sh` in the build environment.

#### 4e: Start Command
```bash
gunicorn todo_api.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 60
```

**Note:** Ensure this is the start command (not build command)

### Step 5: Configure Environment Variables

In the Render Web Service dashboard, scroll to **"Environment"** section:

Click **"Add Environment Variable"** and add each:

| Key | Value | Notes |
|-----|-------|-------|
| `DEBUG` | `False` | ⚠️ Always False in production |
| `DJANGO_SECRET_KEY` | `<generated-secret-key>` | Use the key generated earlier |
| `ALLOWED_HOSTS` | `<your-render-service>.onrender.com` | Replace `<your-render-service>` with your service name |
| `DATABASE_URL` | `<internal-database-url>` | Paste the PostgreSQL URL from Step 3 |
| `DJANGO_LOG_LEVEL` | `INFO` | Logging level |

**Example ALLOWED_HOSTS:**
```
todo-api.onrender.com
```

**Important:** The `DATABASE_URL` should be the **Internal Database URL** from Render PostgreSQL (not External).

### Step 6: Deploy

1. Click **"Create Web Service"** (bottom of form)
2. **Wait for deployment** (~5-10 minutes)
   - You'll see logs streaming in the Render dashboard
   - Look for:
     ```
     INFO: Starting gunicorn X.X.X
     INFO: Listening at: http://0.0.0.0:8000
     INFO: Worker spawned (pid: xxx)
     ```
3. Once complete, you'll see a green checkmark and the service URL

---

## Environment Variables Configuration

### Required Environment Variables

**On Render Dashboard → Environment:**

```
DEBUG=False
DJANGO_SECRET_KEY=<your-generated-secret-key>
ALLOWED_HOSTS=todo-api.onrender.com
DATABASE_URL=postgresql://todouser:<password>@dpg-xxx.oregon-postgres.render.com:5432/todo_api
DJANGO_LOG_LEVEL=INFO
```

### Optional Environment Variables

- `SECURE_SSL_REDIRECT=True` - Forces HTTPS (enabled by default when DEBUG=False)
- `WORKERS=4` - Number of Gunicorn workers (default: 4)

---

## Database Integration

### How Render PostgreSQL Works

1. **Automatic Provisioning:** When you create a PostgreSQL service on Render, it's automatically managed
2. **Connection String:** Render provides `DATABASE_URL` with the connection credentials
3. **Django Integration:** `dj-database-url` library automatically configures Django with the `DATABASE_URL`

### Connecting Django to Render PostgreSQL

The project's `settings.py` automatically detects and uses the PostgreSQL database:

```python
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
```

When `DATABASE_URL` environment variable is set (which Render does automatically), Django uses PostgreSQL instead of SQLite.

### Database Migration on Deployment

The `render-build.sh` script runs automatically during the build process:

```bash
python manage.py migrate
```

This ensures the database schema is created when the app is deployed.

### Verifying Database Connection

After deployment, check if migrations ran:

1. Go to Render dashboard → Web Service
2. Click **"Logs"** tab
3. Look for lines like:
   ```
   Running migrations:
     Applying todos.0001_initial... OK
   ```

---

## Verification & Troubleshooting

### ✅ Verify Deployment Success

1. **Get Your Public URL:**
   - Render dashboard → Web Service → Copy the URL (e.g., `https://todo-api.onrender.com`)

2. **Test the API:**
   - Open browser: `https://todo-api.onrender.com/api/todos/`
   - You should see:
     ```json
     {
       "count": 0,
       "next": null,
       "previous": null,
       "results": []
     }
     ```

3. **Test Admin Panel:**
   - Open: `https://todo-api.onrender.com/admin/`
   - You should see the Django admin login page

### 🔍 Check Logs

In Render dashboard:

1. Click Web Service → **"Logs"** tab
2. View real-time logs as requests come in
3. Common log patterns:
   ```
   INFO: Starting gunicorn              # Startup
   INFO: Worker spawned (pid: xxx)      # Worker process
   INFO: GET /api/todos/ HTTP/1.1 200   # Successful API request
   ```

### ❌ Troubleshooting: Service Won't Start

**Error in logs:** `ModuleNotFoundError: No module named 'whitenoise'`

**Solution:** Wait for `pip install` to complete in build logs. Check that `render-build.sh` ran successfully.

**Error in logs:** `django.core.exceptions.DisallowedHost`

**Solution:** Add your Render service URL to `ALLOWED_HOSTS` environment variable. Example:
```
ALLOWED_HOSTS=todo-api.onrender.com
```

**Error in logs:** `psycopg2: connection refused`

**Solution:**
1. Ensure `DATABASE_URL` is set correctly
2. Verify the PostgreSQL database is running (check Render → PostgreSQL service status)
3. Use the **Internal Database URL** (not External URL)

### ❌ Troubleshooting: Database Migrations Failed

**Error:** `ERROR: no such table: todos_todo`

**Solution:** Migrations didn't run. Check:
1. Build logs show `python manage.py migrate` ran successfully
2. `DATABASE_URL` environment variable is set
3. PostgreSQL database is ready (wait a few minutes after creation)
4. Manually trigger in Render shell:
   ```bash
   python manage.py migrate
   ```

### ❌ Troubleshooting: Static Files Broken (Admin looks broken)

**Symptoms:** Admin panel loads but styling is missing

**Solution:** 
1. Check that `whitenoise` is in `requirements.txt`
2. Verify build logs show `python manage.py collectstatic --noinput` succeeded
3. Rebuild the service: Dashboard → Web Service → Settings → Scroll down → "Restart Latest Deployment"

### 🔧 Manual Troubleshooting via Render Shell

Access the running container directly:

1. Render dashboard → Web Service → **"Shell"** tab
2. Run diagnostic commands:
   ```bash
   python manage.py check                    # Check configuration
   python manage.py migrate --plan           # Preview migrations
   python manage.py shell                    # Django shell
   echo $DATABASE_URL                        # Check env vars
   ```

---

## Post-Deployment Configuration

### Create a Superuser (Admin Account)

Once deployed, create an admin account:

1. Render dashboard → Web Service → **"Shell"** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts to create admin username/password
4. Log in to admin: `https://your-service.onrender.com/admin/`

### Test API Endpoints

In a terminal or with curl:

```bash
# Get all TODOs
curl https://your-service.onrender.com/api/todos/

# Create a TODO
curl -X POST https://your-service.onrender.com/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","description":"At the store"}'

# List with pagination
curl https://your-service.onrender.com/api/todos/?page=1
```

### Monitor & Scale

- **View Metrics:** Dashboard → Web Service → "Metrics" tab
- **View Logs:** Dashboard → Web Service → "Logs" tab
- **Scale Workers:** Update `gunicorn workers` in the Start Command
- **Change Instance Size:** Dashboard → Settings → "Instance Type"

---

## Production Deployment Checklist

Before considering production-ready:

- ✅ `DEBUG=False` in environment variables
- ✅ `DJANGO_SECRET_KEY` is a strong, random key
- ✅ `ALLOWED_HOSTS` includes your Render domain
- ✅ `DATABASE_URL` uses the PostgreSQL connection string
- ✅ Database migrations ran successfully
- ✅ Static files collected (check `/static/` loads)
- ✅ Admin panel accessible and functional
- ✅ API endpoints return correct responses
- ✅ Health checks pass (Render status green)
- ✅ Logs show no ERROR messages
- ✅ Created a superuser account

---

## Redeploying Changes

When you push new code to GitHub, Render automatically redeploys:

1. Push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

2. Render detects the push and starts a new deployment

3. You can watch the deployment in Render dashboard → "Deployments" tab

**Manual Redeploy:**
- Dashboard → Web Service → Settings → "Redeploy Latest"

---

## Useful Render Links

- **Dashboard:** https://dashboard.render.com
- **Service Logs:** https://dashboard.render.com/services/[service-id]/logs
- **Documentation:** https://render.com/docs

---

## Summary

Your Django TODO API is now deployed on Render with:

- ✅ Docker containerization
- ✅ PostgreSQL database
- ✅ Automatic HTTPS
- ✅ Static file serving (WhiteNoise)
- ✅ Environment-based configuration
- ✅ Production security headers
- ✅ Automatic deployments from GitHub

**Public API URL:** `https://your-service-name.onrender.com/api/todos/`
