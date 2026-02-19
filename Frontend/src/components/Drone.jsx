import React, { Suspense, useLayoutEffect, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)



function Drone({ targetRef }) {
    const { scene } = useGLTF('/models/drone.glb')
    const ref = useRef()

    // Start and end positions
    const base = new THREE.Vector3(4, -3, 0)
    const target = new THREE.Vector3(-5, -3, 0)

    // Scroll progress (0 → 1)
    const progressRef = useRef(0)

    useLayoutEffect(() => {
        if (!targetRef?.current) return

        ScrollTrigger.create({
            trigger: targetRef.current,
            start: 'top bottom',
            end: 'top top',
            scrub: true,
            onUpdate: (self) => {
                progressRef.current = self.progress
            },
        })
    }, [targetRef])

    useFrame((state) => {
        if (!ref.current) return

        const progress = progressRef.current

        // Base scroll-driven position
        const currentPosition = new THREE.Vector3().lerpVectors(base, target, progress)

        // Time for smooth motion
        const time = state.clock.elapsedTime

        // Subtle idle motion (ONLY when near initial state)
        if (progress < 0.02) {
            currentPosition.y += Math.sin(time * 1.5) * 0.08   // gentle up/down
            currentPosition.x += Math.sin(time * 0.8) * 0.05   // slight side drift
        }

        ref.current.position.copy(currentPosition)

        // Keep your existing rotation logic
        ref.current.rotation.set(0, progress * 0.5, 0)
    })

    return <primitive ref={ref} object={scene} scale={1} />
}

export default function DroneScene({ targetRef }) {
    return (
        <div className="fixed inset-0 z-10 pointer-events-none">
            <Canvas camera={{ position: [0, 5, 6], fov: 50 }}>
                <ambientLight intensity={0.6} />
                <directionalLight position={[5, 5, 5]} intensity={1} />
                <directionalLight position={[-5, 5, -5]} intensity={0.5} />

                <Suspense fallback={null}>
                    <Drone targetRef={targetRef} />
                </Suspense>

                <OrbitControls enableZoom={false} enablePan={false} />
            </Canvas>
        </div>
    )
}