from shapely import from_wkb, Polygon

def get_polygon_from_wkb(wkb: str) -> list[dict[str, float]]:
    polygon: Polygon = from_wkb(wkb)
    if polygon.geom_type != 'Polygon':
        raise ValueError("Invalid WKB data. Expected a Polygon.")

    coords = polygon.exterior.coords
    lat_lon_coords = [{"lat":y, "lon":x} for x, y in coords]
    return lat_lon_coords
