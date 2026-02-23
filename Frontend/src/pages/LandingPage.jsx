import React, { useEffect, useRef, useState } from "react"
import gsap from "gsap"
import slider1 from '../Images/landingPage-slider/slider1.jpeg';
import slider2 from '../Images/landingPage-slider/slider2.jpg';
import slider3 from '../Images/landingPage-slider/slider3.jpg';
import { Link } from "react-router-dom";


function LandingPage() {
    const intervalRef = useRef(null)

    const [utcTime, setUtcTime] = useState("")

    //time
    useEffect(() => {
        const interval = setInterval(() => {
            const now = new Date()

            const sriLankaTime = now.toLocaleTimeString("en-GB", {
                timeZone: "Asia/Colombo",
                hour12: false,
            })

            setUtcTime(sriLankaTime)
        }, 1000)

        return () => clearInterval(interval)
    }, [])

    //image slider
    useEffect(() => {
        const slides = gsap.utils.toArray(".slide")

        // Initial state
        slides.forEach((slide, i) => {
            gsap.set(slide, {
                opacity: i === 0 ? 1 : 0,
                scale: 1
            })
        })

        let current = 0

        intervalRef.current = setInterval(() => {
            const next = (current + 1) % slides.length

            // Fade out current
            gsap.to(slides[current], {
                opacity: 0,
                scale: 1.1,
                duration: 2,
                ease: "power2.inOut"
            })

            // Fade in next
            gsap.fromTo(
                slides[next],
                { opacity: 0, scale: 1 },
                {
                    opacity: 1,
                    scale: 1.05,
                    duration: 2,
                    ease: "power2.inOut"
                }
            )

            current = next
        }, 5000)

        return () => clearInterval(intervalRef.current)
    }, [])

    return (
        <section className="relative h-screen overflow-hidden">

            {/* Background Slides */}
            <div className="absolute inset-0">
                <img src={slider1} className="slide absolute inset-0 w-full h-full object-cover" />
                <img src={slider2} className="slide absolute inset-0 w-full h-full object-cover" />
                <img src={slider3} className="slide absolute inset-0 w-full h-full object-cover" />
            </div>

            <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/60 to-black/40" />

            <div className="relative z-10 h-full flex items-center lg:text-left text-center lg:px-20 ">
                {/* Hero Content */}
                <div className="text-white w-full lg:max-w-2xl px-6 lg:px-0">

                    <h1 className="
                        text-4xl 
                        sm:text-5xl 
                        md:text-6xl 
                        lg:text-7xl 
                        font-bold 
                        leading-[1.1] 
                        tracking-tight
                        
                    ">
                        Drone <span className="text-purple-500">Image</span> <br className="hidden sm:block" />
                        Upload Platform
                    </h1>

                    <div className="sm:items-start items-center gap-4 mt-8">

                        <Link to="/signin">
                            <button className="
                                w-fit
                                px-6 py-3 
                                bg-amber-400 text-black 
                                font-semibold 
                                rounded-lg 
                                transition-all duration-300 
                                hover:bg-amber-300 
                                hover:scale-105 
                                shadow-lg hover:shadow-amber-400/40
                            ">
                                Sign In →
                            </button>
                        </Link>

                    </div>
                </div>
                {/* glass card */}
                <div className="absolute hidden lg:block right-16 bottom-10 
                        backdrop-blur-xl bg-white/5 
                        border border-white/10 
                        rounded-2xl p-6 w-80 text-white shadow-2xl">

                    <p className="text-sm text-gray-400 mb-4 tracking-wide">
                        System Environment
                    </p>

                    <div className="space-y-4 text-sm">

                        <div className="flex justify-between items-center">
                            <span className="text-gray-300">Environment</span>
                            <span className="font-medium text-green-400">Production</span>
                        </div>

                        <div className="flex justify-between items-center">
                            <span className="text-gray-300">Time</span>
                            <span className="font-mono tracking-wide">{utcTime}</span>
                        </div>

                        <div className="flex justify-between items-center">
                            <span className="text-gray-300">Secure Network</span>
                            <span className="flex items-center gap-2 text-green-400">
                                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                                Connected
                            </span>
                        </div>

                    </div>

                </div>
            </div>

        </section>
    )
}

export default LandingPage