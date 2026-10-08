#!/usr/bin/env python3
"""
Deployment script for PennySurveys on Truehost
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def main():
    print("🚀 Starting PennySurveys deployment...")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Run migrations
    run_command("python manage.py migrate", "Running database migrations")
    
    # Create superuser if needed (optional)
    print("📝 To create a superuser, run: python manage.py createsuperuser")
    
    print("✅ Deployment completed successfully!")
    print("🌐 Your application should now be running on Truehost")

if __name__ == "__main__":
    main() 