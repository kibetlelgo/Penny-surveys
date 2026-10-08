# PennySurveys Deployment Guide for Truehost

This guide will help you deploy your PennySurveys Django application to Truehost.

## Prerequisites

- Truehost hosting account
- Domain name (optional but recommended)
- Git repository of your project

## Step 1: Prepare Your Project

### 1.1 Update Settings
The project is already configured for deployment with:
- Environment-based configuration
- Static files handling with WhiteNoise
- Security settings for production
- Database configuration

### 1.2 Generate a Secure Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 2: Upload to Truehost

### Method 1: Using Git (Recommended)
1. Push your code to GitHub/GitLab
2. In Truehost cPanel, go to "Git Version Control"
3. Clone your repository
4. Set up the deployment path

### Method 2: Using File Manager
1. Compress your project folder
2. Upload via Truehost File Manager
3. Extract in your public_html directory

## Step 3: Configure Environment Variables

In Truehost cPanel, set these environment variables:

```bash
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=sqlite:///db.sqlite3
```

## Step 4: Set Up Python Environment

### 4.1 Create Virtual Environment
```bash
cd public_html
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### 4.2 Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 5: Configure Database

### Option A: SQLite (Default)
- No additional setup needed
- Database file will be created automatically

### Option B: MySQL (Recommended for production)
1. Create MySQL database in Truehost cPanel
2. Update DATABASE_URL:
```bash
DATABASE_URL=mysql://username:password@localhost/database_name
```

## Step 6: Run Django Commands

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

## Step 7: Configure Web Server

### 7.1 Create .htaccess file
Create a `.htaccess` file in your public_html directory:

```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ /wsgi.py/$1 [QSA,L]

# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
```

### 7.2 Create wsgi.py file
Create a `wsgi.py` file in your public_html directory:

```python
#!/usr/bin/env python3
import os
import sys

# Add your project directory to Python path
sys.path.insert(0, '/home/username/public_html')

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'PennySurveys.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 8: Test Your Application

1. Visit your domain
2. Check if the application loads correctly
3. Test user registration and login
4. Verify static files are loading

## Troubleshooting

### Common Issues:

1. **500 Internal Server Error**
   - Check error logs in cPanel
   - Verify SECRET_KEY is set
   - Ensure DEBUG=False in production

2. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT path
   - Verify .htaccess configuration

3. **Database errors**
   - Check DATABASE_URL format
   - Ensure database exists and is accessible
   - Run migrations: `python manage.py migrate`

4. **Import errors**
   - Verify all dependencies are installed
   - Check Python path in wsgi.py
   - Ensure virtual environment is activated

### Useful Commands:

```bash
# Check Django version
python -m django --version

# List installed packages
pip list

# Check Django settings
python manage.py check --deploy

# View error logs
tail -f /home/username/logs/error.log
```

## Security Checklist

- [ ] DEBUG=False in production
- [ ] SECRET_KEY is secure and unique
- [ ] ALLOWED_HOSTS is properly configured
- [ ] HTTPS is enabled
- [ ] Database credentials are secure
- [ ] Static files are served correctly
- [ ] Error pages are configured

## Performance Optimization

1. **Enable caching** (if needed)
2. **Use CDN** for static files
3. **Optimize database queries**
4. **Enable compression**

## Support

If you encounter issues:
1. Check Truehost error logs
2. Verify all configuration steps
3. Test locally first
4. Contact Truehost support if needed

## Maintenance

Regular maintenance tasks:
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Backup database regularly
- Monitor error logs
- Keep Django updated 