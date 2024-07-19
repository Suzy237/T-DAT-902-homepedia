import React from "react";

export default function CityDetails({ cityData }) {
    const formatCurrency = (value) => {
        return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR" }).format(value);
    };

    const getPoliticalInclination = (percentage) => {
        const parsedPercentage = parseFloat(percentage.replace(',', '.'));
        if (isNaN(parsedPercentage)) return "Unknown";
        return parsedPercentage > 50 ? "Right-leaning" : "Left-leaning";
    };

    return (
        <div className="">
            <h3 className="text-xl font-semibold mt-4">Key Statistics</h3>
            <ul>
                <li>Number of Inhabitants: {cityData.stat_population?.["Nombre d'habitants"] ?? "N/A"}</li>
                <li>Average Age: {cityData.stat_population?.["Age moyen"] ?? "N/A"}</li>
                <li>Unemployment Rate: {cityData.stat_population?.["Taux chômage"] ?? "N/A"}</li>
            </ul>
            <h3 className="text-xl font-semibold mt-4">Real Estate Data</h3>
            <ul>
                <li>Average House Price: {cityData.immobilier?.Maison?.["Prix moyen"] ?? "N/A"}</li>
                <li>Average House Price per m²: {cityData.immobilier?.Maison?.["Prix moyen au m²"] ?? "N/A"}</li>
                <li>Average Apartment Price: {cityData.immobilier?.Appartement?.["Prix moyen"] ?? "N/A"}</li>
                <li>Average Apartment Price per m²: {cityData.immobilier?.Appartement?.["Prix moyen au m²"] ?? "N/A"}</li>
            </ul>
            <h3 className="text-xl font-semibold mt-4">Political Inclination</h3>
            <ul>
                <li>
                    Inclination: {cityData.politique?.tour2?.["Marine LE PEN"] ? getPoliticalInclination(cityData.politique.tour2["Marine LE PEN"]) : "Unknown"}
                </li>
            </ul>
        </div>
    );
}
