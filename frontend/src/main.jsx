import './index.css'
import "leaflet/dist/leaflet.css";
import AppRouter from "./routes/AppRouter.jsx";
import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/game.css";
import "./styles/global.css";


ReactDOM.createRoot(document.getElementById("root")).render(
    <AppRouter/>
);