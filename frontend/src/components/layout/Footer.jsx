import { Link } from "react-router-dom";
import "./Footer.css";

export default function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                <p className="footer-copy">
                    © 2026 GeoQuiz. <Link to="/admin/login">Admin</Link>
                </p>
            </div>
        </footer>
    );
}