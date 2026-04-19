import './index.css'
import "leaflet/dist/leaflet.css";
import AppRouter from "./routes/AppRouter.jsx";
import React from "react";
import ReactDOM from "react-dom/client";


ReactDOM.createRoot(document.getElementById("root")).render(
    <AppRouter/>
);