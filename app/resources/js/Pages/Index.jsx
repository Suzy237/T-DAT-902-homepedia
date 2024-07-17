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
    const [currentResultIndex, setCurrentResultIndex] = useState(0);
    const [searchResults, setSearchResults] = useState([]);
    const mapRef = useRef();

    useEffect(() => {
        if (searchTerm === "") {
            const citySlice = cities.filter((e, i) => i % 500 === 0);
            setData(mode === "city" ? citySlice : departments);
        }
    }, [mode, cities, departments, searchTerm]);

    const handleSearch = (event) => {
        event.preventDefault();
        if (searchTerm === "") {
            handleClear();
        } else {
            if (mode === "city") {
                axios.get(`/cities/${searchTerm.replace(/['-]/g, " ")}`)
                    .then(response => {
                        if (response.data && response.data.length > 0) {
                            setSearchResults(response.data);
                            cycleSearchResults(response.data);
                        } else {
                            console.log("No results found");
                        }
                    })
                    .catch(error => {
                        console.error("Error fetching cities:", error);
                    });
            } else {
                const results = departments.filter(dept => dept.dep_name.toLowerCase().includes(searchTerm.toLowerCase()));
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
        const coordinates = mode === "city"
            ? [currentResult.latitude, currentResult.longitude]
            : [currentResult.latitude, currentResult.longitude];
        mapRef.current?.flyTo(coordinates, 13);
    };

    const handleClear = () => {
        console.log({ departments, cities })
        setSearchTerm("");
        setSelectedLocation(null);
        setSearchResults([]);
        const citySlice = cities.filter((e, i) => i % 500 === 0);
        setData(mode === "city" ? citySlice : departments);
        mapRef.current?.setView([46.603354, 1.888334], 6); // Center of France
    };

    return (
        <>
            <Head title="Home" />
            <div className="bg-gray-50 text-black/50 dark:bg-black dark:text-white/50">
                <div className="relative min-h-screen flex flex-col items-center justify-center selection:bg-[#FF2D20] selection:text-white">
                    <div className="relative w-full max-w-2xl px-6 lg:max-w-7xl">
                        <Navbar auth={auth} />
                        <main className="mt-6 pb-12">
                            {!auth.user ? (
                                <div className="text-center">
                                    <img
                                        src="https://img-9gag-fun.9cache.com/photo/a1oy6XR_460s.jpg"
                                        alt="Home"
                                        className="w-64 mx-auto object-cover rounded-lg"
                                    />
                                    <h1 className="mt-8 text-3xl font-bold">
                                        Welcome!
                                    </h1>
                                    <p className="mt-4 text-lg">
                                        Homepedia is a platform to help you find
                                        your dream home. Sign up to get started.
                                    </p>
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
                                                className={`px-4 py-2 text-black rounded ${mode === "city"
                                                    ? "bg-blue-500"
                                                    : "bg-gray-200"
                                                    }`}
                                                onClick={() => setMode("city")}
                                            >
                                                City
                                            </button>
                                            <button
                                                className={`px-4 py-2 text-black rounded ${mode === "department"
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
                                        >
                                            <label
                                                htmlFor="city"
                                                className="block text-lg font-semibold"
                                            >
                                                {`Which ${mode === "city"
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
                                                    setSearchTerm(
                                                        e.target.value
                                                    )
                                                }
                                                placeholder={`Enter a ${mode === "city"
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
                                        <div className="mt-8 w-full">
                                            <Map
                                                ref={mapRef}
                                                data={data}
                                                mode={mode}
                                                selectedLocation={
                                                    selectedLocation
                                                }
                                            />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </main>
                    </div>
                </div>
            </div>
        </>
    );
}
