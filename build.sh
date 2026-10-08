#!/usr/bin/env bash
# Build script for Render deployment

echo "🚀 Starting PennySurveys build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

echo "✅ Build completed successfully!" 