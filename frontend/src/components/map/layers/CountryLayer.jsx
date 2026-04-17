import { GeoJSON } from "react-leaflet";
import { getCountryStyle } from "../countryStyle";

export default function CountryLayer({
    geoData,
    targetCode,
    selectedCountry,
    isCorrect,
    mode,
}) {
    if (!geoData) return null;

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
        />
    );
}