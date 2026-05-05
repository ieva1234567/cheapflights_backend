from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Airport, Flight, FlightSearch
from .serializers import (
    AirportSerializer, FlightSerializer, FlightSearchSerializer,
    RyanairFlightSerializer, FlightSearchRequestSerializer
)
from .ryanair_api import RyanairAPI


class AirportListCreateView(generics.ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class FlightListCreateView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightSearchListCreateView(generics.ListCreateAPIView):
    queryset = FlightSearch.objects.all()
    serializer_class = FlightSearchSerializer


class FlightSearchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FlightSearch.objects.all()
    serializer_class = FlightSearchSerializer


@api_view(['GET'])
def get_airports(request):
    """Get all airports from Ryanair API"""
    api = RyanairAPI()
    airports = api.get_airports()
    
    # Save airports to database
    for airport_data in airports:
        Airport.objects.get_or_create(
            iata_code=airport_data['iata_code'],
            defaults={
                'name': airport_data['name'],
                'city': airport_data['city'],
                'country': airport_data['country']
            }
        )
    
    serializer = AirportSerializer(Airport.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def search_ryanair_flights(request):
    """Search for cheapest Ryanair flights within date ranges"""
    serializer = FlightSearchRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Initialize Ryanair API
    api = RyanairAPI()
    
    try:
        # Search for flights
        destination_iata = data.get('destination_iata') or None
        
        # Handle both date objects and string dates
        def format_date(date_obj):
            if date_obj is None:
                return None
            if hasattr(date_obj, 'strftime'):
                return date_obj.strftime('%Y-%m-%d')
            return str(date_obj)  # Convert string dates to string
        
        result = api.get_cheapest_flights_in_range(
            origin_iata=data['origin_iata'],
            destination_iata=destination_iata,
            departure_date_from=format_date(data['departure_date_from']),
            departure_date_to=format_date(data['departure_date_to']),
            return_date_from=format_date(data.get('return_date_from', None)),
            return_date_to=format_date(data.get('return_date_to', None)),
            passengers=data['passengers']
        )
        
        # Save search to database
        origin_airport, _ = Airport.objects.get_or_create(iata_code=data['origin_iata'])
        
        # For all destinations search, create a placeholder destination
        if destination_iata:
            destination_airport, _ = Airport.objects.get_or_create(iata_code=destination_iata)
        else:
            # Create a placeholder for "all destinations"
            destination_airport, _ = Airport.objects.get_or_create(
                iata_code='ALL',
                defaults={'name': 'All Destinations', 'city': 'Multiple', 'country': 'Multiple'}
            )
        
        flight_search = FlightSearch.objects.create(
            origin=origin_airport,
            destination=destination_airport,
            departure_date_from=data['departure_date_from'],
            departure_date_to=data['departure_date_to'],
            return_date_from=data.get('return_date_from'),
            return_date_to=data.get('return_date_to'),
            passengers=data['passengers']
        )
        
        # Serialize flight results
        outbound_serializer = RyanairFlightSerializer(result['outbound'], many=True)
        return_serializer = RyanairFlightSerializer(result['return'], many=True)
        
        response_data = {
            'search_id': flight_search.id,
            'outbound_flights': outbound_serializer.data,
            'return_flights': return_serializer.data,
            'total_flights_found': result['total_flights_found']
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to search flights: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_cheapest_flights(request):
    """Get cheapest flights from database"""
    origin = request.query_params.get('origin')
    destination = request.query_params.get('destination')
    
    flights = Flight.objects.all()
    
    if origin:
        flights = flights.filter(origin__iata_code=origin)
    if destination:
        flights = flights.filter(destination__iata_code=destination)
    
    # Order by price
    flights = flights.order_by('price')[:20]  # Top 20 cheapest
    
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data)
