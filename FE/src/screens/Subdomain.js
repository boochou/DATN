import React, { useState, useRef, useEffect } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function SubdomainScanner() {
    // const [test, setTest] = useState([{}]);
    // useEffect(() => {
    //     fetch("/members")
    //     .then(res => res.json())
    //     .then(data => {
    //         setTest(data);
    //         console.log(test, data)
    //     });
    // }, []);
    const [domainOrFile, setDomainOrFile] = useState('');
    const [activeScan, setActiveScan] = useState(false);
    const [wordlistFile, setWordlistFile] = useState(null);
    const fileInputRef = useRef(null);
    const wordlistInputRef = useRef(null);
    const [scanResults, setScanResults] = useState([]);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setDomainOrFile(file);
    };

    const handleDomainChange = (event) => {
        setDomainOrFile(event.target.value);
    };

    const handleWordlistFileChange = (event) => {
        const file = event.target.files[0];
        setWordlistFile(file);
    };

    const handleSubmit = async () => {
        console.log('Domain/File:', domainOrFile);
        console.log('Active Scan:', activeScan);
        console.log('Wordlist File:', wordlistFile);
    
        try {
            const wordlistName = wordlistFile?.name || "";
            const inputValue = typeof domainOrFile === 'string' ? domainOrFile : domainOrFile.name;
    
            const response = await fetch(
                `/subdomains?input=${encodeURIComponent(inputValue)}&isactive=${activeScan}&wordlist=${encodeURIComponent(wordlistName)}`
            );
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            const result = await response.json();
            console.log("Scan result:", result);
            setScanResults(result.result || result); // Adjust depending on your Flask return structure
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                        resolve(result);
                }, 1000); 
            });
        } catch (error) {
            console.error("Error fetching subdomains:", error);
        }
    };
    

    const fetchSubdomains = async (input, active, wordlist) => {
        console.log("Input: ",input)
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (typeof input === 'string') {
                    const fakeResults = [`sub1.${input}`, `sub2.${input}`, `sub3.${input}`];
                    resolve(fakeResults);
                } else {
                    resolve(['File processing not implemented in this example']);
                }
            }, 1000); 
        });
    };

    return (
        <div className="bg-center min-h-screen" style={{ backgroundImage: `url(${background})` }}>
            <Header />
            <div className="relative items-center justify-center min-h-screen text-gray-900 container mx-auto p-24">
                <h1 className="text-3xl font-bold text-white mb-4">Subdomain Scanner</h1>

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
                                id="activeScan"
                                className="mr-2"
                                checked={activeScan}
                                onChange={() => setActiveScan(!activeScan)}
                            />
                            <label htmlFor="activeScan">Active Scan</label>
                        </div>
                        <div className="flex items-center">
                            <button
                                type="button"
                                className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
                                onClick={() => wordlistInputRef.current.click()}
                            >
                                Select Wordlist File
                            </button>
                             <input
                                type="file"
                                ref={wordlistInputRef}
                                style={{ display: 'none' }}
                                onChange={handleWordlistFileChange}
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
                            <h2 className="text-lg font-semibold mb-2">Output:</h2>
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