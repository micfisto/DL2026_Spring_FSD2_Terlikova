import { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import "./AdminLogin.css";

export default function AdminLogin() {
    const navigate = useNavigate();
    const { login, isAuthenticated, loading, error, clearError } = useAuthStore();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    if (isAuthenticated) {
        return <Navigate to="/admin" replace />;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        clearError();

        const success = await login(username, password);
        if (success) {
            navigate("/admin");
        }
    };

    return (
        <div className="admin-login">
            <div className="admin-login-container">

                <div className="admin-login-header">
                    <h1>🔐 Админ-панель</h1>
                    <p>Вход для администратора</p>
                </div>

                <form className="admin-login-form" onSubmit={handleSubmit}>

                    <div className="form-group">
                        <label>Имя пользователя</label>
                        <Input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Введите логин"
                            required
                            autoComplete="username"
                        />
                    </div>

                    <div className="form-group">
                        <label>Пароль</label>
                        <Input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Введите пароль"
                            required
                            autoComplete="current-password"
                        />
                    </div>

                    {error && (
                        <div className="error-message">
                            {error}
                        </div>
                    )}

                    <Button
                        type="submit"
                        loading={loading}
                        disabled={loading}
                        className="login-button"
                    >
                        Войти
                    </Button>
                </form>

                <div className="admin-login-footer">
                    <a href="/">← Вернуться на главную</a>
                </div>

            </div>
        </div>
    );
}