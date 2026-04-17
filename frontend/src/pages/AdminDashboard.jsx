import { useState, useEffect } from "react";
import { useNavigate, Navigate } from "react-router-dom";
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

const MODES = ["capitals", "countries", "landmarks"];
const TARGET_TYPES = ["country", "capital", "landmark"];
const DIFFICULTIES = ["easy", "medium", "hard"];

const emptyForm = {
    question_text: "",
    mode: "capitals",
    target_name: "",
    target_type: "country",
    correct_lat: "",
    correct_lng: "",
    difficulty: "medium",
    is_active: true,
};

export default function AdminDashboard() {
    const navigate = useNavigate();
    const { token, isAuthenticated, logout } = useAuthStore();

    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const [form, setForm] = useState(emptyForm);
    const [editingId, setEditingId] = useState(null);
    const [saving, setSaving] = useState(false);

    if (!isAuthenticated || !token) {
        return <Navigate to="/admin/login" replace />;
    }

    const fetchQuestions = async () => {
        try {
            setLoading(true);
            const data = await getQuestions(token);
            setQuestions(data || []);
        } catch (err) {
            setError(err.message);
            if (err.message.includes("401")) {
                logout();
                navigate("/admin/login");
            }
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchQuestions();
    }, [token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);
        setSaving(true);

        try {
            const payload = {
                ...form,
                correct_lat: parseFloat(form.correct_lat),
                correct_lng: parseFloat(form.correct_lng),
            };

            if (editingId) {
                await updateQuestion(token, editingId, payload);
                setSuccess("Вопрос обновлён");
            } else {
                await createQuestion(token, payload);
                setSuccess("Вопрос добавлен");
            }

            setForm(emptyForm);
            setEditingId(null);
            fetchQuestions();
        } catch (err) {
            setError(err.message);
        } finally {
            setSaving(false);
        }
    };

    const handleEdit = (q) => {
        setForm({
            question_text: q.question_text,
            mode: q.mode,
            target_name: q.target_name,
            target_type: q.target_type,
            correct_lat: String(q.correct_lat),
            correct_lng: String(q.correct_lng),
            difficulty: q.difficulty,
            is_active: q.is_active,
        });
        setEditingId(q.id);
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

    return (
        <div className="admin-dashboard">
            <div className="admin-header">
                <h1>Управление вопросами</h1>
                <Button onClick={logout}>Выйти</Button>
            </div>

            <div className="admin-content">
                <div className="admin-form-section">
                    <h2>{editingId ? "Редактирование" : "Добавить вопрос"}</h2>

                    <form onSubmit={handleSubmit} className="question-form">
                        <Input
                            name="question_text"
                            value={form.question_text}
                            onChange={(e) =>
                                setForm({ ...form, question_text: e.target.value })
                            }
                            placeholder="Текст вопроса"
                            required
                        />

                        <Input
                            name="target_name"
                            value={form.target_name}
                            onChange={(e) =>
                                setForm({ ...form, target_name: e.target.value })
                            }
                            placeholder="Цель"
                            required
                        />

                        <div className="form-row">
                            <Input
                                name="correct_lat"
                                type="number"
                                value={form.correct_lat}
                                onChange={(e) =>
                                    setForm({ ...form, correct_lat: e.target.value })
                                }
                                placeholder="lat"
                            />
                            <Input
                                name="correct_lng"
                                type="number"
                                value={form.correct_lng}
                                onChange={(e) =>
                                    setForm({ ...form, correct_lng: e.target.value })
                                }
                                placeholder="lng"
                            />
                        </div>

                        {error && <div className="error-message">{error}</div>}
                        {success && <div className="success-message">{success}</div>}

                        <Button type="submit" disabled={saving}>
                            {editingId ? "Сохранить" : "Добавить"}
                        </Button>
                    </form>
                </div>

                <div className="admin-questions-section">
                    <h2>Вопросы ({questions.length})</h2>

                    {loading ? (
                        <div>Загрузка...</div>
                    ) : (
                        questions.map((q) => (
                            <div key={q.id} className="question-card">
                                <p>{q.question_text}</p>

                                <Button onClick={() => handleEdit(q)}>Edit</Button>
                                <Button onClick={() => handleToggleVisibility(q)}>
                                    {q.is_active ? "Hide" : "Show"}
                                </Button>
                                <Button onClick={() => handleDelete(q.id)}>
                                    Delete
                                </Button>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}