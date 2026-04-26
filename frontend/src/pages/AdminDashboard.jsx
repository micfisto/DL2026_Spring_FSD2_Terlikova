import { useState, useEffect, useRef } from "react";
import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import {
    getQuestions,
    createQuestion,
    updateQuestion,
    deleteQuestion,
    toggleQuestionVisibility,
} from "../api/admin.api";

import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import "./AdminDashboard.css";

const MODES = [
    { value: "capitals", label: "Столицы" },
    { value: "countries", label: "Страны" },
    { value: "landmarks", label: "Достопримечательности" }
];

const DIFFICULTIES = [
    { value: "easy", label: "Легко" },
    { value: "medium", label: "Средне" },
    { value: "hard", label: "Сложно" }
];

const MODE_LABELS = {
    capitals: "Столицы",
    countries: "Страны",
    landmarks: "Достопримечательности"
};

const emptyForm = {
    question_text: "",
    mode: "capitals",
    target_name: "",
    target_type: "capital",
    correct_lat: "",
    correct_lng: "",
    country_code: "",
    difficulty: "easy",
    is_active: true,
};

export default function AdminDashboard() {
    const { token, isAuthenticated, logout } = useAuthStore();

    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(false);

    const [form, setForm] = useState(emptyForm);
    const [editingId, setEditingId] = useState(null);

    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const [filterDifficulty, setFilterDifficulty] = useState("all");
    const [filterMode, setFilterMode] = useState("all");
    const [filterActive, setFilterActive] = useState("all");

    const [deleteTarget, setDeleteTarget] = useState(null);

    const formRef = useRef(null);

    useEffect(() => {
        fetchQuestions();
    }, [token]);

    if (!isAuthenticated || !token) {
        return <Navigate to="/admin/login" replace />;
    }

    async function fetchQuestions() {
        try {
            setLoading(true);
            const data = await getQuestions(token);
            setQuestions(data || []);
        } finally {
            setLoading(false);
        }
    }

    const handleEdit = (q) => {
        setForm({
            question_text: q.question_text,
            mode: q.mode,
            target_name: q.target_name,
            target_type: q.target_type,
            correct_lat: String(q.correct_lat ?? ""),
            correct_lng: String(q.correct_lng ?? ""),
            country_code: q.country_code ?? "",
            difficulty: q.difficulty,
            is_active: q.is_active,
        });

        setEditingId(q.id);

        setTimeout(() => {
            formRef.current?.scrollIntoView({ behavior: "smooth" });
        }, 80);
    };

    const resetForm = () => {
        setForm(emptyForm);
        setEditingId(null);
        setError(null);
        setSuccess(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        const payload = {
            ...form,
            correct_lat: Number(form.correct_lat),
            correct_lng: Number(form.correct_lng),
            country_code: form.country_code?.trim() || null,
        };

        try {
            if (editingId) {
                await updateQuestion(token, editingId, payload);
                setSuccess("Вопрос обновлён");
            } else {
                await createQuestion(token, payload);
                setSuccess("Вопрос создан");
            }

            resetForm();
            fetchQuestions();

        } catch (err) {
            setError(err?.response?.data?.detail || "Ошибка при сохранении вопроса");
        }
    };

    const handleDeleteClick = (q) => {
        setDeleteTarget(q);
    };

    const confirmDelete = async () => {
        if (!deleteTarget) return;

        await deleteQuestion(token, deleteTarget.id);
        setDeleteTarget(null);
        fetchQuestions();
    };

    const cancelDelete = () => {
        setDeleteTarget(null);
    };

    const handleToggleVisibility = async (q) => {
        await toggleQuestionVisibility(token, q.id, !q.is_active);
        fetchQuestions();
    };

    const filteredQuestions = questions.filter(q => {
        if (filterDifficulty !== "all" && q.difficulty !== filterDifficulty) return false;
        if (filterMode !== "all" && q.mode !== filterMode) return false;
        if (filterActive !== "all" && q.is_active !== (filterActive === "active")) return false;
        return true;
    });

    return (
        <div className="admin-dashboard">

            <div className="admin-header">
                <h1>Управление вопросами</h1>
                <Button onClick={logout}>Выйти</Button>
            </div>

            <div className="admin-content">

                <div className="admin-form-section" ref={formRef}>

                    <h2>{editingId ? "Редактирование" : "Создание"}</h2>

                    <form onSubmit={handleSubmit} className="question-form">

                        <Input
                            value={form.question_text}
                            onChange={(e) =>
                                setForm({ ...form, question_text: e.target.value })
                            }
                            placeholder="Текст вопроса"
                        />

                        <div className="form-row">
                            <select
                                value={form.mode}
                                onChange={(e) =>
                                    setForm({
                                        ...form,
                                        mode: e.target.value,
                                        target_type:
                                            e.target.value === "capitals"
                                                ? "capital"
                                                : e.target.value === "countries"
                                                    ? "country"
                                                    : "landmark",
                                    })
                                }
                            >
                                {MODES.map(m => (
                                    <option key={m.value} value={m.value}>
                                        {m.label}
                                    </option>
                                ))}
                            </select>

                            <select
                                value={form.difficulty}
                                onChange={(e) =>
                                    setForm({ ...form, difficulty: e.target.value })
                                }
                            >
                                {DIFFICULTIES.map(d => (
                                    <option key={d.value} value={d.value}>
                                        {d.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <Input
                            value={form.target_name}
                            onChange={(e) =>
                                setForm({ ...form, target_name: e.target.value })
                            }
                            placeholder="Название"
                        />

                        <Input
                            value={form.country_code}
                            onChange={(e) =>
                                setForm({
                                    ...form,
                                    country_code: e.target.value.toUpperCase()
                                })
                            }
                            placeholder="Country code (FRA)"
                            maxLength={3}
                        />

                        <div className="form-row">
                            <Input
                                type="number"
                                value={form.correct_lat}
                                onChange={(e) =>
                                    setForm({ ...form, correct_lat: e.target.value })
                                }
                                placeholder="lat"
                            />
                            <Input
                                type="number"
                                value={form.correct_lng}
                                onChange={(e) =>
                                    setForm({ ...form, correct_lng: e.target.value })
                                }
                                placeholder="lng"
                            />
                        </div>

                        {error && <div className="error">{error}</div>}
                        {success && <div className="success">{success}</div>}

                        <Button type="submit">
                            {editingId ? "Сохранить" : "Создать"}
                        </Button>
                    </form>
                </div>

                <div className="admin-questions-section">

                    <h2>Вопросы</h2>

                    <div className="questions-filter">
                        <select value={filterDifficulty} onChange={(e) => setFilterDifficulty(e.target.value)}>
                            <option value="all">Все сложности</option>
                            {DIFFICULTIES.map(d => (
                                <option key={d.value} value={d.value}>{d.label}</option>
                            ))}
                        </select>

                        <select value={filterMode} onChange={(e) => setFilterMode(e.target.value)}>
                            <option value="all">Все режимы</option>
                            {MODES.map(m => (
                                <option key={m.value} value={m.value}>{m.label}</option>
                            ))}
                        </select>

                        <select value={filterActive} onChange={(e) => setFilterActive(e.target.value)}>
                            <option value="all">Все</option>
                            <option value="active">Активные</option>
                            <option value="inactive">Неактивные</option>
                        </select>
                    </div>

                    {loading ? (
                        <div className="loading">Загрузка...</div>
                    ) : (
                        <div className="questions-grid">
                            {filteredQuestions.map(q => (
                                <div key={q.id} className="question-card">

                                    <div className="question-header">
                                        <span>{MODE_LABELS[q.mode]}</span>
                                        <span className={`question-difficulty ${q.difficulty}`}>
                                            {DIFFICULTIES.find(d => d.value === q.difficulty)?.label}
                                        </span>
                                    </div>

                                    <p>{q.question_text}</p>

                                    <small>{q.target_name}</small>
                                    <small>{q.country_code ?? "—"}</small>
                                    <small>{q.correct_lat}, {q.correct_lng}</small>

                                    <div className="question-actions">
                                        <Button small onClick={() => handleEdit(q)}>Ред.</Button>
                                        <Button small onClick={() => handleToggleVisibility(q)}>
                                            {q.is_active ? "Hide" : "Show"}
                                        </Button>
                                        <Button small onClick={() => handleDeleteClick(q)}>
                                            Del
                                        </Button>
                                    </div>

                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {deleteTarget && (
                <div className="modal-overlay">
                    <div className="modal-box">

                        <h3>Удалить вопрос?</h3>

                        <p className="modal-text">
                            {deleteTarget.question_text}
                        </p>

                        <div className="modal-actions">
                            <button className="danger-btn" onClick={confirmDelete}>
                                Удалить
                            </button>

                            <button className="cancel-btn" onClick={cancelDelete}>
                                Отмена
                            </button>
                        </div>

                    </div>
                </div>
            )}

        </div>
    );
}