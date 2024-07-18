import React from "react";

const LocationDetail = ({ location, onClose }) => {
    if (!location) return null;

    const { name, address, description, imageUrl, zillowLink } = location;

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center">
            <div className="relative p-8 bg-white shadow-lg rounded-lg max-w-lg w-full">
                <button
                    onClick={onClose}
                    className="absolute top-0 right-0 m-4 p-2 bg-gray-200 rounded-full hover:bg-gray-300"
                >
                    <svg
                        className="w-6 h-6 text-gray-600"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M6 18L18 6M6 6l12 12"
                        />
                    </svg>
                </button>
                <h2 className="text-xl font-semibold mb-4">{name}</h2>
                <img
                    src={imageUrl}
                    alt={name}
                    className="w-full rounded-lg mb-4"
                />
                <p className="text-gray-600 mb-2">{address}</p>
                <p className="text-gray-600 mb-4">{description}</p>
                <a
                    href={zillowLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline"
                >
                    View on Homepedia
                </a>
            </div>
        </div>
    );
};

export default LocationDetail;
