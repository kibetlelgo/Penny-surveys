"""
Truehost-specific configuration for PennySurveys
"""

import os

# Truehost environment variables
TRUEHOST_ENV_VARS = {
    'DEBUG': 'False',
    'SECRET_KEY': 'your-secret-key-here',  # Change this to a secure secret key
    'ALLOWED_HOSTS': 'your-domain.com,www.your-domain.com',  # Replace with your actual domain
    'DATABASE_URL': 'sqlite:///db.sqlite3',  # For SQLite, or use MySQL/PostgreSQL URL
}

# Truehost-specific settings
TRUEHOST_SETTINGS = {
    'STATIC_ROOT': '/home/username/public_html/staticfiles',  # Replace 'username' with your Truehost username
    'MEDIA_ROOT': '/home/username/public_html/media',  # Replace 'username' with your Truehost username
    'WSGI_APPLICATION': 'PennySurveys.wsgi.application',
}

def get_truehost_env_vars():
    """Get environment variables for Truehost"""
    return TRUEHOST_ENV_VARS

def get_truehost_settings():
    """Get Truehost-specific settings"""
    return TRUEHOST_SETTINGS

if __name__ == "__main__":
    print("Truehost Configuration for PennySurveys")
    print("=" * 40)
    print("\nEnvironment Variables to set in Truehost:")
    for key, value in TRUEHOST_ENV_VARS.items():
        print(f"{key}={value}")
    
    print("\nTruehost Settings:")
    for key, value in TRUEHOST_SETTINGS.items():
        print(f"{key}: {value}") 