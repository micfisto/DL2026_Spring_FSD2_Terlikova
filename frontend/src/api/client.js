const BASE_URL =
    import.meta.env.VITE_API_URL || "http://localhost:8000";

const API_PREFIX = "/api";

export async function apiRequest(url, options = {}) {
    const res = await fetch(BASE_URL + API_PREFIX + url, {
        method: options.method || "GET",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        body: options.body
            ? JSON.stringify(options.body)
            : undefined,
    });

    const text = await res.text();

    let data;
    try {
        data = JSON.parse(text);
    } catch {
        data = null;
    }

    if (!res.ok) {
        const err = new Error(
            data?.detail || "Request failed"
        );
        err.status = res.status;
        throw err;
    }

    return data;
}