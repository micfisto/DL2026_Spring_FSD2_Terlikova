import Header from "./Header";
import Footer from "./Footer";
import "./Layout.css";
import {Outlet} from "react-router-dom";

export default function Layout() {
    return (
        <div className="layout">
            <Header/>

            <main className="main-content">
                <div className="page-container">
                    <Outlet/>
                </div>
            </main>

            <Footer/>
        </div>
    );
}