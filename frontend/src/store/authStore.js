import { create } from "zustand";
import { persist } from "zustand/middleware";
import { adminLogin as apiAdminLogin } from "../api/admin.api";

export const useAuthStore = create(
    persist(
        (set, get) => ({
            token: null,
            isAuthenticated: false,
            loading: false,
            error: null,

            login: async (username, password) => {
                set({ loading: true, error: null });

                try {
                    const data = await apiAdminLogin(username, password);
                    set({
                        token: data.token,
                        isAuthenticated: true,
                        loading: false,
                    });
                    return true;
                } catch (error) {
                    set({
                        loading: false,
                        error: error.message || "Ошибка входа",
                    });
                    return false;
                }
            },

            logout: () => {
                set({
                    token: null,
                    isAuthenticated: false,
                    error: null,
                });
            },

            clearError: () => {
                set({ error: null });
            },
        }),
        {
            name: "auth-storage",
            partialize: (state) => ({
                token: state.token,
                isAuthenticated: state.isAuthenticated,
            }),
        }
    )
);