import { create } from "zustand";
import { gameAPI } from "../api/game.api";

export const useGameStore = create((set, get) => ({
    sessionId: null,

    question: null,
    currentQuestionId: null,

    progress: null,
    score: 0,

    result: null,

    loading: false,

    selectedPoint: null,

    error: null,

    mode: null,
    difficulty: null,

    setMode: (mode) => set({ mode }),
    setDifficulty: (difficulty) => set({ difficulty }),

    startGame: async (config) => {
        set({
            loading: true,
            error: null,
            mode: config.mode,
            difficulty: config.difficulty,
            result: null,
            selectedPoint: null,
            currentQuestionId: null,
        });

        try {
            const data = await gameAPI.startGame(config);

            const qid = data.question?.id ?? data.question?.question_id;

            set({
                sessionId: data.session_id,
                question: data.question,
                currentQuestionId: qid,
                progress: data.progress,
                score: data.score,
                loading: false,
            });

            return data;
        } catch (e) {
            set({
                error: e.message || "Ошибка запуска игры",
                loading: false,
            });
        }
    },

    setSelectedPoint: (point) => set({ selectedPoint: point }),

    answer: async () => {
        const state = get();

        const {
            sessionId,
            selectedPoint,
            question,
            currentQuestionId,
            loading,
            result,
        } = state;

        if (loading || result) return;
        if (!sessionId || !question) return;

        const qid = question?.id ?? question?.question_id;

        // 🔥 ЖЁСТКАЯ ЗАЩИТА ОТ 400
        if (!qid || qid !== currentQuestionId) {
            console.warn("DROP ANSWER:", { qid, currentQuestionId });
            return;
        }

        set({ loading: true, error: null });

        // Если точка не выбрана (таймер истёк), используем координаты по умолчанию (0, 0)
        const lat = selectedPoint?.lat ?? 0;
        const lng = selectedPoint?.lng ?? 0;

        try {
            const res = await gameAPI.sendAnswer(sessionId, {
                question_id: qid,
                selected_lat: lat,
                selected_lng: lng,
            });

            set({
                result: res,
                score: res.total_score ?? state.score,
                loading: false,
            });

            return res;
        } catch (e) {
            set({
                error: e.message || "Ошибка ответа",
                loading: false,
            });
        }
    },

    next: async () => {
        const { sessionId } = get();
        if (!sessionId) return;

        set({
            loading: true,
            result: null,
            selectedPoint: null,
        });

        try {
            const data = await gameAPI.nextQuestion(sessionId);

            if (data.game_finished) {
                set({
                    question: null,
                    currentQuestionId: null,
                    loading: false,
                    score: data.final_score,
                });
                return "finished";
            }

            const qid = data.question?.id ?? data.question?.question_id;

            set({
                question: data.question,
                currentQuestionId: qid,
                progress: data.progress,
                score: data.score,
                loading: false,
            });
        } catch (e) {
            set({
                error: e.message || "Ошибка следующего вопроса",
                loading: false,
            });
        }
    },

    finish: async () => {
        const { sessionId } = get();
        if (!sessionId) return;
        return gameAPI.finishGame(sessionId);
    },

    clearError: () => set({ error: null }),
}));