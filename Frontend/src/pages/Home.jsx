import React, { useRef } from 'react'
import LandingPage from './LandingPage'
import DroneScene from '../components/Drone'
import Features from './Features'
import HowItsDone from './HowItsDone'


function Home() {
    const howItWorksRef = useRef(null)

    return (
        <>
            <div className='relative'>
    
                <LandingPage />
                <Features ref={howItWorksRef} />
            </div>

            <HowItsDone/>
        </>

    )
}

export default Home
