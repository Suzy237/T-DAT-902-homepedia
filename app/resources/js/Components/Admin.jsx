import { useEffect, useState, useRef } from "react";

export default function Admin() {
    const [logs, setLogs] = useState([]);
    const logContainerRef = useRef(null);

    async function logFetcher() {
        const response = await fetch("/logs");
        const data = await response.json();
        setLogs(data.logs);
    }

    async function fetchCSVs() {
        try {
            fetch("/fetch-csvs");
            logFetcher();
        }
        catch (error) {
            console.error("Error fetching CSV:", error);
        }
    }

    async function processData() {
        try {
            fetch("/process-data");
            logFetcher();
        }
        catch (error) {
            console.error("Error processing data:", error);
        }
    }

    useEffect(() => {
        const interval = setInterval(() => {
            logFetcher();
        }, 20000);

        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (logContainerRef.current) {
            logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <div>
            <div className="flex flex-wrap justify-center">
                <h2 className="text-xl font-semibold mx-auto text-center mb-4 text-white w-full">Admin Panel</h2>
                <button onClick={fetchCSVs}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mx-2">
                    Fetch CSV
                </button>
                <button onClick={processData}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mx-2">
                    Process Data
                </button>
                <button onClick={logFetcher}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mx-2">
                    Update logs
                </button>
            </div>
            <div ref={logContainerRef} className="mt-8 font-mono text-white text-xs h-64 border overflow-y-scroll p-4 bg-black mx-6 rounded-md">
                {logs.map((log, index) => (
                    <div key={index}>{log}</div>
                ))}
            </div>
        </div>
    );
}
