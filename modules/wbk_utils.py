from shapely import from_wkb, Polygon, MultiPolygon
from modules.common_types import Coordinate


def process_polygon(polygon: Polygon) -> list[Coordinate]:
    coords = polygon.exterior.coords
    coordinates = [Coordinate(lat=y, lon=x) for x, y in coords]
    return coordinates


def process_multipolygon(multipolygon: MultiPolygon) -> list[Coordinate]:
    coordinates = []
    for polygon in multipolygon.geoms:
        coordinates.extend(process_polygon(polygon))
    return coordinates


def get_polygon_from_wkb(wkb: str) -> list[Coordinate]:
    p: Polygon | MultiPolygon = from_wkb(wkb)

    if p.geom_type == "Polygon":
        return process_polygon(p)

    if p.geom_type == "MultiPolygon":
        return process_multipolygon(p)

    raise ValueError(
        f"Invalid WKB data. Expected a Polygon. Geometry type is: {p.geom_type}"
    )
