#!/bin/bash

# Production deployment script for CheapFlights application

set -e

echo "🚀 Starting production deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Load environment variables
source .env

echo "📦 Installing production dependencies..."
pip install -r requirements-production.txt

echo "🗄️ Running database migrations..."
python manage.py migrate --settings=flightfinder.production

echo "📁 Collecting static files..."
python manage.py collectstatic --settings=flightfinder.production --noinput

echo "🌳 Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "🔧 Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:8000 flightfinder.wsgi:application --settings=flightfinder.production --workers 3 --daemon --pid gunicorn.pid

echo "✅ Deployment completed successfully!"
echo "🌐 Your application is now running at: http://localhost:8000"
echo "📋 To stop the server: kill $(cat gunicorn.pid)"
