import Navbar from "@/Components/Navbar";
import { Link, Head } from "@inertiajs/react";
import Map from "@/Components/Map";
import React, { useState, useEffect } from "react";

export default function Index({ auth }) {
    const [mode, setMode] = useState("department");
    const [data, setData] = useState([]);

    useEffect(() => {
        const cityData = [
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

        const departmentData = [
            {
                id: 1,
                name: "Île-de-France",
                latitude: 48.8566,
                longitude: 2.3522,
                average_cost: 1300,
                criminality_rate: 0.5,
                good_schools_rate: 0.9,
                hospitals_count: 15,
                best_cities_index: 0.9,
                population: 12000000,
                density: 1000,
            },
            {
                id: 2,
                name: "Provence-Alpes-Côte d'Azur",
                latitude: 43.9351,
                longitude: 6.0679,
                average_cost: 900,
                criminality_rate: 0.7,
                good_schools_rate: 0.7,
                hospitals_count: 8,
                best_cities_index: 0.8,
                population: 5000000,
                density: 200,
            },
            {
                id: 3,
                name: "Auvergne-Rhône-Alpes",
                latitude: 45.5646,
                longitude: 5.922,
                average_cost: 950,
                criminality_rate: 0.6,
                good_schools_rate: 0.8,
                hospitals_count: 10,
                best_cities_index: 0.85,
                population: 8000000,
                density: 150,
            },
        ];

        setData(mode === "city" ? cityData : departmentData);
    }, [mode]);

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
                                        // src="https://images.unsplash.com/photo-1521560013-60a162a182ab"
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
                                                className={`px-4 py-2 text-black rounded ${mode === "city" ? "bg-blue-500" : "bg-gray-200"}`}
                                                onClick={() => setMode("city")}
                                            >
                                                City
                                            </button>
                                            <button
                                                className={`px-4 py-2 text-black rounded ${mode === "department" ? "bg-blue-500" : "bg-gray-200"}`}
                                                onClick={() => setMode("department")}
                                            >
                                                Department
                                            </button>
                                        </div>
                                        <label htmlFor="city" className="block text-lg font-semibold">
                                            {`Which ${mode === "city" ? "city" : "department"} are you looking for?`}
                                        </label>
                                        <input
                                            type="text"
                                            id="city"
                                            name="city"
                                            placeholder={`Enter a ${mode === "city" ? "city" : "department"} name`}
                                            className="w-full px-4 py-2 mt-2 text-lg border border-gray-300 rounded-md focus:ring-[#FF2D20] focus:border-[#FF2D20] dark:bg-black dark:border-gray-700 dark:focus:ring-white dark:focus:border-white"
                                        />

                                        <button
                                            type="button"
                                            className="w-full px-4 py-2 mt-4 text-lg text-white bg-[#FF2D20] rounded-md focus:outline-none focus-visible:ring-[#FF2D20] dark:bg-white dark:text-black dark:focus-visible:ring-white"
                                        >
                                            Search
                                        </button>
                                        <div className="mt-8 w-full">
                                            <Map data={data} />
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
