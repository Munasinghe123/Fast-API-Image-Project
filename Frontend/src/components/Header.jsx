import React, { useEffect, useState } from 'react'
import Logo from '../Images/Leco.png'
import { Link } from 'react-router-dom'
import { MoveRight } from 'lucide-react'

function Header() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header
      className={`
        fixed top-0 left-0 z-50 w-full 
        transition-all duration-300
        ${scrolled
          ? 'backdrop-blur-3xl '
          : 'bg-transparent'}
      `}
    >
      <div className="h-16 px-10 py-10 flex items-center justify-between ">

        <Link to="/">
          <div className="flex items-center  gap-3 group cursor-pointer">
            <img
              src={Logo}
              alt="SkyEye Logo"
              className="
                h-15 w-15 rounded-xl
                transition-transform duration-300
              "
            />
           
          </div>
        </Link>

        {/* CTA */}
        <Link to="/signin">
          <button
            className="
              group flex items-center gap-2
              px-5 py-3 rounded-full
              bg-purple-700 text-white
              text-md font-semibold
              transition-all duration-300
              hover:bg-purple-600
              hover:scale-105 
            "
          >
            Sign in
            <MoveRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          </button>
        </Link>

      </div>
    </header>
  )
}

export default Header
