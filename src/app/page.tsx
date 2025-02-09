'use client'
import Link from 'next/link'
import React from 'react'
import { useState } from 'react'
import axios from "axios"


export default function HomePage() {
  const [userText, setUserText] = useState("");
  const [companies, setCompanies] = useState([]);
  const [showtop5, setShowtop5] = useState(false);



  const handleSubmit = async (event: React.FormEvent) => {
      event.preventDefault();
      try {
          const response = await axios.post("http://localhost:8000/submit", 
              { user_text: userText },
              {
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  withCredentials: false
              }
          );
          console.log("Response:", response);
          if (response.data && Array.isArray(response.data.companies)) {
            setCompanies(response.data.companies);
            setShowtop5(true);
          } else {
            console.error("Unexpected response structure:", response.data);
            setCompanies([]); // Reset companies to an empty array
            setShowtop5(false);
          }
      } catch (error) {
          console.error("Error sending data:", error);
      }
  };



  const CardComponents = () => (
      <div className="flex flex-col w-full h-full justify-start items-start">
        <div className="w-3/4 h-auto bg-gray-500 justify-center items-center p-4 mb-4 rounded-3xl">
            <h1 className="text-white text-2xl">{companies[0]}</h1>
            <h1 className="text-white text-lg">{companies[1]}</h1>
            <h1 className="text-white text-1xl">{companies[2]}</h1>
        </div>
        <div className="w-3/4 h-auto bg-gray-500 justify-center items-center p-4 mb-4 rounded-3xl">
            <h1 className="text-white text-2xl">{companies[3]}</h1>
            <h1 className="text-white text-lg">{companies[4]}</h1>
            <h1 className="text-white text-1xl">{companies[5]}</h1>
        </div>
        <div className="w-3/4 h-auto bg-gray-500 justify-center items-center p-4 mb-4 rounded-3xl">
            <h1 className="text-white text-2xl">{companies[6]}</h1>
            <h1 className="text-white text-lg">{companies[7]}</h1>
            <h1 className="text-white text-1xl">{companies[8]}</h1>
        </div>
        <div className="w-3/4 h-auto bg-gray-500 justify-center items-center p-4 mb-4 rounded-3xl">
            <h1 className="text-white text-2xl">{companies[9]}</h1>
            <h1 className="text-white text-lg">{companies[10]}</h1>
            <h1 className="text-white text-1xl">{companies[11]}</h1>
        </div>
        <div className="w-3/4 h-auto bg-gray-500 justify-center items-center p-4 mb-4 rounded-3xl">
            <h1 className="text-white text-2xl">{companies[12]}</h1>
            <h1 className="text-white text-lg">{companies[13]}</h1>
            <h1 className="text-white text-1xl">{companies[14]}</h1>
        </div>
      </div>
  );




  return (
    <div className="flex flex-col bg-slate-200 w-full h-screen">
      <div className="relative w-full h-3/5 mt-0.5">
        <img src="/logos.jpg" className="object-cover w-full h-full"></img>
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-black bg-opacity-70">
          <h1 className="text-white text-7xl">
            <span className="font-bold">Find Your Next Unicorn Startup</span>
          </h1>
          <h1 className="text-white text-5xl mt-12 font-bold">Search by Product Idea, Vision, or Industry</h1>
          <button className="bg-orange-500 rounded-lg w-44 h-14 mt-20 hover:border hover:border-white">
            <Link href="#target-section" className="text-white text-2xl font-bold">
              Search Now
            </Link>
          </button>
        </div>

        <div id="target-section" className="w-screen h-1 bg-slate-300"></div>

        <div className="bg-gradient-to-b from-orange-400 via-rose-400 to-orange-500 flex flex-col w-screen h-screen justify-start items-center">
          <div className="flex flex-col bg-slate-100 w-3/4 h-screen mt-28 justify-start space-x-40 rounded-3xl shadow-2xl">
            <div className="flex w-full h-24">
              <input
                placeholder="Enter an idea..."
                onChange={(event) => setUserText(event.target.value)}
                className="block w-11/12 h-full text-black bg-gray-300 rounded-3xl text-3xl p-12 placeholder-gray-500 focus:placeholder-gray-600"
              />
              <button onClick={handleSubmit} className="w-1/12 h-full rounded-3xl bg-orange-500 text-4xl p-5 border-2 border-black hover:border-4">
                🔍
              </button>
            </div>

            <div className="mt-10 w-full h-full">
              {showtop5 && companies.length > 0 && CardComponents()}
            </div>

          </div>

          <div className="w-screen h-3 bg-slate-300 mt-36"></div>

          <div className="flex w-screen h-1/2 p-8 bg-gradient-to-b from-rose-400 to-purple-400 justify-end">
            <div className="flex flex-col mr-40 justify-start items-right w-1/2 space-y-1">
              <h1 className="text-white font-bold text-3xl text-right">Columbia DevFest 2025 Project</h1>
              <h1 className="text-white text-2xl text-right">Arm Komolhiran</h1>
              <h1 className="text-white text-2xl text-right">Amrutha Rao</h1>
              <h1 className="text-white text-2xl text-right">David Xiong</h1>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}