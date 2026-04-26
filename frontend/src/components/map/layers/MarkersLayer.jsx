import { Marker } from "react-leaflet";
import { orangeIcon, redIcon, goldIcon } from "../icons";

export default function MarkersLayer({
    selected,
    correctPoint,
    showResult,
}) {
    if (!selected) return null;

    const isCorrect =
        showResult &&
        correctPoint &&
        Math.abs(selected.lat - correctPoint.lat) < 0.0001 &&
        Math.abs(selected.lng - correctPoint.lng) < 0.0001;

    return (
        <>
            <Marker
                position={selected}
                icon={showResult ? (isCorrect ? goldIcon : redIcon) : orangeIcon}
            />

            {showResult && correctPoint && (
                <Marker position={correctPoint} icon={goldIcon} />
            )}
        </>
    );
}