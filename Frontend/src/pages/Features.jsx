import { useEffect, useRef } from "react"
import gsap from "gsap"
import { ScrollTrigger } from "gsap/ScrollTrigger"

import aiImg from "../Images/ai.png"
import realtimeImg from "../Images/real-time.png"
import safetyImg from "../Images/safety.png"
import reportImg from "../Images/reporting.png"

gsap.registerPlugin(ScrollTrigger)

const features = [
  {
    title: "Aerial Data Capture",
    description: "Autonomous inspection with real-time imagery.",
    image: aiImg,
  },
  {
    title: "Secure Image Storage",
    description: "Encrypted and indexed inspection data.",
    image: realtimeImg,
  },
  {
    title: "AI-Powered Inspection",
    description: "Automated obstacle avoidance and analysis.",
    image: safetyImg,
  },
  {
    title: "Actionable Insights",
    description: "Instant reports and maintenance alerts.",
    image: reportImg,
  },
]

export default function Features() {
  const sectionRef = useRef(null)
  const cardsRef = useRef([])
  const currentStep = useRef(0)

  const tilt = -14
  const radius = 260
  const depth = 220
  const scrollFactor = 1.15

  useEffect(() => {
    if (window.innerWidth < 1024) return
    const total = features.length
    const angleStep = (Math.PI * 2) / total

    const setPositions = (step) => {
      cardsRef.current.forEach((card, i) => {
        if (!card) return

        const angle = i * angleStep - step * angleStep
        const x = Math.cos(angle) * radius
        const y = Math.sin(angle) * radius * 0.45
        const z = Math.sin(angle) * depth

        const scale = gsap.utils.mapRange(-depth, depth, 0.65, 1.05, z)
        const opacity = gsap.utils.mapRange(-depth, depth, 0.3, 1, z)
        const blur = gsap.utils.mapRange(-depth, depth, 6, 0, z)

        gsap.to(card, {
          x,
          y,
          z,
          scale,
          opacity,
          filter: `blur(${blur}px)`,
          zIndex: Math.round(scale * 100),
          duration: 0.6,
          ease: "power2.out",
        })
      })
    }

    setPositions(0)

    const trigger = ScrollTrigger.create({
      trigger: sectionRef.current,
      start: "top top",
      end: `+=${window.innerHeight * (total - 1) * scrollFactor}`,
      pin: true,
      scrub: true,
      onUpdate: (self) => {
        const nextStep = Math.round(self.progress * (total - 1))

        if (nextStep !== currentStep.current) {
          currentStep.current = nextStep
          setPositions(currentStep.current)
        }
      },
    })

    return () => trigger.kill()
  }, [])

  return (
    <section
      ref={sectionRef}
      className="relative min-h-screen bg-purple-50 overflow-hidden"
    >
      <div className="hidden lg:grid grid-cols-2 min-h-screen">

        {/* Heading*/}
        <div className="absolute left-10 md:left-20 top-24 z-20 max-w-sm">
          <span className="block text-sm uppercase tracking-widest text-purple-500 mb-3">
            Features
          </span>

          <h2 className="text-4xl md:text-5xl font-bold tracking-tight text-black mb-6">
            Built for modern{" "}
            <span className="text-purple-700">inspection</span>
          </h2>

          <div className="w-12 h-[2px] bg-black rounded-full mb-6" />

          <p className="text-slate-600 text-lg leading-relaxed">
            Intelligent solutions for{" "}
            <span className="text-purple-600 font-medium">
              modern infrastructure inspection
            </span>
          </p>
        </div>
        <div className="hidden lg:block">
          {/* Orbit Wrapper */}
          <div
            className="absolute right-16 mr-10 top-1/2 -translate-y-1/2 w-[720px] h-[720px]"
            style={{
              perspective: "1200px",
              transform: `rotateX(${tilt}deg)`,
            }}
          >
            {features.map((f, i) => (
              <div
                key={i}
                ref={(el) => (cardsRef.current[i] = el)}
                className="
              absolute left-1/2 top-1/2 
              -translate-x-1/2 -translate-y-1/2
              w-[400px] h-[240px]
              rounded-3xl overflow-hidden
              bg-white/85 backdrop-blur-2xl
              border border-purple-400/30
            "
                style={{ transformStyle: "preserve-3d" }}
              >
                <img
                  src={f.image}
                  alt=""
                  className="absolute inset-0 w-full h-full object-cover brightness-95"
                />

                <div className="
              absolute inset-0
              bg-gradient-to-t
              from-black/70
              via-black/35
              to-transparent
            " />

                <div className="relative z-10 p-6 h-full flex flex-col justify-end">
                  <h3 className="text-2xl font-semibold text-white">
                    {f.title}
                  </h3>
                  <p className="mt-2 text-sm text-white">
                    {f.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="lg:hidden px-6 py-20">
        <div className="max-w-xl mx-auto text-center mb-16">
          <span className="block text-sm uppercase tracking-widest text-purple-500 mb-3">
            Features
          </span>

          <h2 className="text-4xl md:text-5xl font-bold tracking-tight text-black mb-6">
            Built for modern{" "}
            <span className="text-purple-700">inspection</span>
          </h2>

          <div className="w-12 h-[2px] bg-black rounded-full mx-auto mb-6" />

          <p className="text-slate-600 text-lg leading-relaxed">
            Intelligent solutions for modern infrastructure inspection.
          </p>
        </div>
        {/* MOBILE & TABLET STACKED VERSION */}
        <div className="lg:hidden px-6 py-20">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((f, i) => (
              <div
                key={i}
                className="rounded-2xl overflow-hidden bg-white shadow-lg"
              >
                <img
                  src={f.image}
                  alt=""
                  className="w-full h-48 object-cover"
                />

                <div className="p-6">
                  <h3 className="text-xl font-semibold text-black">
                    {f.title}
                  </h3>

                  <p className="mt-2 text-slate-600">
                    {f.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}