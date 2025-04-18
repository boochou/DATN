import React from "react";
import logo from "../img/logo.png";

export default function Footer() {
    return (
        <footer className="bg-ft text-white rounded-lg shadow">
            <div className="w-full max-w-screen-xl mx-auto p-4 md:py-8">
                <div className="sm:flex sm:items-center sm:justify-between">
                    <a href="/" className="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse">
                        <img src={logo} className="h-16" alt="ACK Logo" />
                        <span className="self-center text-2xl font-semibold whitespace-nowrap">ACK™</span>
                    </a>
                    <ul className="flex flex-wrap items-center mb-6 text-sm font-medium text-white sm:mb-0">
                        <li>
                            <a href="/" className="hover:underline me-4 md:me-6">About</a>
                        </li>
                        <li>
                            <a href="/" className="hover:underline me-4 md:me-6">Privacy Policy</a>
                        </li>
                        <li>
                            <a href="/" className="hover:underline me-4 md:me-6">Licensing</a>
                        </li>
                        <li>
                            <a href="/" className="hover:underline">Contact Me</a>
                        </li>
                    </ul>
                </div>
                <hr className="my-6 border-white sm:mx-auto lg:my-8" />
                <span className="block text-sm text-gray-300 sm:text-center">© 2025 — <a href="/" className="hover:underline">ACK™</a></span>
            </div>
        </footer>
    );
}
