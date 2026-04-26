import json
import os
from shapely.geometry import shape, Point

_geo_cache = None
_country_index = None


def normalize_code(code: str):
    if not code:
        return None

    code = code.strip().upper()

    if code in ["-99", "XX", "NULL", "N/A", "NONE"]:
        return None

    return code


def point_in_country(lat, lng, country_code):
    index = _get_index()

    code = normalize_code(country_code)
    if not code:
        print("INVALID CODE INPUT:", country_code)
        return False

    geometry = index.get(code)

    if not geometry:
        print("NOT FOUND CODE:", code)
        return False

    point = Point(lng, lat)
    polygon = shape(geometry)

    return polygon.covers(point)


def _load_geojson():
    global _geo_cache

    if _geo_cache is None:
        path = os.path.join(
            os.path.dirname(__file__),
            "../../data/countries.geojson"
        )
        path = os.path.abspath(path)

        print("LOADING GEOJSON FROM:", path)

        with open(path, "r", encoding="utf-8") as f:
            _geo_cache = json.load(f)

    return _geo_cache


def _build_index():
    geo = _load_geojson()
    index = {}

    for feature in geo.get("features", []):
        props = feature.get("properties", {})

        # разные возможные поля (ВАЖНО)
        candidates = [
            props.get("ISO_A3"),
            props.get("iso_a3"),
            props.get("ISO3166-1-Alpha-3"),
            props.get("ADM0_A3"),
        ]

        code = None
        for c in candidates:
            c = normalize_code(c)
            if c:
                code = c
                break

        if not code:
            continue

        index[code] = feature["geometry"]

    print("INDEX SIZE:", len(index))
    print("SAMPLE KEYS:", list(index.keys())[:20])

    return index


def _get_index():
    global _country_index

    if _country_index is None:
        _country_index = _build_index()

    return _country_index