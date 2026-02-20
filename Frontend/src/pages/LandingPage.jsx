import mapbg from "../Images/bg-image-2.png";
import DroneScene from "../components/Drone";


export default function LandingPage() {
    return (
        <section className="relative min-h-screen w-full overflow-hidden bg-purple-50  z-0">

            {/* SVG clip path definition */}
            <svg
                className="hidden lg:block absolute inset-0 w-full h-full  z-20"
                viewBox="0 0 1004 1003"
                preserveAspectRatio="none"
            >
                <defs>
                    <clipPath id="heroCurve">
                        <path d="M0 0H1151C1151 0 1260.05 152.53 1184 246C1129.11 313.459 1028.96 333.45 883.5 328C695.885 320.971 782.295 550.467 826.5 732C864.053 886.219 740.5 995 740.5 995H0V0Z" />
                    </clipPath>
                </defs>
            </svg>

            {/* mobile screen backgrond */}
            <div className="xl:hidden absolute inset-0"
                style={{
                    backgroundImage: `url(${mapbg})`,
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                }}
            />

            {/*desktop  Background clipped by curve */}
            <div
                className="hidden xl:block absolute inset-0"
                style={{
                    backgroundImage: `url(${mapbg})`,
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    clipPath: "url(#heroCurve)",
                }}
            />
            {/* Edge shadow overlay */}
            <div
                className="hidden xl:block absolute inset-0 "
                style={{
                    clipPath: "url(#heroCurve)",
                    background: "radial-gradient(circle at 85% 50%, rgba(0,0,0,0.6), transparent 60%)",
                }}
            />
            <div className="relative grid grid-cols-1 lg:grid-cols-2 min-h-screen">

                {/* left side */}
                {/* ── TEXT CONTENT */}
                <div className="relative space-y-10 z-40 h-full flex flex-col items-center xl:items-start text-center xl:text-left  justify-center px-10">
                    <span>
                        <span className="body-font inline-flex items-center px-4 py-1.5 rounded-full bg-gradient-to-r from-purple-500/20 to-purple-600/10 border border-purple-400/30 text-[12px] tracking-[0.25em] uppercase font-medium text-purple-200 backdrop-blur-md shadow-[0_0_20px_rgba(168,85,247,0.25)]">
                            AERIAL INTELLIGENCE
                        </span>
                    </span>

                    <h1 className="heading-font text-4xl md:text-5xl lg:text-[64px] text-white font-extrabold leading-[1.05] tracking-tight">
                        From Aerial Images
                        <br />
                        <span className="text-white">To Actionable Insights</span>
                    </h1>

                    <p className="body-font text-lg text-white/80 max-w-md leading-relaxed">
                        Drone-based image capture and intelligent data analysis to enable
                        safer, faster, and more accurate powerline inspections.
                    </p>

                    {/* <MobileDroneScene /> */}
                </div>
                {/* right side */}
                <div className="relative hidden xl:flex justify-center items-center">

                    {/* Particle layer */}
                    <div className="absolute inset-0   -z-10 overflow-hidden">
                        {Array.from({ length: 120 }).map((_, i) => (
                            <span
                                key={i}
                                className="absolute rounded-full bg-purple-400/70 shadow-[0_0_4px_rgba(168,85,247,0.5)] particle"
                                style={{
                                    width: `${3 + Math.random() * 3}px`,
                                    height: `${3 + Math.random() * 3}px`,
                                    left: `${Math.random() * 100}%`,
                                    top: `${Math.random() * 100}%`,
                                    animationDelay: `${Math.random() * 10}s`,
                                    animationDuration: `${12 + Math.random() * 10}s`,
                                }}
                            />
                        ))}
                    </div>

                    {/* floating cards */}
                    <div className="absolute inset-0  z-10 overflow-hidden">

                        {/* Card 1 — upper right */}
                        <div
                            className="absolute flex flex-col items-center justify-center text-center gap-3"
                            style={{
                                width: "150px",
                                height: "150px",
                                borderRadius: "50%",
                                top: "15%",
                                right: "7%",
                                background: "radial-gradient(circle at 30% 25%, rgba(109,40,217,0.95) 0%, rgba(60,10,120,0.98) 60%, rgba(20,5,50,1) 100%)", border: "1px solid rgba(192,132,252,0.35)",
                                boxShadow: "0 0 40px rgba(139,92,246,0.3), 0 0 80px rgba(139,92,246,0.1), inset 0 1px 0 rgba(255,255,255,0.15)",
                                backdropFilter: "blur(16px)",
                                animation: "floatCard1 6s ease-in-out infinite",
                            }}
                        >
                            {/* Glowing icon ring */}
                            <div style={{
                                width: "44px",
                                height: "44px",
                                borderRadius: "50%",
                                background: "radial-gradient(circle, rgba(168,85,247,0.5), rgba(109,40,217,0.3))",
                                border: "1px solid rgba(192,132,252,0.5)",
                                boxShadow: "0 0 16px rgba(168,85,247,0.5)",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                fontSize: "20px",
                            }}>
                                📡
                            </div>
                            <div>
                                <p style={{
                                    color: "rgba(255,255,255,0.95)",
                                    fontSize: "11.5px",
                                    fontWeight: "700",
                                    letterSpacing: "0.05em",
                                    lineHeight: "1.3",
                                    textShadow: "0 0 20px rgba(192,132,252,0.8)",
                                }}>
                                    Real-Time<br />Capture
                                </p>
                            </div>
                            {/* Inner shimmer arc */}
                            <div style={{
                                position: "absolute",
                                top: "10px",
                                left: "20px",
                                width: "60px",
                                height: "30px",
                                borderRadius: "50%",
                                background: "linear-gradient(135deg, rgba(255,255,255,0.15), transparent)",
                                filter: "blur(4px)",
                            }} />
                        </div>

                        {/* Card 2 — lower right */}
                        <div
                            className="absolute flex flex-col items-center justify-center text-center gap-3"
                            style={{
                                width: "165px",
                                height: "165px",
                                borderRadius: "50%",
                                top: "50%",
                                right: "3%",
                                background: "radial-gradient(circle at 30% 25%, rgba(88,28,135,0.98) 0%, rgba(50,8,100,0.99) 60%, rgba(15,4,40,1) 100%)", border: "1px solid rgba(167,139,250,0.3)",
                                boxShadow: "0 0 50px rgba(124,58,237,0.35), 0 0 100px rgba(124,58,237,0.12), inset 0 1px 0 rgba(255,255,255,0.12)",
                                backdropFilter: "blur(16px)",
                                animation: "floatCard2 8s ease-in-out infinite",
                            }}
                        >
                            <div style={{
                                width: "48px",
                                height: "48px",
                                borderRadius: "50%",
                                background: "radial-gradient(circle, rgba(167,139,250,0.3), rgba(124,58,237,0.1))",
                                border: "1px solid rgba(167,139,250,0.45)",
                                boxShadow: "0 0 18px rgba(124,58,237,0.55)",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                fontSize: "22px",
                            }}>
                                ⚡
                            </div>
                            <div>
                                <p style={{
                                    color: "rgba(255,255,255,0.95)",
                                    fontSize: "11.5px",
                                    fontWeight: "700",
                                    letterSpacing: "0.05em",
                                    lineHeight: "1.3",
                                    textShadow: "0 0 20px rgba(167,139,250,0.8)",
                                }}>
                                    Faster<br />Inspections
                                </p>
                            </div>
                            <div style={{
                                position: "absolute",
                                top: "12px",
                                left: "22px",
                                width: "68px",
                                height: "34px",
                                borderRadius: "50%",
                                background: "linear-gradient(135deg, rgba(255,255,255,0.12), transparent)",
                                filter: "blur(4px)",
                            }} />
                        </div>
                    </div>

                    <style>{`
                        @keyframes floatCard1 {
                            0%, 100% { transform: translateY(0px) scale(1); }
                            50%       { transform: translateY(-14px) scale(1.02); }
                        }
                        @keyframes floatCard2 {
                            0%, 100% { transform: translateY(0px) scale(1); }
                            50%       { transform: translateY(-18px) scale(1.02); }
                        }
                    `}</style>
                </div>

                <DroneScene />
            </div>
        </section>
    );
}