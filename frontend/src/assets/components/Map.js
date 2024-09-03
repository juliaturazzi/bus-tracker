import L from 'leaflet';
import '../../styles/Map.css';
import 'leaflet/dist/leaflet.css';
import {fetchData} from '../../api/Api';
import React, {useEffect, useState} from 'react';
import MarkerClusterGroup from 'react-leaflet-cluster';
import {MapContainer, TileLayer, Marker, Popup} from 'react-leaflet';

// fix default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// custom icons for stops and buses
const stopIcon = L.icon({
  iconUrl: require('../images/bus-stop-icon.png'),
  iconSize: [22, 22],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const busIcon = L.icon({
  iconUrl: require('../images/bus-icon.png'),
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

// display bus and stop data
const Map = ({formData, submitted, onStopSelected, selectedBusStop, allStops, busData}) => {
  const [coords, setCoords] = useState([]);
  const [stops, setStops] = useState([]);
  const [selectedStop, setSelectedStop] = useState(null);

  const fetchCoordinates = async () => {
    try {
      const data = await fetchData(formData);
      setCoords(data);
    } catch (error) {
      console.error("Error fetching coordinates:", error);
    }
  };

  useEffect(() => {
    if (submitted) {
      fetchCoordinates();
    }
  }, [submitted]);

  useEffect(() => {
    if (!submitted) {
      setCoords([]);
    }
  }, [submitted]);

  useEffect(() => {
    if (selectedBusStop) {
      const stop = stops.find(s => s.stop_name === selectedBusStop);
      if (stop) {
        setSelectedStop(stop);
      }
    }
  }, [selectedBusStop, stops]);

  useEffect(() => {
    if (submitted && selectedStop) {
      setStops([selectedStop]); // selected bus
    }
  }, [submitted, selectedStop]);

  const checkStop = (stop1, stop2) => {
    if (stop1.stop_name === stop2.stop_name) {
      if (stop1.stop_lat === stop2.stop_lat && stop1.stop_lon === stop2.stop_lon) {
        return true;
      }
      return false;
    }
    return false;
  };

  if (selectedStop) {
    allStops = allStops.filter(stop => checkStop(stop, selectedStop));
    console.log(allStops);
  }

  // starting coordinate for the map in the center of Rio
  const centerRioPosition = [-22.9068, -43.1729];

  return (
    <div className='outer-container'>
      <div className="map-container" style={{borderRadius: '10px'}}>
        <MapContainer
          center={busData.length > 0 ? [busData[0].latitude, busData[0].longitude] : centerRioPosition}
          zoom={15}
          style={{width: '100%', height: '100%', borderRadius: '20px'}}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
            {busData.map((bus, index) => (
              <Marker key={`bus-${index}`} position={[bus.latitude, bus.longitude]} icon={busIcon}>
                <Popup>
                  Bus: {bus.ordem}, Speed: {bus.velocidade}
                </Popup>
              </Marker>
            ))}
            <MarkerClusterGroup chunkedLoading>
            {allStops.map((stop, index) => (
              <Marker
                key={`stop-${index}`}
                position={[stop.stop_lat, stop.stop_lon]}
                icon={stopIcon}
                eventHandlers={{click: () => {onStopSelected(stop.stop_name);}}}
              >
                <Popup>
                  Name: {stop.stop_name}
                </Popup>
              </Marker>
            ))}
          </MarkerClusterGroup>
        </MapContainer>
      </div>
    </div>
  );
};

export default Map;
