from django.urls import path
from . import views

urlpatterns = [
    # Airport endpoints
    path('airports/', views.AirportListCreateView.as_view(), name='airport-list-create'),
    path('airports/<int:pk>/', views.AirportDetailView.as_view(), name='airport-detail'),
    path('api/airports/', views.get_airports, name='get-ryanair-airports'),
    
    # Flight endpoints
    path('flights/', views.FlightListCreateView.as_view(), name='flight-list-create'),
    path('flights/<int:pk>/', views.FlightDetailView.as_view(), name='flight-detail'),
    path('api/flights/cheapest/', views.get_cheapest_flights, name='get-cheapest-flights'),
    
    # Flight search endpoints
    path('searches/', views.FlightSearchListCreateView.as_view(), name='search-list-create'),
    path('searches/<int:pk>/', views.FlightSearchDetailView.as_view(), name='search-detail'),
    path('api/search/ryanair/', views.search_ryanair_flights, name='search-ryanair-flights'),
]
