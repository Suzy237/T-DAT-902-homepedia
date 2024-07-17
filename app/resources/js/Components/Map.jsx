import React, { useState, useEffect, forwardRef } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
import CityDetails from "./CityDetails";

const MapComponent = ({ data, mode, selected, setSelected }) => {
    const mapRef = React.useRef();

    useEffect(() => {
        if (selected) {
            const { latitude, longitude } = mode === "department"
                ? data.find(location => location.code_departement === selected.code_departement) || {}
                : data.find(location => location.code_postal === selected.code_postal) || {};
            if (latitude && longitude) {
                mapRef.current?.flyTo([latitude, longitude], 13);
            } else {
                console.error("Invalid selected location coordinates:", selected);
            }
        }
    }, [selected, data, mode]);

    const handleMarkerClick = async (location) => {
        if (mode === "city") {
            try {
                const response = await axios.get(`/location/${location.code_postal}`);
                const locationData = { ...response.data, postalCode: location.code_postal };

                try {
                    const cityResponse = await axios.get(`/city/${location.code_postal}`);
                    if (Object.keys(cityResponse.data).length > 0) {
                        locationData.cityData = cityResponse.data;
                    }
                } catch (error) {
                    console.error("Error fetching city details:", error);
                }

                if (locationData.latitude && locationData.longitude) {
                    locationData.latitude = +locationData.latitude;
                    locationData.longitude = +locationData.longitude;
                    setSelected(locationData);
                } else {
                    console.error("Invalid marker click coordinates:", locationData);
                }
            } catch (error) {
                console.error("Error fetching location details:", error);
            }
        } else {
            setSelected(location);
        }
    };

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(value);
    };

    const formatSafetyRate = (rate) => {
        const parsedRate = parseFloat(rate);
        if (isNaN(parsedRate)) return "N/A";
        if (parsedRate < 2) return <span style={{ color: "green" }}>Safe</span>;
        if (parsedRate < 5) return <span style={{ color: "orange" }}>Moderate</span>;
        return <span style={{ color: "red" }}>Dangerous</span>;
    };

    return (
        <>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {data.map((location, i) => (
                location.latitude && location.longitude ? (
                    <Marker
                        key={i}
                        position={[+location.latitude, +location.longitude]}
                        eventHandlers={{
                            click: () => handleMarkerClick(location),
                        }}
                    >
                        <Popup>
                            <div>
                                <h3 className="font-bold">
                                    {mode === "department"
                                        ? location.dep_name
                                        : location.nom_commune_postal}
                                </h3>
                                {selected && (
                                    <div>
                                        <p>
                                            <span className="font-bold">Average property cost: </span>
                                            {formatCurrency(selected.average_cost)}
                                        </p>
                                        <p>
                                            <span className="font-bold">Safety rate: </span>
                                            {formatSafetyRate(+selected.safety_rate)}
                                        </p>
                                        <p>
                                            <span className="font-bold">School count: </span>
                                            {selected.school_count}
                                        </p>
                                        {mode === "city" && selected.cityData ? (
                                            <CityDetails cityData={selected.cityData} />
                                        ) : (
                                            <p>No additional city data available.</p>
                                        )}
                                    </div>
                                )}
                            </div>
                        </Popup>
                    </Marker>
                ) : null
            ))}
        </>
    );
};

const Map = forwardRef(({ data, mode, selectedLocation }, ref) => {
    const [selected, setSelected] = useState(null);

    useEffect(() => {
        if (selectedLocation) {
            setSelected(selectedLocation);
        }
    }, [selectedLocation]);

    return (
        <MapContainer
            center={[46.603354, 1.888334]}
            zoom={6}
            style={{ height: "100vh", width: "100%" }}
            ref={ref}
        >
            <MapComponent
                data={data}
                mode={mode}
                selected={selected}
                setSelected={setSelected}
            />
        </MapContainer>
    );
});

export default Map;
