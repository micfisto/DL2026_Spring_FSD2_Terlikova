import { GeoJSON } from "react-leaflet";
import { useGameStore } from "../../../store/gameStore";
import { getCountryStyle } from "../countryStyle";

export default function CountryLayer({
    geoData,
    targetCode,
    selectedCountry,
    isCorrect,
    mode,
}) {
    const setSelectedPoint = useGameStore((s) => s.setSelectedPoint);

    if (!geoData) return null;

    const handleEachFeature = (feature, layer) => {
        layer.on({
            click: () => {
                const bounds = layer.getBounds();
                const center = bounds.getCenter();
                setSelectedPoint(center);
            },
        });
    };

    return (
        <GeoJSON
            data={geoData}
            style={(feature) =>
                getCountryStyle({
                    feature,
                    targetCode,
                    selectedCountry,
                    isCorrect,
                    mode,
                })
            }
            onEachFeature={handleEachFeature}
        />
    );
}