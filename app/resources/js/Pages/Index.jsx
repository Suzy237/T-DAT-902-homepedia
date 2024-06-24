import Navbar from "@/Components/Navbar";
import { Link, Head } from "@inertiajs/react";
import Map from "@/Components/Map";

export default function Welcome({ auth }) {
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
                            ) : <div className="min-h-screen flex flex-wrap">
                                <div className="w-full md:w-1/2 mx-auto">
                                    <label htmlFor="city" className="block text-lg font-semibold">
                                        Which city are you looking for?
                                    </label>
                                    <input
                                        type="text"
                                        id="city"
                                        name="city"
                                        placeholder="Enter a city name"
                                        className="w-full px-4 py-2 mt-2 text-lg border border-gray-300 rounded-md focus:ring-[#FF2D20] focus:border-[#FF2D20] dark:bg-black dark:border-gray-700 dark:focus:ring-white dark:focus:border-white"
                                    />

                                    <button
                                        type="button"
                                        className="w-full px-4 py-2 mt-4 text-lg text-white bg-[#FF2D20] rounded-md focus:outline-none focus-visible:ring-[#FF2D20] dark:bg-white dark:text-black dark:focus-visible:ring-white"
                                    >
                                        Search
                                    </button>
                                    <div className="mt-8 w-full">
                                        <Map />
                                    </div>
                                </div>
                            </div>
                            }
                        </main>
                    </div>
                </div>
            </div>
        </>
    );
}
