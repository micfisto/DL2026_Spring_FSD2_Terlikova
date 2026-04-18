import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useGameStore } from "../store/gameStore";
import "./Home.css";

export default function Home() {
    const setMode = useGameStore((s) => s.setMode);
    const error = useGameStore((s) => s.error);

    const navigate = useNavigate();
    const [selectedMode, setSelectedMode] = useState("capitals");

    const handleContinue = () => {
        setMode(selectedMode);
        navigate("/difficulty");
    };

    const modes = [
        { value: "capitals", label: "Столицы", icon: "🏛️", desc: "Угадай столицы стран" },
        { value: "countries", label: "Страны", icon: "🚩", desc: "Найди страны на карте" },
        { value: "landmarks", label: "Достояния", icon: "🗼", desc: "Найди достопримечательности" },
    ];

    return (
        <div className="home">
            <div className="hero-animation-container">
                <div className="hero-icon">🌍</div>
            </div>

            <div className="hero-title-container">
                <h1 className="hero-title">GeoQuiz</h1>
            </div>

            <div className="hero-subtitle-container">
                <p className="hero-subtitle">
                    Испытай свои знания географии! Угадай столицы, страны и достопримечательности
                </p>
            </div>

            <div className="home-content">
                <div className="mode-select">
                    <h2 className="mode-title">Выбери режим</h2>
                    <div className="mode-grid">
                        {modes.map((m) => (
                            <button
                                key={m.value}
                                className={`mode-card ${selectedMode === m.value ? "mode-card-active" : ""}`}
                                onClick={() => setSelectedMode(m.value)}
                            >
                                <span className="mode-icon">{m.icon}</span>
                                <span className="mode-label">{m.label}</span>
                                <span className="mode-desc">{m.desc}</span>
                            </button>
                        ))}
                    </div>
                </div>

                {error && <div className="home-error-message">{error}</div>}

                <button
                    className="home-start-button"
                    onClick={handleContinue}
                >
                    <span>🚀</span>
                    <span>Продолжить</span>
                </button>
            </div>
        </div>
    );
}