from shapely import from_wkb, Polygon
from modules.common_types import Coordinate


def get_polygon_from_wkb(wkb: str) -> list[Coordinate]:
    polygon: Polygon = from_wkb(wkb)
    if polygon.geom_type != "Polygon":
        raise ValueError("Invalid WKB data. Expected a Polygon.")

    coords = polygon.exterior.coords
    coordinates = [Coordinate(lat=y, lon=x) for x, y in coords]
    return coordinates
