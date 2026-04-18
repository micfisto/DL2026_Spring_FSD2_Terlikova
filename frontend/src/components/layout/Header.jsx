import { Link } from "react-router-dom";
import "./Header.css";

export default function Header() {
    return (
        <header className="header">
            <div className="header-content">
                <Link to="/" className="logo">
                    <span className="logo-icon">🌍</span>
                    <span className="logo-text">GeoQuiz</span>
                </Link>
                <nav className="nav">
                    <Link to="/leaderboard" className="nav-link">Рейтинг</Link>
                </nav>
            </div>
        </header>
    );
}