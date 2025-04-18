
import { StarIcon } from '@heroicons/react/20/solid'
import Header from "../assets/component/Header"
import Footer from "../assets/component/Footer"
import React, { useState,useRef} from 'react';

import background from "../assets/img/bg.jpg";

export default function HomePage() {
  return (
    <div
      className="bg-center min-h-screen"
      style={{ backgroundImage: `url(${background})` }}
    >
      <Header />

      <div className="relative flex flex-col items-center justify-center min-h-screen text-white text-center px-6">
        <h1 className="text-4xl font-bold md:text-5xl">ACK Tool</h1>
        <p className="mt-4 text-lg font-bold md:text-xl max-w-2xl">
          A powerful reconnaissance tool that helps you gather information quickly and efficiently.
        </p>
        
        <a 
          href="/dashboard"
          className="mt-6 px-6 py-3 bg-gray-500 hover:bg-gray-700 rounded-lg text-white text-lg font-semibold transition duration-300"
        >
          Get Started
        </a>

        
      </div>
      
      <div className="bottom">
          <Footer />
      </div>
    </div>
  );
}
