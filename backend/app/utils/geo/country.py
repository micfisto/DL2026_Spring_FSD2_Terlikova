import json
import urllib.request

_geo_cache = None


def _load_geojson():
    global _geo_cache

    if _geo_cache is None:
        url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
        with urllib.request.urlopen(url, timeout=30) as r:
            _geo_cache = json.loads(r.read().decode())

    return _geo_cache


def point_in_country(lat, lng, country_code):
    geo = _load_geojson()

    target = None
    for f in geo["features"]:
        iso = f["properties"].get("ISO_A3")
        if iso == country_code or iso == country_code.upper():
            target = f
            break

    if not target:
        return False

    return _point_in_geometry(lat, lng, target["geometry"])


def _point_in_geometry(lat, lng, geometry):
    if geometry["type"] == "Polygon":
        polygons = [geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        polygons = geometry["coordinates"]
    else:
        return False

    for polygon in polygons:
        for ring in polygon:
            if _point_in_ring(lat, lng, ring):
                return True

    return False


def _point_in_ring(lat, lng, ring):
    inside = False
    n = len(ring)

    for i in range(n):
        j = (i + 1) % n

        xi, yi = ring[i]
        xj, yj = ring[j]

        if ((yi > lng) != (yj > lng)) and (
            lat < (xj - xi) * (lng - yi) / (yj - yi) + xi
        ):
            inside = not inside

    return inside