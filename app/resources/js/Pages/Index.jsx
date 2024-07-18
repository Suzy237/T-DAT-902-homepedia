import Navbar from "@/Components/Navbar";
import { Link, Head } from "@inertiajs/react";
import Map from "@/Components/Map";
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function Index({ auth, departments, cities, sampleCities }) {
    const [mode, setMode] = useState("department");
    const [data, setData] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedLocation, setSelectedLocation] = useState(null);
    const [currentResultIndex, setCurrentResultIndex] = useState(0);
    const [searchResults, setSearchResults] = useState([]);
    const mapRef = useRef();

    useEffect(() => {
        if (searchTerm === "") {
            let citySlice = cities.filter((e, i) => sampleCities.includes(e.code_postal) && i % 5 === 0);
            setData(mode === "city" ? citySlice : departments);
        }
    }, [mode, cities, departments, searchTerm]);

    const handleSearch = (event) => {
        event.preventDefault();
        if (searchTerm === "") {
            handleClear();
        } else {
            if (mode === "city") {
                axios
                    .get(`/cities/${searchTerm.replace(/['-]/g, " ")}`)
                    .then((response) => {
                        if (response.data && response.data.length > 0) {
                            setSearchResults(response.data);
                            cycleSearchResults(response.data);
                        } else {
                            console.log("No results found");
                        }
                    })
                    .catch((error) => {
                        console.error("Error fetching cities:", error);
                    });
            } else {
                const results = departments.filter((dept) =>
                    dept.dep_name
                        .toLowerCase()
                        .includes(searchTerm.toLowerCase())
                );
                if (results.length > 0) {
                    setSearchResults(results);
                    cycleSearchResults(results);
                } else {
                    console.log("No results found");
                }
            }
        }
    };

    const cycleSearchResults = (results) => {
        const newIndex = (currentResultIndex + 1) % results.length;
        setCurrentResultIndex(newIndex);
        const currentResult = results[newIndex];
        setSelectedLocation(currentResult);
        setData(results);
        const coordinates =
            mode === "city"
                ? [currentResult.latitude, currentResult.longitude]
                : [currentResult.latitude, currentResult.longitude];
        mapRef.current?.flyTo(coordinates, 13);
    };

    const handleClear = () => {
        setSearchTerm("");
        setSelectedLocation(null);
        setSearchResults([]);
        let citySlice = cities.filter((e, i) => sampleCities.includes(e.code_postal) && i % 5 === 0);
        setData(mode === "city" ? citySlice : departments);
        mapRef.current?.setView([46.603354, 1.888334], 6); // Center of France
    };

    const handleLocationSelect = (event) => {
        const locationName = event.target.value;
        setSearchTerm(locationName);
    };

    return (
        <>
            <Head title="Home" />
            <div className="relative min-h-screen flex flex-col items-center justify-center bg-black text-white">
                <div className="relative z-10 w-full max-w-2xl px-6 lg:max-w-7xl"></div>
                <div className="relative z-10 w-full max-w-2xl px-6 lg:max-w-7xl">
                    <Navbar auth={auth} />
                    <main className="mt-6 pb-12">
                        {!auth.user ? (
                            <div className="text-center">
                                <div className="mt-8">
                                    <Link
                                        href={route("register")}
                                        className="rounded-md px-6 py-3 text-white bg-[#FF2D20] ring-1 ring-[#FF2D20] transition hover:bg-transparent hover:text-[#FF2D20] focus:outline-none focus-visible:ring-[#FF2D20] dark:text-black dark:bg-white dark:hover:text-white dark:hover:bg-transparent dark:focus-visible:ring-white"
                                    >
                                        Register now
                                    </Link>
                                </div>
                            </div>
                        ) : (
                            <div className="min-h-screen flex flex-wrap">
                                <div className="w-full md:w-1/2 mx-auto flex flex-wrap">
                                    <div className="flex space-x-2 mb-4 mx-auto w-full justify-center">
                                        <button
                                            className={`px-4 py-2 text-black rounded ${
                                                mode === "city"
                                                    ? "bg-blue-500"
                                                    : "bg-gray-200"
                                            }`}
                                            onClick={() => setMode("city")}
                                        >
                                            City
                                        </button>
                                        <button
                                            className={`px-4 py-2 text-black rounded ${
                                                mode === "department"
                                                    ? "bg-blue-500"
                                                    : "bg-gray-200"
                                            }`}
                                            onClick={() =>
                                                setMode("department")
                                            }
                                        >
                                            Department
                                        </button>
                                    </div>
                                    <form
                                        onSubmit={handleSearch}
                                        className="w-full"
                                        style={{
                                            backgroundColor:
                                                "rgba(255, 255, 255, 0.8)",
                                            padding: "20px",
                                            borderRadius: "10px",
                                        }}
                                    >
                                        <label
                                            htmlFor="city"
                                            className="block text-lg font-semibold"
                                        >
                                            {`Which ${
                                                mode === "city"
                                                    ? "city"
                                                    : "department"
                                            } are you looking for?`}
                                        </label>
                                        <input
                                            type="text"
                                            id="city"
                                            name="city"
                                            value={searchTerm}
                                            onChange={(e) =>
                                                setSearchTerm(e.target.value)
                                            }
                                            placeholder={`Enter a ${
                                                mode === "city"
                                                    ? "city"
                                                    : "department"
                                            } name`}
                                            className="w-full px-4 py-2 mt-2 text-lg border border-gray-300 rounded-md focus:ring-[#FF2D20] focus:border-[#FF2D20] dark:bg-black dark:border-gray-700 dark:focus:ring-white dark:focus:border-white"
                                        />
                                        <div className="flex space-x-2 mt-4">
                                            <button
                                                type="submit"
                                                className="flex-1 px-4 py-2 text-lg text-white bg-[#FF2D20] rounded-md focus:outline-none focus-visible:ring-[#FF2D20] dark:bg-white dark:text-black dark:focus-visible:ring-white"
                                            >
                                                Search
                                            </button>
                                            <button
                                                type="button"
                                                onClick={handleClear}
                                                className="flex-1 px-4 py-2 text-lg text-white bg-gray-400 rounded-md focus:outline-none focus-visible:ring-gray-400 dark:bg-gray-600 dark:text-black dark:focus-visible:ring-gray-600"
                                            >
                                                Clear
                                            </button>
                                        </div>
                                    </form>
                                    {mode === "department" && (
                                        <div className="mt-4 w-full">
                                            <select
                                                className="w-full px-4 py-2 mt-2 text-lg border border-gray-300 rounded-md focus:ring-[#FF2D20] focus:border-[#FF2D20] dark:bg-black dark:border-gray-700 dark:focus:ring-white dark:focus:border-white"
                                                onChange={handleLocationSelect}
                                            >
                                                <option value="">
                                                    Select a department
                                                </option>
                                                {departments.map(
                                                    (department) => (
                                                        <option
                                                            key={
                                                                department.dep_code
                                                            }
                                                            value={
                                                                department.dep_name
                                                            }
                                                        >
                                                            {
                                                                department.dep_name
                                                            }
                                                        </option>
                                                    )
                                                )}
                                            </select>
                                        </div>
                                    )}
                                    <div className="mt-8 w-full">
                                        <Map
                                            ref={mapRef}
                                            data={data}
                                            mode={mode}
                                            selectedLocation={selectedLocation}
                                        />
                                    </div>
                                </div>
                            </div>
                        )}
                    </main>
                </div>
            </div>
        </>
    );
}
