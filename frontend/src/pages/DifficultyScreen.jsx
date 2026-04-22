import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useGameStore } from "../store/gameStore";
import "./DifficultyScreen.css";

export default function DifficultyScreen() {
    const startGame = useGameStore((s) => s.startGame);
    const error = useGameStore((s) => s.error);
    const loading = useGameStore((s) => s.loading);
    const mode = useGameStore((s) => s.mode);

    const navigate = useNavigate();
    const [selectedDifficulty, setSelectedDifficulty] = useState("medium");

    if (!mode) {
        navigate("/");
        return null;
    }

    const handleStart = async () => {
        try {
            useGameStore.setState({ error: null });

            const payload = {
                mode,
                difficulty: selectedDifficulty,
                question_count: 5,
            };

            const res = await startGame(payload);

            if (res) {
                navigate("/game");
            }
        } catch (e) {
            useGameStore.setState({ error: e.message });
        }
    };

    const handleBack = () => {
        navigate("/");
    };

    const difficulties = [
        { 
            value: "easy", 
            label: "Легкий", 
            icon: "🔥",
            desc: "Больше времени, крупные регионы",
            time: "60 сек",
            score: "x1"
        },
        { 
            value: "medium", 
            label: "Средний", 
            icon: "🔥🔥",
            desc: "Баланс времени и сложности",
            time: "30 сек",
            score: "x1.5"
        },
        { 
            value: "hard", 
            label: "Сложный", 
            icon: "🔥🔥🔥",
            desc: "Мало времени, все регионы",
            time: "15 сек",
            score: "x2"
        },
    ];

    const getModeLabel = () => {
        const modes = {
            capitals: "Столицы",
            countries: "Страны",
            landmarks: "Достопримечательности",
        };
        return modes[mode] || mode;
    };

    return (
        <div className="difficulty-screen">
            <button className="back-button" onClick={handleBack}>
                ← Назад
            </button>

            <div className="difficulty-header">
                <h1>Выбери сложность</h1>
                <p className="selected-mode">Режим: <strong>{getModeLabel()}</strong></p>
            </div>

            <div className="difficulty-grid">
                {difficulties.map((d) => (
                    <button
                        key={d.value}
                        className={`difficulty-card ${selectedDifficulty === d.value ? "difficulty-card-active" : ""}`}
                        onClick={() => setSelectedDifficulty(d.value)}
                    >
                        <span className="difficulty-icon">{d.icon}</span>
                        <span className="difficulty-label">{d.label}</span>
                        <span className="difficulty-desc">{d.desc}</span>
                        <div className="difficulty-stats">
                            <span>⏱️ {d.time}</span>
                            <span>⭐ {d.score}</span>
                        </div>
                    </button>
                ))}
            </div>

            {error && <div className="difficulty-error-message">{error}</div>}

            <button
                className="difficulty-screen-start-button"
                onClick={handleStart}
                disabled={loading}
            >
                {loading ? (
                    <span className="difficulty-loading-spinner">⏳</span>
                ) : (
                    <>
                        <span>🚀</span>
                        <span>Начать игру</span>
                    </>
                )}
            </button>
        </div>
    );
}