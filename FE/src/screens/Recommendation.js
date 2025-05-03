import React, { useState, useRef, useEffect } from 'react';
import Header from "../assets/component/Header";
import Footer from "../assets/component/Footer";
import background from "../assets/img/background.jpg";

export default function Recommendation() {
    const [messages, setMessages] = useState([]);
    const [currentInput, setCurrentInput] = useState('');
    const [loading, setLoading] = useState(false);

    const messagesContainerRef = useRef(null); // Ref for the messages container
    const textareaRef = useRef(null);

    // Scroll to the latest bot message
    useEffect(() => {
        // Only scroll when the last message is from the bot
        if (messages[messages.length - 1]?.sender === 'bot' && messagesContainerRef.current) {
            messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
        }
    }, [messages]); // This effect triggers whenever messages change

    const handleInputChange = (event) => {
        setCurrentInput(event.target.value);
    };

    const handleSubmit = async () => {
        if (!currentInput.trim()) return;
        textareaRef.current.style.height = "auto"; // Reset textarea height before new message
        const userMessage = { sender: 'user', text: currentInput };
        setMessages((prev) => [...prev, userMessage]);
        setCurrentInput('');
        setLoading(true);

        // Reset textarea height after submitting
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'; 
        }

        try {
            const response = await fetch('http://localhost:5000/api/recommend-tools', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: userMessage.text }),
            });

            const data = await response.json();

            const serverMessage = {
                sender: 'bot',
                text: data.status === 200
                    ? (typeof data.data === 'object' ? JSON.stringify(data.data, null, 2) : data.data)
                    : data.error || 'Unknown error from server',
            };

            setMessages((prev) => [...prev, serverMessage]);
        } catch (error) {
            setMessages((prev) => [...prev, { sender: 'bot', text: `Error: ${error.message}` }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-center min-h-screen" style={{ backgroundImage: `url(${background})` }}>
            <Header />

            <div className="relative min-h-screen text-gray-900 container mx-auto p-24">
                <h1 className="text-3xl font-bold text-white mb-4">Tool Recommendation</h1>
                
                <div 
                    className="bg-white p-8 rounded-lg shadow-md max-h-[70vh] overflow-y-auto"
                    ref={messagesContainerRef} // Ref for the messages container
                >
                    {messages.map((msg, index) => (
                        <div key={index} className={`mb-4 flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`p-3 rounded-lg w-2/3 break-words ${msg.sender === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-100 text-left'}`}>
                                <div className="font-semibold">{msg.sender === 'user' ? 'You' : 'Bot'}</div>
                                <pre className="whitespace-pre-wrap">{msg.text}</pre>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-4 flex gap-2">
                    <textarea
                        ref={textareaRef}
                        className="border rounded p-2 w-full resize-none"
                        placeholder="Type your question here..."
                        value={currentInput}
                        onChange={handleInputChange}
                        rows={1}
                        onInput={(e) => {
                            e.target.style.height = 'auto';
                            e.target.style.height = Math.min(e.target.scrollHeight, 144) + 'px'; // 6 * 24px
                        }}
                    />
                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={handleSubmit}
                        disabled={loading}
                    >
                        {loading ? 'Sending...' : 'Send'}
                    </button>
                </div>
            </div>

            <Footer />
        </div>
    );
}
