import { Marker } from "react-leaflet";
import {
    defaultIcon,
    redIcon,
    goldIcon,
} from "../icons/mapIcons";

export default function MarkersLayer({
    selected,
    showResult,
    mode,
    isCorrect,
}) {
    if (!selected) return null;

    return (
        <Marker
            position={selected}
            icon={
                mode === "countries" && showResult
                    ? isCorrect
                        ? goldIcon
                        : redIcon
                    : defaultIcon
            }
        />
    );
}