# Production Deployment Guide

## Overview

This guide covers deploying the CheapFlights application to production with real Ryanair API access.

## Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Docker and Docker Compose installed
- Domain name pointing to your server
- SSL certificate (Let's Encrypt recommended)
- PostgreSQL database
- Redis for caching

## Quick Start (Docker Compose)

### 1. Prepare Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd cheapflights

# Copy environment template
cp .env.example .env

# Edit .env with your production values
nano .env
```

### 2. Configure Environment Variables

Edit `.env` file with your actual values:

```bash
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=cheapflights
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/1

DOMAIN=yourdomain.com
```

### 3. Deploy with Docker Compose

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --settings=flightfinder.production

# Create superuser (optional)
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser --settings=flightfinder.production

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --settings=flightfinder.production --noinput
```

### 4. Setup SSL Certificate

```bash
# Install certbot
sudo apt update
sudo apt install certbot

# Generate SSL certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to nginx directory
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem
```

### 5. Restart Services

```bash
docker-compose -f docker-compose.prod.yml restart
```

## Manual Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3.11 python3.11-venv python3-pip postgresql postgresql-contrib redis-server nginx certbot -y

# Create user
sudo useradd -m -s /bin/bash cheapflights
sudo usermod -aG sudo cheapflights
```

### 2. Application Setup

```bash
# Switch to application user
sudo su - cheapflights

# Clone repository
git clone <your-repo-url>
cd cheapflights

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-production.txt
```

### 3. Database Setup

```bash
# Create database
sudo -u postgres createdb cheapflights
sudo -u postgres createuser cheapflights
sudo -u postgres psql -c "ALTER USER cheapflights PASSWORD 'your-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cheapflights TO cheapflights;"
```

### 4. Environment Configuration

```bash
# Copy and edit environment file
cp .env.example .env
nano .env
```

### 5. Application Deployment

```bash
# Run migrations
python manage.py migrate --settings=flightfinder.production

# Collect static files
python manage.py collectstatic --settings=flightfinder.production --noinput

# Create superuser
python manage.py createsuperuser --settings=flightfinder.production

# Build frontend
cd frontend
npm install
npm run build
cd ..
```

### 6. Gunicorn Service

Create `/etc/systemd/system/cheapflights.service`:

```ini
[Unit]
Description=CheapFlights Gunicorn daemon
After=network.target

[Service]
User=cheapflights
Group=cheapflights
WorkingDirectory=/home/cheapflights/cheapflights
Environment="PATH=/home/cheapflights/cheapflights/venv/bin"
ExecStart=/home/cheapflights/cheapflights/venv/bin/gunicorn --workers 3 --bind unix:/home/cheapflights/cheapflights/cheapflights.sock flightfinder.wsgi:application --settings=flightfinder.production

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable cheapflights
sudo systemctl start cheapflights
```

### 7. Nginx Configuration

Copy `nginx.conf` to `/etc/nginx/sites-available/cheapflights` and create symlink:

```bash
sudo cp nginx.conf /etc/nginx/sites-available/cheapflights
sudo ln -s /etc/nginx/sites-available/cheapflights /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-very-secret-key` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed domains | `yourdomain.com,www.yourdomain.com` |
| `DB_NAME` | Database name | `cheapflights` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `secure-password` |
| `DB_HOST` | Database host | `localhost` or `db` |
| `REDIS_URL` | Redis connection | `redis://localhost:6379/1` |
| `DOMAIN` | Your domain | `yourdomain.com` |

## SSL Setup

### Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring

### Health Check

```bash
# Check application status
curl -f https://yourdomain.com/api/airports/ || exit 1
```

### Logs

```bash
# Django logs
tail -f django.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Gunicorn logs
sudo journalctl -u cheapflights -f
```

## Performance Optimization

1. **Enable Redis Caching**: Configure Redis for session and application caching
2. **Database Optimization**: Use connection pooling and optimize queries
3. **CDN**: Serve static files via CDN
4. **Load Balancing**: Use multiple Gunicorn workers behind load balancer

## Security

1. **Firewall**: Configure UFW to allow only necessary ports
2. **Updates**: Keep system and dependencies updated
3. **Backups**: Regular database backups
4. **Monitoring**: Set up error monitoring (Sentry recommended)

## Troubleshooting

### Common Issues

1. **DNS Resolution**: Ensure server can resolve Ryanair API domains
2. **Database Connection**: Check database credentials and connectivity
3. **Static Files**: Verify static files are collected and accessible
4. **SSL**: Ensure certificates are properly configured

### Testing Ryanair API

```bash
# Test DNS resolution
nslookup api.ryanair.com
nslookup desktopapps.ryanair.com

# Test API connectivity
curl -I https://api.ryanair.com/aggregate/3/common
```

## Support

For deployment issues:
1. Check logs for error messages
2. Verify environment variables
3. Test network connectivity
4. Check system resources (memory, disk space)
