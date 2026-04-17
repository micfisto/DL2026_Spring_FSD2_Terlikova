import { useState, useEffect, useCallback, useRef } from "react";
import { gameAPI } from "../api/game.api";

/**
 * Hook for managing game questions state and fetching
 * 
 * @param {number|null} sessionId - Current game session ID
 * @returns {Object} Question state and actions
 */
export function useQuestions(sessionId) {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Cache for questions to avoid refetching
  const cacheRef = useRef(new Map());

  // Fetch questions for session
  const fetchQuestions = useCallback(async (sid) => {
    if (!sid) return;
    
    // Check cache first
    if (cacheRef.current.has(sid)) {
      const cached = cacheRef.current.get(sid);
      setQuestions(cached);
      return cached;
    }

    setLoading(true);
    setError(null);

    try {
      // Get current question from API
      const question = await gameAPI.getCurrentQuestion(sid);
      
      if (question) {
        const newQuestions = [question];
        setQuestions(newQuestions);
        cacheRef.current.set(sid, newQuestions);
      }
      
      return question;
    } catch (err) {
      console.error("Error fetching questions:", err);
      setError(err.message || "Failed to fetch questions");
    } finally {
      setLoading(false);
    }
  }, []);

  // Move to next question
  const nextQuestion = useCallback(async (sid) => {
    if (!sid) return;
    
    setLoading(true);
    
    try {
      const question = await gameAPI.nextQuestion(sid);
      
      if (question) {
        setQuestions((prev) => [...prev, question]);
        setCurrentIndex((prev) => prev + 1);
        cacheRef.current.set(sid, [...questions, question]);
      }
      
      return question;
    } catch (err) {
      console.error("Error getting next question:", err);
      setError(err.message || "Failed to get next question");
    } finally {
      setLoading(false);
    }
  }, [questions]);

  // Submit answer and get result
  const submitAnswer = useCallback(async (sid, answer) => {
    if (!sid || !answer) return;
    
    setLoading(true);
    
    try {
      const result = await gameAPI.sendAnswer(sid, answer);
      return result;
    } catch (err) {
      console.error("Error submitting answer:", err);
      setError(err.message || "Failed to submit answer");
    } finally {
      setLoading(false);
    }
  }, []);

  // Clear cache
  const clearCache = useCallback(() => {
    cacheRef.current.clear();
  }, []);

  // Reset state
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