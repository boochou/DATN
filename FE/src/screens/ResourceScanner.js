import React, { useState, useRef } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function ResourceScanner() {
    const [domain, setDomain] = useState('');
    const [wordlistFile, setWordlistFile] = useState(null);
    const fileInputRef = useRef(null);
    const [scanResults, setScanResults] = useState([]);
    const [isScanning, setIsScanning] = useState(false); 

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setWordlistFile(file);
    };

    const handleDomainChange = (event) => {
        setDomain(event.target.value);
    };

    const handleSubmit = async () => {
        setIsScanning(true); 
        setScanResults([]);

        console.log('Domain:', domain);
        console.log('Wordlist File:', wordlistFile);
        try {
            const wordlistName = wordlistFile?.name || "";
            const inputValue = domain;

            const response = await fetch(
                `http://localhost:5000/collectUrls?input=${encodeURIComponent(inputValue)}&wordlist=${encodeURIComponent(wordlistName)}`
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
            console.error("Error fetching resources:", error);
            setScanResults([`Error fetching resources: ${error.message}`]);
        } finally {
            setIsScanning(false); 
        }
    };

    return (
        <div className="bg-center min-h-screen" style={{ backgroundImage: `url(${background})` }}>
            <Header />

            <div className="relative items-center justify-center min-h-screen text-gray-900 container mx-auto p-24">
                <h1 className="text-3xl font-bold text-white mb-4">Resource Scanner</h1>

                <div className="bg-white p-16 rounded-lg shadow-md">
                    <div className="mb-4">
                        <label htmlFor="domain" className="block text-gray-700 font-semibold mb-2">
                            Domain:
                        </label>
                        <input
                            type="text"
                            id="domain"
                            className="border rounded p-2 w-full"
                            placeholder="Enter domain"
                            value={domain}
                            onChange={handleDomainChange}
                        />
                    </div>

                    <div className="mb-4">
                        <label className="block text-gray-700 font-semibold mb-2">
                            Option:
                        </label>
                        <div className="flex">
                            <input
                                type="text"
                                id="wordlistFileText"
                                className="border rounded-l-md p-2 flex-grow"
                                placeholder={wordlistFile?.name || "Select dict file"}
                                readOnly
                            />
                            <button
                                type="button"
                                className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-r-md"
                                onClick={() => fileInputRef.current.click()}
                                disabled={isScanning}
                            >
                                Select Wordlist File
                            </button>
                            <input
                                type="file"
                                ref={fileInputRef}
                                style={{ display: 'none' }}
                                onChange={handleFileChange}
                                disabled={isScanning}
                            />
                        </div>
                    </div>

                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                        disabled={isScanning}
                    >
                        {isScanning ? 'Scanning...' : 'Start Scan'}
                    </button>

                    {isScanning && (
                        <div className="mt-4">
                            <h2 className="text-lg font-semibold mb-2">Scanning...</h2>
                            <p>Please wait while resources are being scanned.</p>
                        </div>
                    )}

                    {!isScanning && scanResults.length > 0 && (
                        <div className="mt-4">
                            <h2 className="text-lg font-semibold mb-2">Scan Results:</h2>
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