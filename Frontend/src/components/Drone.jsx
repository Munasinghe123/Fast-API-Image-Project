import React, { Suspense, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'

function Drone() {
  const { scene } = useGLTF('/models/drone.glb')
  const ref = useRef()

  const baseY = -2.5   // your current height

  useFrame((state) => {
    if (!ref.current) return
    const time = state.clock.elapsedTime

    // subtle vertical float
    ref.current.position.y = baseY + Math.sin(time * 1.5) * 0.2
  })

  return (
    <primitive
      ref={ref}
      object={scene}
      scale={0.8}
      position={[3.5, baseY, 0]}
    />
  )
}

export default function DroneScene() {
  return (
    <div className="absolute hidden xl:block inset-0 z-10 pointer-events-none">
      <Canvas
        camera={{ position: [0, 2, 8], fov: 45 }}
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