import { useMapEvents } from "react-leaflet";
import { useGameStore } from "../../../store/gameStore";

export default function ClickLayer({ disabled }) {
    const setSelectedPoint = useGameStore((s) => s.setSelectedPoint);

    useMapEvents({
        click: (e) => {
            if (!disabled) {
                setSelectedPoint(e.latlng);
            }
        },
    });

    return null;
}