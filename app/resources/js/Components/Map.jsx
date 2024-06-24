import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import 'leaflet/dist/leaflet.css';

export default function Map() {
    const [data, setData] = useState([]);

    useEffect(() => {
        const data = [
            {
                id: 1,
                name: "Paris",
                latitude: 48.8566,
                longitude: 2.3522,
                average_cost: 1200,
                criminality_rate: 0.6,
                good_schools_rate: 0.8,
                hospitals_count: 10,
                best_cities_index: 0.9,
                population: 1000000,
                density: 20000,
            },
            {
                id: 2,
                name: "Marseille",
                latitude: 43.2965,
                longitude: 5.3698,
                average_cost: 800,
                criminality_rate: 0.8,
                good_schools_rate: 0.6,
                hospitals_count: 5,
                best_cities_index: 0.7,
                population: 500000,
                density: 10000,
            },
            {
                id: 3,
                name: "Lyon",
                latitude: 45.75,
                longitude: 4.85,
                average_cost: 1000,
                criminality_rate: 0.7,
                good_schools_rate: 0.7,
                hospitals_count: 8,
                best_cities_index: 0.8,
                population: 700000,
                density: 15000,
            },
            {
                id: 4,
                name: "Toulouse",
                latitude: 43.6045,
                longitude: 1.4442,
                average_cost: 700,
                criminality_rate: 0.5,
                good_schools_rate: 0.9,
                hospitals_count: 6,
                best_cities_index: 0.8,
                population: 400000,
                density: 8000,
            },
            {
                id: 5,
                name: "Nice",
                latitude: 43.7102,
                longitude: 7.262,
                average_cost: 900,
                criminality_rate: 0.6,
                good_schools_rate: 0.7,
                hospitals_count: 4,
                best_cities_index: 0.7,
                population: 300000,
                density: 6000,
            },
        ];
        setData(data);
    }, []);

    return (
        <MapContainer
            center={[48.8566, 2.3522]}
            zoom={6}
            style={{ height: "100vh", width: "100%" }}
        >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {data.map((city) => (
                <Marker
                    key={city.id}
                    position={[city.latitude, city.longitude]}
                >
                    <Popup>
                        <div>
                            <h3>{city.name}</h3>
                            <p>Average Cost: {city.average_cost}</p>
                            <p>Criminality Rate: {city.criminality_rate}</p>
                            <p>Good Schools: {city.good_schools_rate}</p>
                            <p>Hospitals: {city.hospitals_count}</p>
                            <p>Best Cities Index: {city.best_cities_index}</p>
                            <p>Population: {city.population}</p>
                            <p>Density: {city.density}</p>
                        </div>
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
}
