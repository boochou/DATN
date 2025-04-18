import React, { useState, useRef } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function ConfigPage() {
    const [limitRate, setLimitRate] = useState('');
    const [dictFile, setDictFile] = useState(null);
    const fileInputRef = useRef(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setDictFile(file);
    };

    const handleLimitRateChange = (event) => {
        setLimitRate(event.target.value);
    };

    const handleSubmit = () => {
        console.log('Limit Rate:', limitRate);
        console.log('Dict File:', dictFile);
    };

    return (
        <div className="bg-center min-h-screen" style={{ backgroundImage: `url(${background})` }}>
            <Header />

            <div className="relative items-center justify-center min-h-screen text-gray-900 container mx-auto p-24">
                <h1 className="text-3xl font-bold text-white mb-4">Config</h1>

                <div className="bg-white p-16 rounded-lg shadow-md">
                    <div className="mb-4">
                        <label htmlFor="limitRate" className="block text-gray-700 font-semibold mb-2">
                            Limit Rate:
                        </label>
                        <input
                            type="number"
                            id="limitRate"
                            className="border rounded p-2 w-full"
                            placeholder="Enter limit rate"
                            value={limitRate}
                            onChange={handleLimitRateChange}
                        />
                    </div>

                    <div className="mb-4">
                        <label className="block text-gray-700 font-semibold mb-2">
                        Dict File:
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

                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                    >
                        Save Config
                    </button>
                </div>
            </div>

            <div className="bottom">
                <Footer />
            </div>
        </div>
    );
}