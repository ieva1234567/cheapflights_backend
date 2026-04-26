import React from 'react';
import './FlightResults.css';

function FlightResults({ searchResults }) {
  if (!searchResults || !searchResults.outbound_flights) {
    return (
      <div className="flight-results">
        <div className="no-results">
          <h3>No flights found</h3>
          <p>Try adjusting your search criteria or dates.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flight-results">
      <h2>Search Results</h2>
      
      {searchResults.outbound_flights && (
        <div className="results-section">
          <h3>
            {searchResults.search_params.destination_iata 
              ? "Flights from " + searchResults.search_params.origin_iata + " to " + searchResults.search_params.destination_iata
              : "All destinations from " + searchResults.search_params.origin_iata}
          </h3>
          
          <div className="flights-list">
            {searchResults.outbound_flights.map((flight, index) => (
              <div key={index} className="flight-card">
                <div className="flight-header">
                  <h4>
                    {searchResults.search_params.destination_iata 
                      ? flight.destination_name || flight.destination + " - " + (flight.destination_city || 'Unknown')
                      : flight.destination_name || 'All Destinations'}
                  </h4>
                  <div className="flight-details">
                    <p><strong>Flight:</strong> {flight.flight_number}</p>
                    <p><strong>From:</strong> {flight.origin} → <strong>To:</strong> {flight.destination}</p>
                    <p><strong>Departure:</strong> {new Date(flight.departure_time).toLocaleString()}</p>
                    <p><strong>Arrival:</strong> {new Date(flight.arrival_time).toLocaleString()}</p>
                    <p><strong>Price:</strong> €{flight.price}</p>
                    <p><strong>Available Seats:</strong> {flight.available_seats}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {searchResults.return_flights && searchResults.return_flights.length > 0 && (
        <div className="results-section">
          <h3>Return Flights</h3>
          
          <div className="flights-list">
            {searchResults.return_flights.map((flight, index) => (
              <div key={index} className="flight-card">
                <div className="flight-header">
                  <h4>Return Flight</h4>
                  <div className="flight-details">
                    <p><strong>Flight:</strong> {flight.flight_number}</p>
                    <p><strong>From:</strong> {flight.origin} → <strong>To:</strong> {flight.destination}</p>
                    <p><strong>Departure:</strong> {new Date(flight.departure_time).toLocaleString()}</p>
                    <p><strong>Arrival:</strong> {new Date(flight.arrival_time).toLocaleString()}</p>
                    <p><strong>Price:</strong> €{flight.price}</p>
                    <p><strong>Available Seats:</strong> {flight.available_seats}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default FlightResults;
