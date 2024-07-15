import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import 'leaflet/dist/leaflet.css';

export default function Map({ data }) {
    return (
        <MapContainer
            center={[48.8566, 2.3522]}
            zoom={6}
            style={{ height: "100vh", width: "100%" }}
        >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {data.map((location) => (
                <Marker
                    key={location.id}
                    position={[location.latitude, location.longitude]}
                >
                    <Popup>
                        <div>
                            <h3>{location.name}</h3>
                            <p>Average Cost: {location.average_cost}</p>
                            <p>Criminality Rate: {location.criminality_rate}</p>
                            <p>Good Schools: {location.good_schools_rate}</p>
                            <p>Hospitals: {location.hospitals_count}</p>
                            <p>Best Cities Index: {location.best_cities_index}</p>
                            <p>Population: {location.population}</p>
                            <p>Density: {location.density}</p>
                        </div>
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
}
