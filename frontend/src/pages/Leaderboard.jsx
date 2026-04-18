import { useState, useEffect } from "react";
import { leaderboardAPI } from "../api/leaderboard.api";
import { useGameStore } from "../store/gameStore";
import "./Leaderboard.css";

const MODES = ["capitals", "countries", "landmarks"];

export default function Leaderboard() {
    const [activeMode, setActiveMode] = useState("capitals");
    const [leaderboards, setLeaderboards] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const gameState = useGameStore.getState();
    const defaultMode = gameState.mode || "capitals";

    useEffect(() => {
        setActiveMode(defaultMode);
    }, [defaultMode]);

    useEffect(() => {
        loadAllLeaderboards();
    }, []);

    const loadAllLeaderboards = async () => {
        try {
            setLoading(true);
            const results = {};
            
            for (const mode of MODES) {
                try {
                    const data = await leaderboardAPI.getLeaderboard(mode);
                    results[mode] = data.items || [];
                } catch (err) {
                    console.error(`Error loading ${mode} leaderboard:`, err);
                    results[mode] = [];
                }
            }
            
            setLeaderboards(results);
        } catch (err) {
            console.error("Error loading leaderboards:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const leaderboard = leaderboards[activeMode] || [];

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

    return (
        <div className="leaderboard-container">
            <h2 className="leaderboard-title">🏆 Таблица лидеров</h2>
            
            <div className="leaderboard-tabs">
                {MODES.map((mode) => (
                    <button
                        key={mode}
                        className={`leaderboard-tab ${activeMode === mode ? 'active' : ''}`}
                        onClick={() => setActiveMode(mode)}
                    >
                        {getModeLabel(mode)}
                    </button>
                ))}
            </div>

            {!leaderboard.length ? (
                <div className="leaderboard-empty">
                    <p>В категории "{getModeLabel(activeMode)}" пока нет результатов. Будь первым!</p>
                </div>
            ) : (
                <>
                    <p className="leaderboard-mode">{getModeLabel(activeMode)}</p>

                    <div className="leaderboard-table-container">
                        <table className="leaderboard-table">
                            <thead>
                                <tr>
                                    <th className="leaderboard-rank">Место</th>
                                    <th className="leaderboard-name">Игрок</th>
                                    <th className="leaderboard-score">Очки</th>
                                    <th className="leaderboard-date">Дата</th>
                                </tr>
                            </thead>
                            <tbody>
                                {leaderboard.slice(0, 5).map((entry, index) => (
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
                </>
            )}
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
