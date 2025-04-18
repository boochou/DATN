import React, { useState, useRef } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function DomainChecker() {
    const [domainOrFile, setDomainOrFile] = useState('');
    const [ipOnly, setIpOnly] = useState(false);
    const [scanType, setScanType] = useState('tcp_connect');
    const [portType, setPortType] = useState('common');
    const fileInputRef = useRef(null);
    const [scanResults, setScanResults] = useState([]);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setDomainOrFile(file);
    };

    const handleDomainChange = (event) => {
        setDomainOrFile(event.target.value);
    };

    const handleSubmit = async () =>  {
        console.log('Domain/File:', domainOrFile);
        console.log('IP Only:', ipOnly);
        console.log('Scan Type:', scanType);
        console.log('Port Type:', portType);
        try {
            const all_port = (portType === 'common') ? false : true;
            const inputValue = typeof domainOrFile === 'string' ? domainOrFile : domainOrFile.name;
            console.log("Result: ",inputValue, all_port, ipOnly)
            const response = await fetch(
                `/checkdomains?input=${encodeURIComponent(inputValue)}&ipOnly=${ipOnly}&all_port=${encodeURIComponent(all_port)}`
            );
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            const result = await response.json();
            console.log("Scan result:", result, response);
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

    const checkDomains = async (input, ipOnly, scanType, portType) => {

        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (typeof input === 'string') {
                    const fakeResults = [`${input} - ${scanType} - ${portType} - Active`];
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
                <h1 className="text-3xl font-bold text-white mb-4">Domain Checker</h1>

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
                                id="ipOnly"
                                className="mr-2"
                                checked={ipOnly}
                                onChange={() => setIpOnly(!ipOnly)}
                            />
                            <label htmlFor="ipOnly">IP Only</label>
                        </div>
                        <div className="mb-2">
                            <label htmlFor="scanType" className="block text-gray-700 font-semibold mb-2">Scan Type:</label>
                            <select
                                id="scanType"
                                className="border rounded p-2"
                                value={scanType}
                                onChange={(e) => setScanType(e.target.value)}
                            >
                                <option value="tcp_connect">TCP Connect Scan</option>
                                <option value="tcp_syn">TCP SYN Scan</option>
                                <option value="udp">UDP Scan</option>
                                <option value="null">NULL Scan</option>
                            </select>
                        </div>
                        <div className="mb-2">
                            <label htmlFor="portType" className="block text-gray-700 font-semibold mb-2">Port Type:</label>
                            <select
                                id="portType"
                                className="border rounded p-2"
                                value={portType}
                                onChange={(e) => setPortType(e.target.value)}
                            >
                                <option value="common">Common Ports</option>
                                <option value="all">All Ports</option>
                            </select>
                        </div>
                    </div>

                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                    >
                        Start Check
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