import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";

export default function Map({ data, mode }) {
    console.log({ data });
    const [selectedLocation, setSelectedLocation] = useState(null);

    const handleMarkerClick = async (locationId) => {
        try {
            const response = await axios.get(`/location/${locationId}`);
            setSelectedLocation(response.data);
        } catch (error) {
            console.error("Error fetching location details:", error);
        }
    };

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
                    position={[+location.latitude, +location.longitude]}
                    eventHandlers={{
                        click: () => handleMarkerClick(location.code_postal),
                    }}
                >
                    <Popup>
                        <div>
                            <h3 className="font-bold">
                                {mode === "department"
                                    ? location.dep_name
                                    : location.nom_commune_postal}
                            </h3>
                            {selectedLocation && (
                                <div>
                                    <p>
                                        Average Cost:{" "}
                                        {selectedLocation.average_cost}
                                    </p>
                                    <p>
                                        Criminality Rate:{" "}
                                        {selectedLocation.safety_rate > 0
                                            ? selectedLocation.safety_rate
                                            : "N/A"}
                                    </p>
                                    <p>
                                        School Count:{" "}
                                        {selectedLocation.school_count}
                                    </p>
                                </div>
                            )}
                        </div>
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
}
