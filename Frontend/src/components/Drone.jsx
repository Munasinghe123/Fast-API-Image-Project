import React, { Suspense, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'

import { useEffect } from "react"
import * as THREE from "three"

function Drone() {
  const { scene } = useGLTF("/models/drone.glb")
  const ref = useRef()


  const baseY = -2.5
  const baseX = -1.3

  // motion
  useFrame((state) => {
    if (!ref.current) return
    const time = state.clock.elapsedTime
    ref.current.position.y = baseY + Math.sin(time * 1.2) * 0.15
    ref.current.position.x = baseX
  })


  return (
    <group ref={ref}>
      <primitive object={scene} scale={0.7} />
    </group>
  )
}
export default function DroneScene() {
  return (
    <div className="w-full h-screen z-10 pointer-events-none">
    
        <Canvas
          shadows
          camera={{ position: [3, 2, 6], fov: 45 }}  //x y z
          style={{ width: '100%', height: '100%' }}
        >
          <ambientLight intensity={0.7} />
          <directionalLight position={[5, 5, 5]} intensity={1} />
          <directionalLight position={[-5, 5, -5]} intensity={0.5} />

          <Suspense fallback={null}>
            <Drone />
          </Suspense>

          <OrbitControls enableZoom={false} enablePan={false} />
        </Canvas>
      
    </div>
  )
}