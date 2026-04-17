import {BrowserRouter, Routes, Route} from "react-router-dom";
import Layout from "../components/layout/Layout";
import Home from "../pages/Home";
import DifficultyScreen from "../pages/DifficultyScreen";
import Game from "../pages/Game";
import Results from "../pages/Results";
import NotFound from "../pages/NotFound";
import AdminLogin from "../pages/AdminLogin";
import AdminDashboard from "../pages/AdminDashboard";
import Leaderboard from "../pages/Leaderboard";

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<Layout/>}>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/difficulty" element={<DifficultyScreen/>}/>
                    <Route path="/game" element={<Game/>}/>
                    <Route path="/results" element={<Results/>}/>
                    <Route path="/leaderboard" element={<Leaderboard/>}/>
                    <Route path="/admin/login" element={<AdminLogin/>}/>
                    <Route path="/admin" element={<AdminDashboard/>}/>
                    <Route path="*" element={<NotFound/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    );
}