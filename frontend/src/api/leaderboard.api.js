import { apiRequest } from "./client";

export const leaderboardAPI = {
    getLeaderboard: (mode) =>
        apiRequest(`/leaderboard?mode=${mode}`),

    saveResult: (data) =>
        apiRequest("/leaderboard/save", {
            method: "POST",
            body: data,
        }),

    getLeaderboardWithUser: (mode, userEntryId) => {
        const params = new URLSearchParams({ mode });

        if (userEntryId) {
            params.append("user_entry_id", userEntryId);
        }

        return apiRequest(
            `/leaderboard/with-user?${params.toString()}`
        );
    },
};