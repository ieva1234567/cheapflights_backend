# Production Dockerfile for CheapFlights application

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-production.txt /app/
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy project
COPY . /app/

# Create static files directory
RUN mkdir -p /app/staticfiles

# Build React frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Return to app directory
WORKDIR /app

# Collect static files
RUN python manage.py collectstatic --settings=flightfinder.production --noinput

# Expose port
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "flightfinder.wsgi:application", "--settings", "flightfinder.production"]
