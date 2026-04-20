import { useState, useCallback, useRef } from "react";
import { gameAPI } from "../api/game.api";

export function useQuestions(sessionId) {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const cacheRef = useRef(new Map());

  const fetchQuestions = useCallback(async () => {
    if (!sessionId) return;

    if (cacheRef.current.has(sessionId)) {
      const cached = cacheRef.current.get(sessionId);
      setQuestions(cached);
      return cached;
    }

    setLoading(true);
    setError(null);

    try {
      const question = await gameAPI.getCurrentQuestion(sessionId);

      if (question) {
        const newQuestions = [question];
        setQuestions(newQuestions);
        cacheRef.current.set(sessionId, newQuestions);
      }

      return question;
    } catch (err) {
      console.error("Error fetching questions:", err);
      setError(err.message || "Failed to fetch questions");
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const nextQuestion = useCallback(async () => {
    if (!sessionId) return;

    setLoading(true);

    try {
      const question = await gameAPI.nextQuestion(sessionId);

      if (question) {
        setQuestions((prev) => {
          const updated = [...prev, question];
          cacheRef.current.set(sessionId, updated);
          return updated;
        });

        setCurrentIndex((prev) => prev + 1);
      }

      return question;
    } catch (err) {
      console.error("Error getting next question:", err);
      setError(err.message || "Failed to get next question");
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const submitAnswer = useCallback(async (answer) => {
    if (!sessionId || !answer) return;

    setLoading(true);

    try {
      return await gameAPI.sendAnswer(sessionId, answer);
    } catch (err) {
      console.error("Error submitting answer:", err);
      setError(err.message || "Failed to submit answer");
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const clearCache = useCallback(() => {
    cacheRef.current.clear();
  }, []);

  const reset = useCallback(() => {
    setQuestions([]);
    setCurrentIndex(0);
    setError(null);
  }, []);

  return {
    questions,
    currentIndex,
    currentQuestion: questions[currentIndex],
    loading,
    error,
    fetchQuestions,
    nextQuestion,
    submitAnswer,
    clearCache,
    reset,
  };
}