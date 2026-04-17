import { useState, useEffect } from "react";
import { leaderboardAPI } from "../api/leaderboard.api";
import { useGameStore } from "../store/gameStore";
import "./Leaderboard.css";

export default function Leaderboard() {
    const [leaderboard, setLeaderboard] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const gameState = useGameStore.getState();
    const mode = gameState.mode || "capitals";

    useEffect(() => {
        loadLeaderboard();
    }, [mode]);

    const loadLeaderboard = async () => {
        try {
            setLoading(true);
            const data = await leaderboardAPI.getLeaderboard(mode);
            console.log("Leaderboard API response:", data);
            // API возвращает { items: [...] }
            setLeaderboard(data.items || []);
        } catch (err) {
            console.error("Error loading leaderboard:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="leaderboard-loading">
                <span className="loading-spinner">⏳</span>
                <p>Загрузка таблицы лидеров...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="leaderboard-error">
                <p>Не удалось загрузить таблицу лидеров</p>
            </div>
        );
    }

    if (!leaderboard.length) {
        return (
            <div className="leaderboard-empty">
                <p>Пока нет результатов. Будь первым!</p>
            </div>
        );
    }

    return (
        <div className="leaderboard-container">
            <h2 className="leaderboard-title">🏆 Таблица лидеров</h2>
            <p className="leaderboard-mode">Режим: {getModeLabel(mode)}</p>

            <table className="leaderboard-table">
                <thead>
                    <tr>
                        <th>Место</th>
                        <th>Игрок</th>
                        <th>Очки</th>
                        <th>Дата</th>
                    </tr>
                </thead>
                <tbody>
                    {leaderboard.map((entry, index) => (
                        <tr
                            key={entry.id || index}
                            className={`leaderboard-row ${index < 3 ? 'top-three' : ''}`}
                        >
                            <td className="leaderboard-rank">
                                {index === 0 && <span className="rank-badge gold">🥇</span>}
                                {index === 1 && <span className="rank-badge silver">🥈</span>}
                                {index === 2 && <span className="rank-badge bronze">🥉</span>}
                                {index > 2 && <span className="rank-number">{index + 1}</span>}
                            </td>
                            <td className="leaderboard-name">{entry.player_name}</td>
                            <td className="leaderboard-score">{entry.score}</td>
                            <td className="leaderboard-date">
                                {formatDate(entry.played_at)}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function getModeLabel(mode) {
    const labels = {
        capitals: "Столицы",
        countries: "Страны",
        landmarks: "Достопримечательности"
    };
    return labels[mode] || mode;
}

function formatDate(dateString) {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("ru-RU", {
        day: "numeric",
        month: "short",
        year: "numeric"
    });
}
