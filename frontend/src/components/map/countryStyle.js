export function getCountryStyle({
    feature,
    targetCode,
    selectedCountry,
    isCorrect,
    mode,
}) {
    const iso = feature.properties.ISO_A3;

    if (mode !== "countries") {
        return {
            fillColor: "#e0e0e0",
            fillOpacity: 0.05,
            weight: 0.5,
            color: "#666",
        };
    }

    const isTarget = iso === targetCode;
    const isSelected = iso === selectedCountry;

    // Всегда показываем целевую страну
    if (isTarget) {
        return {
            fillColor: "#22c55e", // зеленая
            color: "#22c55e",
            weight: 3,
            fillOpacity: 0.5,
        };
    }

    // Если игрок выбрал страну - показываем её
    if (isSelected) {
        return {
            fillColor: isCorrect ? "#22c55e" : "#ef4444", // зеленая если правильно, красная если нет
            color: isCorrect ? "#22c55e" : "#ef4444",
            weight: 3,
            fillOpacity: 0.4,
        };
    }

    // Остальные страны - серые
    return {
        fillColor: "#e0e0e0",
        color: "#666",
        weight: 0.5,
        fillOpacity: 0.05,
    };
}