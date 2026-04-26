# Ryanair Cheap Flight Finder

A Django React application that finds the cheapest Ryanair flights within selected date intervals.

## Features

- Search for cheapest Ryanair flights within flexible date ranges
- Support for one-way and round-trip flights
- Real-time flight search using Ryanair's API
- Beautiful, responsive React frontend
- RESTful Django backend with API endpoints
- Flight search history tracking

## Tech Stack

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- Django CORS Headers 4.3.1
- SQLite database
- Python 3.10+

### Frontend
- React 18 with TypeScript
- Axios for API requests
- Date-fns for date handling
- CSS Grid and Flexbox for responsive design

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the project directory:
```bash
cd /home/ieva/projektai/cheapflights/return_cheap_flights
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the Django development server:
```bash
source venv/bin/activate && python manage.py runserver
```

The Django API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The React app will be available at `http://localhost:3000`

## Usage

1. Make sure both the Django backend and React frontend are running
2. Open your browser and go to `http://localhost:3000`
3. Select origin and destination airports from the dropdowns
4. Choose your departure date range
5. Optionally select return dates for round-trip flights
6. Set the number of passengers
7. Click "Search Flights" to find the cheapest options

## API Endpoints

### Airports
- `GET /api/airports/` - Get all airports from Ryanair API
- `GET /airports/` - List saved airports in database

### Flight Search
- `POST /api/search/ryanair/` - Search for Ryanair flights
- `GET /api/flights/cheapest/` - Get cheapest flights from database

### Flight Management
- `GET /flights/` - List all saved flights
- `POST /flights/` - Create a new flight record
- `GET /searches/` - List all flight searches
- `POST /searches/` - Create a new flight search record

## Project Structure

```
return_cheap_flights/
├── flightfinder/          # Django project settings
│   ├── __init__.py
│   ├── settings.py        # Django configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py
├── flights/              # Django app for flight functionality
│   ├── migrations/       # Database migrations
│   ├── __init__.py
│   ├── admin.py         # Django admin configuration
│   ├── apps.py         # App configuration
│   ├── models.py       # Database models
│   ├── ryanair_api.py  # Ryanair API integration
│   ├── serializers.py  # REST framework serializers
│   ├── urls.py         # App URL routing
│   └── views.py        # API views
├── frontend/           # React frontend
│   ├── public/         # Static files
│   ├── src/
│   │   ├── api/        # API service functions
│   │   ├── components/ # React components
│   │   ├── types/      # TypeScript type definitions
│   │   ├── App.tsx     # Main app component
│   │   └── index.tsx   # Entry point
│   └── package.json
├── venv/              # Python virtual environment
├── db.sqlite3         # SQLite database
├── manage.py          # Django management script
├── requirements.txt    # Python dependencies
└── README.md         # This file
```

## Notes

- The application uses Ryanair's public API to fetch real-time flight data
- Flight prices and availability are subject to change
- The API may have rate limits, so excessive requests might be temporarily blocked
- All flight searches are saved to the database for analytics and debugging

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the Django server is running and CORS is properly configured
2. **API Timeouts**: Ryanair's API might be slow during peak times
3. **No Flights Found**: Try different date ranges or airport combinations
4. **Virtual Environment Issues**: Ensure Python 3.10+ is installed and venv is created properly

### Development Tips

- Use `python manage.py shell` to test API functions
- Check the Django admin panel at `http://localhost:8000/admin/` to view saved data
- Monitor browser console for frontend debugging
- Use Django's built-in debugging tools for backend issues

## License

This project is for educational purposes only. Please respect Ryanair's terms of service when using their API.
