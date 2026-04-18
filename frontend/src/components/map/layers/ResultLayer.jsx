import { Marker, Polyline, Popup } from "react-leaflet";
import { greenIcon } from "../icons";

export default function ResultLayer({
    selected,
    correctPoint,
    showResult,
}) {
    if (!showResult) return null;

    const line =
        selected && correctPoint
            ? [
                  [selected.lat, selected.lng],
                  [correctPoint.lat, correctPoint.lng],
              ]
            : [];

    return (
        <>
            {correctPoint && (
                <Marker position={correctPoint} icon={greenIcon}>
                    <Popup>Правильный ответ</Popup>
                </Marker>
            )}

            {line.length > 0 && (
                <Polyline
                    positions={line}
                    color="#667eea"
                    weight={2}
                    opacity={0.7}
                    dashArray="5, 10"
                />
            )}
        </>
    );
}