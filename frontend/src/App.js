import React from 'react';
import axios from 'axios';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Cheap Flights Finder</h1>
        <p>Find the cheapest Ryanair flights for your travel dates</p>
      </header>
      <main>
        <FlightSearchForm />
        <FlightResults />
      </main>
    </div>
  );
}

export default App;
