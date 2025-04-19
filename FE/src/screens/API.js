import React, { useState } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function ApiAnalysis() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);

    const handleQuestionChange = (event) => {
        setQuestion(event.target.value);
    };

    const handleSubmit = async () => {
        setLoading(true);
        setAnswer('');

        try {
            const response = await fetch('http://localhost:5000/members', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("API Response:", data);
            if (typeof data === 'object' && data !== null) {
                setAnswer(JSON.stringify(data, null, 2));
            } else if (typeof data === 'string') {
                setAnswer(data);
            } else {
                setAnswer(String(data));
            }
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
                            Input:
                        </label>
                        <textarea
                            id="question"
                            className="border rounded p-2 w-full"
                            placeholder="Enter your question"
                            value={question}
                            onChange={handleQuestionChange}
                        />
                    </div>

                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                        disabled={loading}
                    >
                        {loading ? 'Analyzing...' : 'Ask'}
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
                                <pre className="font-mono text-sm">
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