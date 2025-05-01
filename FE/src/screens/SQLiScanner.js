import React, { useState, useRef, useEffect } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";
import axios from 'axios';

export default function SQLiScanner() {
    const [domainOrFile, setDomainOrFile] = useState('');
    const fileInputRef = useRef(null);

    const [scanResults, setScanResults] = useState([]);

    const [fullExploit, setFullExploit] = useState(false);
    const [findInjection, setFindInjection] = useState(false);
    const [getDbName, setGetDbName] = useState(false);
    const [getDbTable, setGetDbTable] = useState(false);
    const [getDbSchema, setGetDbSchema] = useState(false);


    useEffect(() => {
        if (findInjection && getDbName && getDbTable && getDbSchema) {
            setFullExploit(true);
        } else {
            setFullExploit(false);
        }
    }, [findInjection, getDbName, getDbTable, getDbSchema]);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setDomainOrFile(file);
    };

    const handleDomainChange = (event) => {
        setDomainOrFile(event.target.value);
    };


    const handleFullExploitToggle = () => {
        const newState = !fullExploit;
        setFullExploit(newState);
        setFindInjection(newState);
        setGetDbName(newState);
        setGetDbTable(newState);
        setGetDbSchema(newState);
    };

    const handleSubmit = async () => {
        let options = []
        if (fullExploit){
            options = ['-b', '--tables', '--schema']
        }
        else{
            if (getDbName) options.push('-b');
            if (getDbTable) options.push('--tables');
            if (getDbSchema) options.push('--schema');
        }
        const optionString = options.join(' ');
        try {
            const formData = new FormData();
    
            if (typeof domainOrFile === 'string') {
                formData.append('url', domainOrFile);
            } else {
                formData.append('file', domainOrFile);
            }
    
            formData.append('options', optionString);
    
            const response = await axios.post('http://localhost:5000/api/sqli-scan', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
    
            const result = response.data;
            console.log("Scan result:", result);
            setScanResults(result.result || result);
    
            return new Promise((resolve) => {
                setTimeout(() => {
                    resolve(result);
                }, 1000);
            });
        } catch (error) {
            console.error("Error scanning SQLi:", error);
        }
        // try {
        //     //check if domainOrFile is file or string
        //     // if domainOrFile is string, let url = domainOrFile
        //     // else: let file = domainOrFile
        //     // send axios POST request to http://localhost:5000/api/sqli-scan with data options, url, file
        //     // then hanlde response
    
        //     if (!response.ok) {
        //         throw new Error(`HTTP error! status: ${response.status}`);
        //     }
    
        //     const result = await response.json();
        //     console.log("Scan result:", result);
        //     setScanResults(result.result || result);
        //     return new Promise((resolve, reject) => {
        //         setTimeout(() => {
        //                 resolve(result);
        //         }, 1000); 
        //     });
        // } catch (error) {
        //     console.error("Error scanning SQLi:", error);
        // }
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
                <h1 className="text-3xl font-bold text-white mb-4">SQL Injection Scanner</h1>

                <div className="bg-white p-16 rounded-lg shadow-md">
                    <div className="mb-4">
                        <label htmlFor="domainOrFile" className="block text-gray-700 font-semibold mb-2">
                            Target for scanning:
                        </label>
                        <div className="flex">
                            <input
                                type="text"
                                id="domainOrFile"
                                className="border rounded-l-md p-2 flex-grow"
                                placeholder="Enter domain or select file that contain request"
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
                        <label className="block text-gray-700 font-semibold mb-2">Scan Options:</label>

                        <div className="flex items-center mb-2">
                            <input
                                type="checkbox"
                                id="fullExploit"
                                className="mr-2"
                                checked={fullExploit}
                                onChange={handleFullExploitToggle}
                            />
                            <label htmlFor="fullExploit">Full Exploit</label>
                        </div>

                        {/* <div className="flex items-center mb-2">
                            <input
                                type="checkbox"
                                id="findInjection"
                                className="mr-2"
                                checked={findInjection}
                                onChange={() => setFindInjection(!findInjection)}
                            />
                            <label htmlFor="findInjection">Find Injection Vulnerability</label>
                        </div> */}

                        <div className="flex items-center mb-2">
                            <input
                                type="checkbox"
                                id="getDbName"
                                className="mr-2"
                                checked={getDbName}
                                onChange={() => setGetDbName(!getDbName)}
                            />
                            <label htmlFor="getDbName">Retrieve Database Name</label>
                        </div>

                        <div className="flex items-center mb-2">
                            <input
                                type="checkbox"
                                id="getDbTable"
                                className="mr-2"
                                checked={getDbTable}
                                onChange={() => setGetDbTable(!getDbTable)}
                            />
                            <label htmlFor="getDbTable">Retrieve Database Table</label>
                        </div>

                        <div className="flex items-center mb-2">
                            <input
                                type="checkbox"
                                id="getDbSchema"
                                className="mr-2"
                                checked={getDbSchema}
                                onChange={() => setGetDbSchema(!getDbSchema)}
                            />
                            <label htmlFor="getDbSchema">Retrieve Database Schema</label>
                        </div>
                    </div>

                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                    >
                        Start Scan
                    </button>

                    {scanResults && (
                        <div className="mt-4">
                            <h2 className="text-lg font-semibold mb-2">Scan Result:</h2>
                            <div className="overflow-auto max-h-60 bg-gray-100 rounded p-4">
                                <pre className="font-mono text-sm whitespace-pre-wrap break-words">
                                    {scanResults}
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