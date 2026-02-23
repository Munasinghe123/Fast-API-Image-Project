import React, { useRef } from "react"
import Logo from "../Images/Leco.png"
import { Link } from "react-router-dom"
import { Menu, X } from "lucide-react"
import gsap from "gsap"

function Header() {

  const sidebarRef = useRef(null)
  const overlayRef = useRef(null)

  const openNav = () => {
    gsap.to(sidebarRef.current, {
      x: 0,
      duration: 0.5,
      ease: "power3.out"
    })

    gsap.to(overlayRef.current, {
      opacity: 1,
      pointerEvents: "auto",
      duration: 0.3
    })
  }

  const closeNav = () => {
    gsap.to(sidebarRef.current, {
      x: "-100%",
      duration: 0.5,
      ease: "power3.inOut"
    })

    gsap.to(overlayRef.current, {
      opacity: 0,
      pointerEvents: "none",
      duration: 0.3
    })
  }

  return (
    <>
      {/* desktop header */}
      <header className=" fixed top-0 left-0 z-50 w-full transition-all duration-300" >
        <div className="hidden h-16 px-10 py-10 lg:flex items-center justify-between ">
          <Link to="/"> <div className="flex items-center md:pl-10 pl-5 pt-5 gap-3 group cursor-pointer">
            <img src={Logo} alt="SkyEye Logo" className=" h-17 w-17 rounded-xl transition-transform duration-300 " />
          </div> </Link> </div>
      </header>
      
      {/*moblie Header */}
      <header className="lg:hidden fixed top-0 left-0 w-full z-50">
        <div className="
          flex items-center justify-between
          h-16 px-6
          backdrop-blur-md bg-black/40
          border-b border-white/10
        ">
          {/* Hamburger */}
          <button onClick={openNav} className="text-white">
            <Menu size={24} />
          </button>

          {/* Logo */}
          <Link to="/">
            <img src={Logo} alt="Logo" className="h-10 w-10 rounded-lg" />
          </Link>
        </div>
      </header>

      {/* Overlay */}
      <div
        ref={overlayRef}
        onClick={closeNav}
        className="fixed inset-0 bg-black/60 opacity-0 pointer-events-none z-40"
      />

      {/* Sidebar */}
      <div
        ref={sidebarRef}
        className="
          fixed top-0 left-0 h-full w-72
          bg-black text-white
          shadow-2xl
          transform -translate-x-full
          z-50
          p-6
        "
      >
        <div className="flex justify-end items-center mb-8">
          <button onClick={closeNav}>
            <X size={22} />
          </button>
        </div>

        <nav className="flex flex-col gap-6 text-gray-300">
          {/* <Link to="/">Home</Link>
          <Link to="/signin">Sign In</Link>
          <Link to="/register">Register</Link> */}
        </nav>
      </div>
    </>
  )
}

export default Header