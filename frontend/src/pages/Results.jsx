import {useState, useEffect} from "react";
import {leaderboardAPI} from "../api/leaderboard.api";
import {useLocation, useNavigate} from "react-router-dom";
import "./Results.css";

export default function Results() {
    const location = useLocation();
    const navigate = useNavigate();
    const state = location.state || {};

    const [name, setName] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [saved, setSaved] = useState(false);
    const [leaderboardData, setLeaderboardData] = useState(null);
    const [leaderboardLoading, setLeaderboardLoading] = useState(false);
    const [entryId, setEntryId] = useState(null);

    const score = state.finalScore || 0;
    const difficulty = state.difficulty || "easy";
    
    // Множители для разных уровней сложности
    const difficultyMultipliers = {
        "easy": 1.0,    // Простой: до 5000 очков
        "medium": 1.5,  // Средний: до 7500 очков
        "hard": 2.0     // Сложный: до 10000 очков
    };
    
    const baseMaxScore = 5000; // Базовый максимум для 5 вопросов
    const maxScore = Math.round(baseMaxScore * (difficultyMultipliers[difficulty] || 1.0));
    const percentage = maxScore ? (score / maxScore) * 100 : 0;

    useEffect(() => {
        if (!entryId) return;

        const loadLeaderboard = async () => {
            try {
                setLeaderboardLoading(true);

                const data = await leaderboardAPI.getLeaderboardWithUser(
                    "classic",
                    entryId
                );

                setLeaderboardData(data);
            } catch (e) {
                console.error("Error loading leaderboard:", e);
            } finally {
                setLeaderboardLoading(false);
            }
        };

        loadLeaderboard();
    }, [entryId]);

    const save = async () => {
        if (loading) return;

        if (!name.trim()) {
            setError("Введите имя");
            return;
        }

        try {
            setLoading(true);
            setError(null);

            const result = await leaderboardAPI.saveResult({
                session_id: state.sessionId,
                player_name: name.trim(),
            });

            setEntryId(result.leaderboard_entry_id);
            setSaved(true);
        } catch (e) {
            setError(e.message || "Ошибка сохранения результата");
        } finally {
            setLoading(false);
        }
    };

    const getResultEmoji = () => {
        if (percentage >= 80) return "🏆";
        if (percentage >= 60) return "🥈";
        if (percentage >= 40) return "🥉";
        return "🎮";
    };

    const getResultText = () => {
        if (percentage >= 80) return "Отлично!";
        if (percentage >= 60) return "Хорошо!";
        if (percentage >= 40) return "Неплохо!";
        return "Есть куда расти!";
    };

    return (
        <div className="results">
            <div className="results-card">
                <div className="results-emoji">{getResultEmoji()}</div>

                <h1 className="results-title">{getResultText()}</h1>

                <div className="results-score">
                    <span className="score-label">Ваш счёт</span>
                    <span className="score-value">{score}</span>
                    <span className="score-max">/ {maxScore}</span>
                </div>

                <div className="score-bar">
                    <div
                        className="score-fill"
                        style={{width: `${percentage}%`}}
                    />
                </div>

                {saved && leaderboardData && !leaderboardData.user_rank && (
                    <div className="top-five-notice">
                        🎉 Вы в топ-5!
                    </div>
                )}

                {!saved ? (
                    <div className="results-form">
                        <input
                            className="results-input"
                            placeholder="Введите ваше имя"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            disabled={loading}
                            maxLength={50}
                        />

                        <button
                            className="results-button"
                            onClick={save}
                            disabled={loading || !name.trim()}
                        >
                            {loading ? "Сохранение..." : "Сохранить результат"}
                        </button>
                    </div>
                ) : (
                    <div className="results-success">
                        <span>Результат сохранён!</span>
                    </div>
                )}

                {leaderboardLoading && (
                    <div className="loader">
                        Загрузка таблицы лидеров...
                    </div>
                )}

                {leaderboardData && !leaderboardLoading && leaderboardData.user_rank && (
                            <div className="leaderboard-user">
                                <div className="your-position">
                                    <span>Ваша позиция: </span>
                                    <strong>
                                        #{leaderboardData.user_rank}
                                    </strong>
                                    <span>
                                        {" "}
                                        из {leaderboardData.total_players}
                                    </span>
                                </div>

                                <div className="neighbors">
                                    <h4>Рядом с вами</h4>

                                    <ul className="leaderboard-list">
                                        {leaderboardData.neighbors?.map(
                                            (item) => (
                                                <li
                                                    key={item.rank}
                                                    className="leaderboard-item"
                                                >
                                                    <span className="rank">
                                                        #{item.rank}
                                                    </span>
                                                    <span className="name">
                                                        {item.player_name}
                                                    </span>
                                                    <span className="score">
                                                        {item.score}
                                                    </span>
                                                </li>
                                            )
                                        )}
                                    </ul>
                                </div>
                            </div>
                )}

                {error && (
                    <div className="results-error">{error}</div>
                )}

                <div className="results-actions">
                    <button
                        className="results-button-secondary"
                        onClick={() => navigate("/")}
                    >
                        Играть снова
                    </button>
                </div>
            </div>
        </div>
    );
}
