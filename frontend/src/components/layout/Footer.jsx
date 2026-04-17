import "./Footer.css";

export default function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-brand">
                    <span className="footer-icon">🌍</span>
                    <span className="footer-text">GeoQuiz</span>
                </div>
                <p className="footer-copy">
                    © 2026 GeoQuiz. Тест на знание географии.
                </p>
            </div>
        </footer>
    );
}