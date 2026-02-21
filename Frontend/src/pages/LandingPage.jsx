import React from 'react'
import DroneScene from '../components/Drone';
import HeroImage from '../Images/hero-bg.avif';

function LandingPage() {
    return (
        <div className='relative w-full min-h-screen'>
            <div className='relative grid grid-cols-1 lg:grid-cols-2 min-h-screen'>
                {/* left col */}
                <div className='flex flex-col justify-center px-5 lg:px-10 '>

                    <div className='flex flex-col justify-center '>
                        <h1 className="text-4xl lg:text-6xl font-semibold leading-tight text-gray-900 mb-6">
                            <span className='text-purple-800'>Power Line Inspection</span> <br />
                            <span> and Analysis </span>
                        </h1>

                        <p className="text-lg text-gray-600 max-w-xl mb-10 leading-relaxed">
                            Transform drone imagery into actionable infrastructure insights.
                        </p>

                        <div className="grid grid-cols-2 gap-6 max-w-lg">

                            <div className="p-4 rounded-xl bg-gray-50 border border-purple-400 hover:border-purple-600 transition">
                                <p className="text-xs text-gray-500 uppercase tracking-wide">Image Upload</p>
                                <p className="font-medium text-gray-800">Drone Image Management</p>
                            </div>

                            <div className="p-4 rounded-xl bg-gray-50 border border-purple-400 hover:border-purple-600 transition">
                                <p className="text-xs text-gray-500 uppercase tracking-wide">Annotation Tools</p>
                                <p className="font-medium text-gray-800">Manual Defect Marking</p>
                            </div>

                            <div className="p-4 rounded-xl bg-gray-50 border border-purple-400 hover:border-purple-600 transition">
                                <p className="text-xs text-gray-500 uppercase tracking-wide">Reporting</p>
                                <p className="font-medium text-gray-800">Structured PDF Output</p>
                            </div>

                            <div className="p-4 rounded-xl bg-gray-50 border border-purple-400 hover:border-purple-600 transition">
                                <p className="text-xs text-gray-500 uppercase tracking-wide">Deployment</p>
                                <p className="font-medium text-gray-800">Secure Internal Access</p>
                            </div>

                        </div>

                    </div>

                </div>

                {/* Right side */}
                <div className='relative flex items-center justify-center w-full h-screen overflow-hidden'>
                    {/* SVG blob with clipped image */}
                    <div className='absolute inset-0 flex items-center justify-end'>
                        <svg
                            viewBox="0 0 822 980"
                            className="absolute right-0 top-0 h-full w-full"
                            preserveAspectRatio="xMaxYMid slice"
                        >
                            <defs>
                                <clipPath id="curveClip">
                                    <path d="M210.222 0H1089.22V1024H210.222C210.222 1024 683.222 686 210.222 522C-262.778 358 210.222 0 210.222 0Z" />
                                </clipPath>


                            </defs>

                            <image
                                href={HeroImage}
                                x="0"
                                y="25"
                                width="822"
                                height="980"
                                preserveAspectRatio="xMaxYMax slice"
                                clipPath="url(#curveClip)"
                            />
                            <rect
                                width="100%"
                                height="100%"
                                fill="black"
                                opacity="0.3"
                                clipPath="url(#curveClip)"
                            />
                        </svg>
                    </div>

                    <DroneScene />
                    
                </div>
            </div>
        </div>
    )
}

export default LandingPage