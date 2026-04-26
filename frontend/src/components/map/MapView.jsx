import {MapContainer, TileLayer} from "react-leaflet";
import {useEffect, useState} from "react";
import {useGameStore} from "../../store/gameStore";
import CountryLayer from "./layers/CountryLayer";
import ClickLayer from "./layers/ClickLayer";
import ResultLayer from "./layers/ResultLayer";
import MarkersLayer from "./layers/MarkersLayer";

import {loadCountriesGeoJSON} from "../../utils/geoUtils";

export default function MapView({
                                    correctPoint,
                                    showResult,
                                    mode,
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

    return (
        <MapContainer
            center={[20, 0]}
            zoom={2}
            style={{
                height: "500px",
                borderRadius: "16px",
            }}
        >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>

            <ClickLayer disabled={showResult}/>

            <CountryLayer geoData={geoData}/>

            <ResultLayer
                selected={selected}
                correctPoint={correctPoint}
                mode={mode}
                showResult={showResult}
            />

            <MarkersLayer
                selected={selected}
                correctPoint={correctPoint}
                showResult={showResult}
            />
        </MapContainer>
    );
}