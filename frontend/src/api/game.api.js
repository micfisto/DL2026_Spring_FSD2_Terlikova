import { apiRequest } from "./client";

export const gameAPI = {
    startGame: (data) =>
        apiRequest("/game/start", {
            method: "POST",
            body: data,
        }),

    sendAnswer: (sessionId, payload) =>
        apiRequest(`/game/${sessionId}/answer`, {
            method: "POST",
            body: payload,
        }),

    nextQuestion: (sessionId) =>
        apiRequest(`/game/${sessionId}/next`),

    getCurrentQuestion: (sessionId) =>
        apiRequest(`/game/${sessionId}/question`),

    finishGame: (sessionId) =>
        apiRequest(`/game/${sessionId}/finish`, {
            method: "POST",
        }),
};