import { MapContainer, TileLayer } from "react-leaflet";
import { useEffect, useState, useMemo } from "react";
import { useGameStore } from "../../store/gameStore";

import ClickLayer from "./layers/ClickLayer";
import CountryLayer from "./layers/CountryLayer";
import ResultLayer from "./layers/ResultLayer";
import MarkersLayer from "./layers/MarkersLayer";

import { loadCountriesGeoJSON, findCountryAtPoint } from "../../utils/geoUtils";

export default function MapView({
    correctPoint,
    showResult,
    mode,
    targetCode,
    selectedPoint,
}) {
    const storeSelected = useGameStore((s) => s.selectedPoint);
    const selected = selectedPoint || storeSelected;

    const [geoData, setGeoData] = useState(null);

    useEffect(() => {
        loadCountriesGeoJSON()
            .then(setGeoData)
            .catch(console.error);
    }, []);

    const selectedCountry = useMemo(() => {
        if (!selected || !geoData) return null;

        const country = findCountryAtPoint(
            selected.lat,
            selected.lng
        );

        return country?.code || null;
    }, [selected, geoData]);

    const isCorrect =
        mode === "countries"
            ? selectedCountry === targetCode
            : null;

    return (
        <MapContainer
            center={[20, 0]}
            zoom={2}
            style={{
                height: "500px",
                borderRadius: "16px",
            }}
        >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

            <ClickLayer disabled={showResult} />

            <CountryLayer
                geoData={geoData}
                targetCode={targetCode}
                selectedCountry={selectedCountry}
                isCorrect={isCorrect}
                mode={mode}
            />

            <ResultLayer
                selected={selected}
                correctPoint={correctPoint}
                mode={mode}
                showResult={showResult}
            />

            <MarkersLayer
                selected={selected}
                showResult={showResult}
                mode={mode}
                isCorrect={isCorrect}
            />
        </MapContainer>
    );
}