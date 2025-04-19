import React, { useState, useRef } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function Tech() {
    const [domainOrFile, setDomainOrFile] = useState('');
    const [scanOS, setScanOS] = useState(false);
    const [detectFirewall, setDetectFirewall] = useState(false);
    const fileInputRef = useRef(null);
    const [scanResults, setScanResults] = useState([]);
    const [isScanning, setIsScanning] = useState(false); // State to track scanning

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setDomainOrFile(file);
    };

    const handleDomainChange = (event) => {
        setDomainOrFile(event.target.value);
    };

    const handleSubmit = async () => {
        setIsScanning(true); // Set scanning state to true
        setScanResults([]); // Clear previous results

        console.log('Domain/File:', domainOrFile);
        console.log('Scan OS:', scanOS);
        console.log('Detect Firewall:', detectFirewall);
        try {
            const inputValue = typeof domainOrFile === 'string' ? domainOrFile : domainOrFile.name;

            const response = await fetch(
                `http://localhost:5000/scanTech?input=${encodeURIComponent(inputValue)}&firewall=${detectFirewall}&scanOS=${encodeURIComponent(scanOS)}`
            );

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log("Scan result:", result);

            if (Array.isArray(result)) {
                setScanResults(result);
            } else if (typeof result === 'object' && result !== null) {
                setScanResults([JSON.stringify(result, null, 2)]);
            } else {
                setScanResults([String(result)]);
            }

        } catch (error) {
            console.error("Error fetching technology stack:", error);
            setScanResults([`Error fetching technology stack: ${error.message}`]);
        } finally {
            setIsScanning(false); // Set scanning state to false after completion or error
        }
    };

    return (
        <div className="bg-center min-h-screen" style={{ backgroundImage: `url(${background})` }}>
            <Header />

            <div className="relative items-center justify-center min-h-screen text-gray-900 container mx-auto p-24">
                <h1 className="text-3xl font-bold text-white mb-4">Technology Stack Detection</h1>

                <div className="bg-white p-16 rounded-lg shadow-md">
                    <div className="mb-4">
                        <label htmlFor="domainOrFile" className="block text-gray-700 font-semibold mb-2">
                            Domain or File:
                        </label>
                        <div className="flex">
                            <input
                                type="text"
                                id="domainOrFile"
                                className="border rounded-l-md p-2 flex-grow"
                                placeholder="Enter domain or select file"
                                value={domainOrFile}
                                onChange={handleDomainChange}
                            />
                            <button
                                type="button"
                                className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-r-md"
                                onClick={() => fileInputRef.current.click()}
                            >
                                Select File
                            </button>
                            <input
                                type="file"
                                ref={fileInputRef}
                                style={{ display: 'none' }}
                                onChange={handleFileChange}
                            />
                        </div>
                    </div>

                    <div className="mb-4">
                        <label className="block text-gray-700 font-semibold mb-2">Options:</label>
                        <div className="flex items-center mb-2">
                            <input
                                type="checkbox"
                                id="scanOS"
                                className="mr-2"
                                checked={scanOS}
                                onChange={() => setScanOS(!scanOS)}
                            />
                            <label htmlFor="scanOS">Scan Possible OS (Root Privileged)</label>
                        </div>
                        <div className="flex items-center">
                            <input
                                type="checkbox"
                                id="detectFirewall"
                                className="mr-2"
                                checked={detectFirewall}
                                onChange={() => setDetectFirewall(!detectFirewall)}
                            />
                            <label htmlFor="detectFirewall">Detect Firewall</label>
                        </div>
                    </div>

                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                        disabled={isScanning} // Disable button while scanning
                    >
                        {isScanning ? 'Detecting...' : 'Start Detection'}
                    </button>

                    {isScanning && (
                        <div className="mt-4">
                            <h2 className="text-lg font-semibold mb-2">Detecting...</h2>
                            <p>Please wait while technology stack is being detected.</p>
                            {/* You can add a visual indicator here like a spinner */}
                        </div>
                    )}

                    {!isScanning && scanResults.length > 0 && (
                        <div className="mt-4">
                            <h2 className="text-lg font-semibold mb-2">Output:</h2>
                            <div className="overflow-auto max-h-60 bg-gray-100 rounded p-4">
                                <pre className="font-mono text-sm">
                                    {scanResults.map((result, index) => (
                                        <div key={index}>{result}</div>
                                    ))}
                                </pre>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            <div className="bottom">
                <Footer />
            </div>
        </div>
    );
}