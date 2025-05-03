import React, { useState } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function ApiAnalysis() {
    const [file, setFile] = useState(null);
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!file) {
            alert('Please select a file first!');
            return;
        }

        setLoading(true);
        setAnswer('');

        const formData = new FormData();
        formData.append('apisFile', file);

        try {
            const response = await fetch('http://localhost:5000/api/api-analysis/create-api-relationship', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("API Response:", data);
            if (data.status === 200){
                if (typeof data.raw_response === 'object' && data.raw_response !== null) {
                    setAnswer(JSON.stringify(data.raw_response, null, 2));
                } else if (typeof data.raw_response === 'string') {
                    setAnswer(data.raw_response);
                } else {
                    setAnswer(data.raw_response);
                }
            }
            else{
                setAnswer(data.error);
            }

            
            // console.log("API Response:", data);
            // setAnswer(data.raw_response);
            // if (typeof data === 'object' && data !== null) {
            //     setAnswer(JSON.stringify(data, null, 2));
            // } else if (typeof data === 'string') {
            //     setAnswer(data);
            // } else {
            //     setAnswer(String(data));
            // }
        } catch (error) {
            console.error('Error fetching data:', error);
            setAnswer(`Error fetching data: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-center min-h-screen" style={{ backgroundImage: `url(${background})` }}>
            <Header />

            <div className="relative items-center justify-center min-h-screen text-gray-900 container mx-auto p-24">
                <h1 className="text-3xl font-bold text-white mb-4">API Analysis</h1>

                <div className="bg-white p-16 rounded-lg shadow-md">
                    <div className="mb-4">
                        <label htmlFor="question" className="block text-gray-700 font-semibold mb-2">
                            Upload APIs file for analysis:
                        </label>
                        <input
                            id="fileUpload"
                            type="file"
                            className="border rounded p-2 w-full"
                            onChange={handleFileChange}
                        />
                    </div>
                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                        disabled={loading}
                    >
                        {loading ? 'Analyzing...' : 'Analyze'}
                    </button>

                    {loading && (
                        <div className="mt-4">
                            <h2 className="text-lg font-semibold mb-2">Analyzing...</h2>
                            <p>Please wait while the API is being analyzed.</p>
                        </div>
                    )}

                    {answer && (
                        <div className="mt-4">
                            <h2 className="text-lg font-semibold mb-2">Answer:</h2>
                            <div className="overflow-auto max-h-60 bg-gray-100 rounded p-4">
                                <pre className="font-mono text-sm whitespace-pre-wrap break-words">
                                    {answer}
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