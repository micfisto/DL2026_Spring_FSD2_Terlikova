import { useEffect, useCallback, useMemo, useRef } from "react";
import { useNavigate } from "react-router-dom";
import MapView from "../components/map/MapView";
import { useGameStore } from "../store/gameStore";
import { useTimer } from "../hooks/useTimer";
import "./Game.css";

export default function Game() {
  const navigate = useNavigate();

  const question = useGameStore((s) => s.question);
  const result = useGameStore((s) => s.result);
  const selectedPoint = useGameStore((s) => s.selectedPoint);
  const loading = useGameStore((s) => s.loading);
  const sessionId = useGameStore((s) => s.sessionId);
  const score = useGameStore((s) => s.score);
  const error = useGameStore((s) => s.error);
  const answer = useGameStore((s) => s.answer);
  const next = useGameStore((s) => s.next);
  const mode = useGameStore((s) => s.mode);
  const difficulty = useGameStore((s) => s.difficulty);

  const lockRef = useRef(false);

  const getTimeForDifficulty = (diff) => {
    switch (diff) {
      case "easy": return 60;
      case "medium": return 30;
      case "hard": return 15;
      default: return 30;
    }
  };

  const timeForDifficulty = getTimeForDifficulty(difficulty);

  // Множители для разных уровней сложности
  const difficultyMultipliers = {
      "easy": 1.0,
      "medium": 1.5,
      "hard": 2.0
  };
  const baseMaxScore = 5000;
  const maxScore = Math.round(baseMaxScore * (difficultyMultipliers[difficulty] || 1.0));

  const questionId = question?.question_id ?? question?.id;

  const handleTimeUp = useCallback(() => {
    if (lockRef.current) return;
    if (!questionId || result) return;

    lockRef.current = true;

    answer().finally(() => {
      lockRef.current = false;
    });
  }, [questionId, result, answer]);

  const timer = useTimer(timeForDifficulty, handleTimeUp);

  const handleNext = async () => {
    const status = await next();
    if (status === "finished") {
      navigate("/results", {
        state: {
          sessionId,
          finalScore: score,
          difficulty: difficulty,
        },
      });
    }
  };

  useEffect(() => {
    if (!question || result || loading) {
      timer.stop();
      return;
    }

    lockRef.current = false;
    timer.reset?.();
    timer.start();
  }, [questionId, result, loading]);

  const correctPoint = useMemo(() => {
    const lat = result?.correctLat ?? result?.correct_lat;
    const lng = result?.correctLng ?? result?.correct_lng;

    if (typeof lat !== "number" || typeof lng !== "number") return null;

    return { lat, lng };
  }, [result]);

  if (!question && !result) {
    return <div className="game-loading">Игра не загружена</div>;
  }

  return (
    <div className="game">
      <div className="game-layout">
        <div className="hud">
          <h2>{question?.text}</h2>
          <div className="score-display">
            <span>Score: {score}</span>
            <span className="score-max">/ {maxScore}</span>
          </div>

          <div className={`timer ${timer.timeLeft <= 11 ? "timer-warning" : ""}`}>
            Time: {timer.timeLeft}s
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="map-container">
          <MapView
            correctPoint={correctPoint}
            showResult={!!result}
            mode={mode}
            targetCode={question?.target_name}
            selectedPoint={selectedPoint}
          />
        </div>

        {result && (
          <div className="answer-result">
            <p>Расстояние: {result.distance_km} км</p>
            <p>Очков: +{result.points_earned}</p>
          </div>
        )}

        <div className="controls">
          <button
            disabled={!selectedPoint || loading || result}
            onClick={() => {
              if (lockRef.current) return;
              lockRef.current = true;

              timer.stop();
              answer().finally(() => {
                lockRef.current = false;
              });
            }}
          >
            {loading ? "Отправка..." : "Ответить"}
          </button>

          {result && (
            <button
              onClick={handleNext}
              disabled={loading}
            >
              Далее
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
