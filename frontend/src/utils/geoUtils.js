import * as turf from "@turf/turf";

const GEOJSON_URL = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson";

let countriesGeoJSON = null;

export async function loadCountriesGeoJSON() {
  if (countriesGeoJSON) {
    return countriesGeoJSON;
  }

  try {
    const response = await fetch(GEOJSON_URL);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    countriesGeoJSON = await response.json();
    return countriesGeoJSON;
  } catch (error) {
    console.error("Error loading GeoJSON:", error);
    throw error;
  }
}

export function isPointInCountry(lat, lng, countryCode) {
  if (!countriesGeoJSON || !countryCode) {
    return false;
  }

  const point = turf.point([lng, lat]);

  for (const feature of countriesGeoJSON.features) {
    const isoCode = feature.properties.ISO_A3;
    
    if (isoCode === countryCode || isoCode === countryCode.toUpperCase()) {
      return turf.booleanPointInPolygon(point, feature.geometry);
    }
  }

  return false;
}

export function findCountryAtPoint(lat, lng) {
  if (!countriesGeoJSON) {
    return null;
  }

  const point = turf.point([lng, lat]);

  for (const feature of countriesGeoJSON.features) {
    if (turf.booleanPointInPolygon(point, feature.geometry)) {
      return {
        code: feature.properties.ISO_A3,
        name: feature.properties.ADMIN || feature.properties.NAME_EN || "Unknown",
      };
    }
  }

  return null;
}

export async function checkAnswerWithBorder(
  selectedLat,
  selectedLng,
  correctCountryCode
) {
  await loadCountriesGeoJSON();

  const inCorrectCountry = isPointInCountry(selectedLat, selectedLng, correctCountryCode);

  if (inCorrectCountry) {
    return {
      isCorrect: true,
      message: "Точно в стране!",
      bonus: true,
    };
  }

  const countryAtPoint = findCountryAtPoint(selectedLat, selectedLng);

  return {
    isCorrect: false,
    message: countryAtPoint
      ? `Вы выбрали ${countryAtPoint.name}, а нужно было ${correctCountryCode}`
      : "Точка не находится в пределах какой-либо страны",
    countryFound: countryAtPoint?.name || null,
    bonus: false,
  };
}