import Navbar from "@/Components/Navbar";
import { Link, Head } from "@inertiajs/react";
import Map from "@/Components/Map";
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function Index({ auth, departments, cities }) {
    const [mode, setMode] = useState("department");
    const [data, setData] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedLocation, setSelectedLocation] = useState(null);
    const [searchResults, setSearchResults] = useState([]);
    const mapRef = useRef();

    useEffect(() => {
        setData(mode === "city" ? cities : departments);
    }, [mode, cities, departments]);

    const handleSearch = (event) => {
        event.preventDefault();
        if (searchTerm === "") {
            handleClear();
        } else {
            if (mode === "city") {
                const results = cities.filter((city) =>
                    city.name.toLowerCase().includes(searchTerm.toLowerCase())
                );
                if (results.length > 0) {
                    setSearchResults(results);
                    setSelectedLocation(results[0]);
                    mapRef.current?.flyTo(
                        [results[0].latitude, results[0].longitude],
                        13
                    );
                } else {
                    console.log("No results found");
                }
            } else {
                const results = departments.filter((dept) =>
                    dept.dep_name
                        .toLowerCase()
                        .includes(searchTerm.toLowerCase())
                );
                if (results.length > 0) {
                    setSearchResults(results);
                    setSelectedLocation(results[0]);
                    mapRef.current?.flyTo(
                        [results[0].latitude, results[0].longitude],
                        13
                    );
                } else {
                    console.log("No results found");
                }
            }
        }
    };

    const handleClear = () => {
        setSearchTerm("");
        setSelectedLocation(null);
        setSearchResults([]);
        mapRef.current?.setView([46.603354, 1.888334], 6); // Center of France
    };

    const handleLocationSelect = (event) => {
        const locationName = event.target.value;
        setSearchTerm(locationName);
    };

    return (
        <>
            <Head title="Home" />
            <div className="min-h-screen bg-gradient-to-r from-gray-900 to-gray-800 text-gray-100 flex flex-col items-center justify-center">
                <Navbar auth={auth} />
                <div className="w-full max-w-4xl p-6 bg-white rounded-lg shadow-md dark:bg-gray-800">
                    <main className="space-y-6">
                        {!auth.user ? (
                            <div className="text-center">
                                <img
                                    src="https://img-9gag-fun.9cache.com/photo/a1oy6XR_460s.jpg"
                                    alt="Home"
                                    className="w-64 mx-auto object-cover rounded-full shadow-lg"
                                />
                                <h1 className="mt-8 text-4xl font-bold text-gray-900 dark:text-gray-100">
                                    Welcome to Homepedia!
                                </h1>
                                <p className="mt-4 text-lg text-gray-700 dark:text-gray-300">
                                    Find your dream home with ease. Sign up to
                                    get started.
                                </p>
                                <div className="mt-8">
                                    <Link
                                        href={route("register")}
                                        className="px-6 py-3 text-lg font-semibold text-white bg-red-600 rounded-lg shadow-md hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
                                    >
                                        Register now
                                    </Link>
                                </div>
                            </div>
                        ) : (
                            <div className="space-y-6">
                                <div className="flex justify-center space-x-4">
                                    <button
                                        className={`px-6 py-3 rounded-lg font-semibold text-lg ${
                                            mode === "city"
                                                ? "bg-blue-600 text-white"
                                                : "bg-gray-200 text-gray-900"
                                        } hover:bg-blue-500 transition-colors duration-200`}
                                        onClick={() => setMode("city")}
                                    >
                                        City
                                    </button>
                                    <button
                                        className={`px-6 py-3 rounded-lg font-semibold text-lg ${
                                            mode === "department"
                                                ? "bg-blue-600 text-white"
                                                : "bg-gray-200 text-gray-900"
                                        } hover:bg-blue-500 transition-colors duration-200`}
                                        onClick={() => setMode("department")}
                                    >
                                        Department
                                    </button>
                                </div>
                                <form
                                    onSubmit={handleSearch}
                                    className="space-y-4"
                                >
                                    <div>
                                        <label
                                            htmlFor="location"
                                            className="block text-xl font-semibold text-gray-900 dark:text-gray-100"
                                        >
                                            {`Which ${
                                                mode === "city"
                                                    ? "city"
                                                    : "department"
                                            } are you looking for?`}
                                        </label>
                                        <div className="relative mt-2">
                                            <input
                                                type="text"
                                                id="location"
                                                name="location"
                                                value={searchTerm}
                                                onChange={(e) =>
                                                    setSearchTerm(
                                                        e.target.value
                                                    )
                                                }
                                                placeholder={`Enter a ${
                                                    mode === "city"
                                                        ? "city"
                                                        : "department"
                                                } name`}
                                                className="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-600 focus:border-transparent dark:bg-gray-700 dark:text-gray-100 dark:focus:ring-white"
                                            />
                                            <div className="absolute right-0 top-0 h-full flex items-center pr-2">
                                                <button
                                                    type="button"
                                                    className="px-4 py-2 text-sm bg-gray-300 rounded-lg shadow hover:bg-gray-200 transition-colors duration-200"
                                                    onClick={handleClear}
                                                >
                                                    Clear
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex justify-center space-x-4">
                                        <button
                                            type="submit"
                                            className="px-6 py-3 text-lg font-semibold text-white bg-red-600 rounded-lg shadow-md hover:bg-red-500 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-opacity-50"
                                        >
                                            Search
                                        </button>
                                    </div>
                                </form>
                                <div className="flex justify-center mt-4">
                                    <select
                                        className="px-4 py-3 text-lg border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-700 dark:text-gray-100"
                                        onChange={handleLocationSelect}
                                    >
                                        <option value="">
                                            {`Select a ${
                                                mode === "city"
                                                    ? "city"
                                                    : "department"
                                            }`}
                                        </option>
                                        {(mode === "city"
                                            ? cities
                                            : departments
                                        ).map((item) => (
                                            <option
                                                key={
                                                    mode === "city"
                                                        ? item.id
                                                        : item.dep_code
                                                }
                                                value={
                                                    mode === "city"
                                                        ? item.name
                                                        : item.dep_name
                                                }
                                            >
                                                {mode === "city"
                                                    ? item.name
                                                    : item.dep_name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div className="mt-8 w-full h-96 rounded-lg overflow-hidden">
                                    <Map
                                        ref={mapRef}
                                        data={data}
                                        mode={mode}
                                        selectedLocation={selectedLocation}
                                    />
                                </div>
                            </div>
                        )}
                    </main>
                </div>
            </div>
        </>
    );
}
