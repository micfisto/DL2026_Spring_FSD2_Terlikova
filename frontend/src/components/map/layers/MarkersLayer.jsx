import { Marker } from "react-leaflet";
import {
    defaultIcon,
    orangeIcon,
    redIcon,
    goldIcon,
} from "../icons";

export default function MarkersLayer({
    selected,
    showResult,
    mode,
    isCorrect,
}) {
    if (!selected) return null;

    const getIcon = () => {
        if (!showResult) {
            return orangeIcon;
        }
        
        if (mode === "countries") {
            return isCorrect ? goldIcon : redIcon;
        }
        
        return defaultIcon;
    };

    return (
        <Marker
            position={selected}
            icon={getIcon()}
        />
    );
}