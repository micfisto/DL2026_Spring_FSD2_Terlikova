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
    { value: "easy", label: "Легко", color: "#22c55e" },
    { value: "medium", label: "Средне", color: "#f59e0b" },
    { value: "hard", label: "Сложно", color: "#ef4444" }
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
    correct_lat: "",
    correct_lng: "",
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

    const formRef = useRef(null);

    // ✅ ВСЕ ХУКИ СНАЧАЛА
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

    const scrollToForm = () => {
        setTimeout(() => {
            formRef.current?.scrollIntoView({
                behavior: "smooth",
                block: "start",
            });
        }, 80);
    };

    const handleEdit = (q) => {
        setForm({
            question_text: q.question_text,
            mode: q.mode,
            target_name: q.target_name,
            correct_lat: String(q.correct_lat),
            correct_lng: String(q.correct_lng),
            difficulty: q.difficulty,
            is_active: q.is_active,
        });

        setEditingId(q.id);
        scrollToForm();
    };

    const resetForm = () => {
        setForm(emptyForm);
        setEditingId(null);
        setError(null);
        setSuccess(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const payload = {
            ...form,
            target_type:
                form.mode === "capitals"
                    ? "capital"
                    : form.mode === "countries"
                    ? "country"
                    : "landmark",
            correct_lat: parseFloat(form.correct_lat),
            correct_lng: parseFloat(form.correct_lng),
        };

        if (editingId) {
            await updateQuestion(token, editingId, payload);
            setSuccess("Вопрос обновлён");
        } else {
            await createQuestion(token, payload);
            setSuccess("Вопрос создан");
        }

        resetForm();
        fetchQuestions();
    };

    const handleDelete = async (id) => {
        if (!confirm("Удалить вопрос?")) return;
        await deleteQuestion(token, id);
        fetchQuestions();
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

                {/* FORM */}
                <div className="admin-form-section" ref={formRef}>

                    <div className="form-header">
                        <h2>
                            {editingId ? "Редактирование" : "Создание"}
                        </h2>

                        {editingId && (
                            <Button small onClick={resetForm}>
                                Отмена
                            </Button>
                        )}
                    </div>

                    <form onSubmit={handleSubmit} className="question-form">

                        <Input
                            value={form.question_text}
                            onChange={(e) =>
                                setForm({ ...form, question_text: e.target.value })
                            }
                            placeholder="Текст вопроса"
                            maxLength={200}
                        />

                        <div className="form-row">
                            <select
                                value={form.mode}
                                onChange={(e) =>
                                    setForm({ ...form, mode: e.target.value })
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
                            placeholder="Название страны"
                            maxLength={100}
                        />

                        <div className="form-row">
                            <Input
                                type="number"
                                value={form.correct_lat}
                                onChange={(e) =>
                                    setForm({ ...form, correct_lat: e.target.value })
                                }
                                placeholder="lat"
                                maxLength={15}
                            />
                            <Input
                                type="number"
                                value={form.correct_lng}
                                onChange={(e) =>
                                    setForm({ ...form, correct_lng: e.target.value })
                                }
                                placeholder="lng"
                                maxLength={15}
                            />
                        </div>

                        {error && <div className="error">{error}</div>}
                        {success && <div className="success">{success}</div>}

                        <Button type="submit">
                            {editingId ? "Сохранить" : "Создать"}
                        </Button>
                    </form>
                </div>

                {/* LIST */}
                <div className="admin-questions-section">

                    <h2>Вопросы</h2>

                    <div className="questions-filter">
                        <select
                            value={filterDifficulty}
                            onChange={(e) => setFilterDifficulty(e.target.value)}
                        >
                            <option value="all">Все сложности</option>
                            {DIFFICULTIES.map(d => (
                                <option key={d.value} value={d.value}>{d.label}</option>
                            ))}
                        </select>

                        <select
                            value={filterMode}
                            onChange={(e) => setFilterMode(e.target.value)}
                        >
                            <option value="all">Все категории</option>
                            {MODES.map(m => (
                                <option key={m.value} value={m.value}>{m.label}</option>
                            ))}
                        </select>

                        <select
                            value={filterActive}
                            onChange={(e) => setFilterActive(e.target.value)}
                        >
                            <option value="all">Все статусы</option>
                            <option value="active">Активные</option>
                            <option value="inactive">Неактивные</option>
                        </select>
                    </div>

                    {loading ? (
                        <div>Загрузка...</div>
                    ) : (
                        <div className="questions-grid">
                            {filteredQuestions.map(q => (
                                <div
                                    key={q.id}
                                    className={`question-card ${
                                        q.id === editingId ? "editing" : ""
                                    } ${!q.is_active ? "inactive" : ""}`}
                                >
                                    <div className="question-header">
                                        <span className={`question-difficulty ${q.difficulty}`}>
                                            {q.difficulty === 'easy' ? 'Легко' : q.difficulty === 'medium' ? 'Средне' : 'Сложно'}
                                        </span>
                                        <span className="question-mode">{MODE_LABELS[q.mode]}</span>
                                    </div>

                                    <p>{q.question_text}</p>

                                    <div className="question-actions">
                                        <Button small onClick={() => handleEdit(q)}>Ред.</Button>
                                        <Button small onClick={() => handleToggleVisibility(q)}>
                                            {q.is_active ? "Скрыть" : "Показать"}
                                        </Button>
                                        <Button small variant="danger" onClick={() => handleDelete(q.id)}>
                                            Удалить
                                        </Button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
}