import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';
import { format, addDays, parseISO } from 'date-fns';
import './FlightSearchForm.css';

function FlightSearchForm({ onSearchResults, onLoading }) {
  const [airports, setAirports] = useState([]);
  const [selectedOrigin, setSelectedOrigin] = useState(null);
  const [selectedDestination, setSelectedDestination] = useState(null);
  const [searchForm, setSearchForm] = useState({
    origin_iata: '',
    destination_iata: '',
    departure_date_from: '',
    departure_date_to: '',
    return_date_from: '',
    return_date_to: '',
    passengers: 1,
  });
  const [isRoundTrip, setIsRoundTrip] = useState(false);

  useEffect(() => {
    loadAirports();
  }, []);

  const loadAirports = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/airports/');
      setAirports(response.data);
    } catch (error) {
      console.error('Error loading airports:', error);
    }
  };

  const handleOriginChange = (selectedOption) => {
    setSelectedOrigin(selectedOption);
    setSearchForm(prev => ({
      ...prev,
      origin_iata: selectedOption ? selectedOption.iata_code : '',
    }));
  };

  const handleDestinationChange = (selectedOption) => {
    setSelectedDestination(selectedOption);
    setSearchForm(prev => ({
      ...prev,
      destination_iata: selectedOption ? selectedOption.iata_code : '',
    }));
  };

  const getAirportOptions = () => {
    const allDestinationsOption = { value: '', label: 'All Destinations', iata_code: '' };
    const airportOptions = airports.map(airport => ({
      value: airport.id.toString(),
      label: `${airport.iata_code} - ${airport.name}, ${airport.city}, ${airport.country}`,
      iata_code: airport.iata_code,
    }));
    return [allDestinationsOption, ...airportOptions];
  };

  const handlePassengersChange = (e) => {
    const value = parseInt(e.target.value);
    setSearchForm(prev => ({
      ...prev,
      passengers: value,
    }));
  };

  const handleDateChange = (field, value) => {
    setSearchForm(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleRoundTripToggle = () => {
    setIsRoundTrip(!isRoundTrip);
    if (!isRoundTrip) {
      const today = format(new Date(), 'yyyy-MM-dd');
      const tomorrow = format(addDays(new Date(), 1), 'yyyy-MM-dd');
      setSearchForm(prev => ({
        ...prev,
        return_date_from: tomorrow,
        return_date_to: tomorrow,
      }));
    } else {
      setSearchForm(prev => ({
        ...prev,
        return_date_from: '',
        return_date_to: '',
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    onLoading(true);
    
    try {
      const response = await axios.post('http://localhost:8000/api/search/ryanair/', searchForm);
      onSearchResults(response.data);
    } catch (error) {
      console.error('Error searching flights:', error);
    } finally {
      onLoading(false);
    }
  };

  const today = format(new Date(), 'yyyy-MM-dd');
  const maxDate = format(new Date(new Date().setFullYear(new Date().getFullYear() + 1)), 'yyyy-MM-dd');

  return (
    <div className="flight-search-form">
      <h2>Search Cheapest Ryanair Flights</h2>
      
      <form onSubmit={handleSubmit} className="search-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="origin_iata">From:</label>
            <Select
              id="origin_iata"
              value={selectedOrigin}
              onChange={handleOriginChange}
              options={getAirportOptions().filter(option => option.iata_code !== '')}
              placeholder="Search and select origin airport..."
              isSearchable
              isClearable
              classNamePrefix="react-select"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="destination_iata">To:</label>
            <Select
              id="destination_iata"
              value={selectedDestination}
              onChange={handleDestinationChange}
              options={getAirportOptions()}
              placeholder="Search and select destination airport..."
              isSearchable
              isClearable
              classNamePrefix="react-select"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="departure_date_from">Departure Date From:</label>
            <input
              type="date"
              id="departure_date_from"
              value={searchForm.departure_date_from}
              onChange={(e) => handleDateChange('departure_date_from', e.target.value)}
              min={today}
              max={maxDate}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="departure_date_to">Departure Date To:</label>
            <input
              type="date"
              id="departure_date_to"
              value={searchForm.departure_date_to}
              onChange={(e) => handleDateChange('departure_date_to', e.target.value)}
              min={searchForm.departure_date_from}
              max={maxDate}
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="passengers">Passengers:</label>
            <input
              type="number"
              id="passengers"
              value={searchForm.passengers}
              onChange={handlePassengersChange}
              min="1"
              max="9"
              required
            />
          </div>

          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={isRoundTrip}
                onChange={handleRoundTripToggle}
              />
              Round Trip
            </label>
          </div>
        </div>

        {isRoundTrip && (
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="return_date_from">Return Date From:</label>
              <input
                type="date"
                id="return_date_from"
                value={searchForm.return_date_from}
                onChange={(e) => handleDateChange('return_date_from', e.target.value)}
                min={searchForm.departure_date_to}
                max={maxDate}
              />
            </div>

            <div className="form-group">
              <label htmlFor="return_date_to">Return Date To:</label>
              <input
                type="date"
                id="return_date_to"
                value={searchForm.return_date_to}
                onChange={(e) => handleDateChange('return_date_to', e.target.value)}
                min={searchForm.return_date_from}
                max={maxDate}
              />
            </div>
          </div>
        )}

        <button type="submit" className="search-button">
          Search Flights
        </button>
      </form>
    </div>
  );
}

export default FlightSearchForm;
