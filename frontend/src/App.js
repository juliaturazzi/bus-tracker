import './styles/App.css';
import {fetchData} from './api/Api';
import Map from './assets/components/Map';
import Table from './assets/components/Table';
import Input from './assets/components/Input';
import React, {useState, useEffect} from 'react';

function App() {
  const [formData, setFormData] = useState({
    bus_line: '',
    bus_stop: '',
    start_time: '',
    end_time: ''
  });

  const [globalData, setGlobalData] = useState([]);
  const [stops, setStops] = useState([]);
  const [submitted, setSubmitted] = useState(false);
  const [selectedBusStop, setSelectedBusStop] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value,
    }));
    if (name === 'bus_stop') {
      setSelectedBusStop(value); // update selectedBusStop when dropdown changes
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitted(true);
    await getData(); // fetch data on form submit
    setSubmitted(false);
  };

  const handleStopSelected = (stopName) => {
    setFormData(prevState => ({
      ...prevState,
      bus_stop: stopName, // update bus stop name
    }));
  };

  const getData = async () => {
    try {
      const jsonData = await fetchData(formData);
      setGlobalData(jsonData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const fetchStops = async (lat, lon) => {
    setLoading(true); 
    try {
      const response = await fetch(`http://127.0.0.1:8000/stops/?lat=${lat}&lon=${lon}`);
      if (!response.ok) {
        throw new Error("Failed to fetch stops");
      }
      const data = await response.json();
      setStops(data); // save bus stops data
    } catch (error) {
      console.error("Error fetching stops:", error);
    } finally {
      setLoading(false); 
    }
  };

  useEffect(() => {
    if (stops.length === 0) {
      fetchStops('-22.9399', '-43.3437');
    }
  }, [stops]);

  return (
    <div className='outer-container'>
      <p
        className='title'
        style={{
          fontSize: '100px',
          textAlign: 'center',
          marginTop: '50px',
          color: 'white',
          fontWeight: 'bold',
          textShadow: '3px 3px 2px rgba(0, 0, 0, 0.8), -1px -1px 1px rgba(0, 0, 0, 0.5)',
          fontFamily: 'Nexa'
        }}
      >
        Bus Tracker
      </p>
      <div className='main-container'>
        <div className='map-container'>
          {loading ? (<div>
            <div className='loading-spinner'></div>
            <p style={{fontFamily: 'SF Pro, sans-serif'}}>Loading map data...</p>
          </div>) : (
            <Map
              formData={formData}
              submitted={submitted}
              onStopSelected={handleStopSelected}
              selectedBusStop={selectedBusStop}
              allStops={stops}
              busData={globalData} // bus data to map
            />
          )}
        </div>
        <div className='input-container'>
          <Input
            formData={formData}
            handleChange={handleChange}
            handleSubmit={handleSubmit}
            stops={stops} // bus stops for the input component
          />
        </div>
      </div>
      <div className='table-container'>
        <p style={{alignContent: 'center', textAlign: 'center', fontSize: '25px', fontFamily: 'Nexa', fontWeight: 'bold'}}>Bus line: {formData.bus_line}</p>  
        <Table data={globalData} // bus data to table 
        />
      </div>
    </div >
  );
}

export default App;
