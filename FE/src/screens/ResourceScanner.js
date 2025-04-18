import React, { useState, useRef } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function ResourceScanner() {
    const [domain, setDomain] = useState('');
    const [wordlistFile, setWordlistFile] = useState(null);
    const fileInputRef = useRef(null);
    const [scanResults, setScanResults] = useState([]);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setWordlistFile(file);
    };

    const handleDomainChange = (event) => {
        setDomain(event.target.value);
    };

    const handleSubmit = () => {
        console.log('Domain:', domain);
        console.log('Wordlist File:', wordlistFile);
        scanResources(domain, wordlistFile)
            .then(results => {
                setScanResults(results);
            })
            .catch(error => {
                console.error('Error scanning resources:', error);
                setScanResults(['Error scanning resources.']);
            });
    };

    const scanResources = async (domain, wordlist) => {

        return new Promise((resolve, reject) => {
            setTimeout(() => {
                const fakeResults = [`${domain}/resource1`, `${domain}/resource2`, `${domain}/resource3`];
                resolve(fakeResults);
            }, 1000); 
        });
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
                                id="domainOrFile"
                                className="border rounded-l-md p-2 flex-grow"
                                placeholder="Select dict file"
                            />
                            <button
                                type="button"
                                className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-r-md"
                                onClick={() => fileInputRef.current.click()}
                            >
                                Select Wordlist File
                            </button>
                            <input
                                type="file"
                                ref={fileInputRef}
                                style={{ display: 'none' }}
                                onChange={handleFileChange}
                            />
                        </div>
                    </div>

                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                    >
                        Start Scan
                    </button>

                    {scanResults.length > 0 && (
                        <div className="mt-4">
                            <h2 className="text-lg font-semibold mb-2">Scan Results:</h2>
                            <ul>
                                {scanResults.map((result, index) => (
                                    <li key={index}>{result}</li>
                                ))}
                            </ul>
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