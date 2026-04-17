import { apiRequest } from "./client";

export async function adminLogin(username, password) {
    return apiRequest("/admin/login", {
        method: "POST",
        body: { username, password },
    });
}

export async function getQuestions(token) {
    return apiRequest("/admin/questions", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export async function createQuestion(token, questionData) {
    return apiRequest("/admin/questions", {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`,
        },
        body: questionData,
    });
}

export async function updateQuestion(token, questionId, questionData) {
    return apiRequest(`/admin/questions/${questionId}`, {
        method: "PUT",
        headers: {
            Authorization: `Bearer ${token}`,
        },
        body: questionData,
    });
}

export async function deleteQuestion(token, questionId) {
    return apiRequest(`/admin/questions/${questionId}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export async function toggleQuestionVisibility(token, questionId, isActive) {
    return apiRequest(`/admin/questions/${questionId}`, {
        method: "PUT",
        headers: {
            Authorization: `Bearer ${token}`,
        },
        body: { is_active: isActive },
    });
}