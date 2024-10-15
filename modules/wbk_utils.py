from shapely import from_wkb, Polygon, MultiPolygon
from modules.h3_utils import get_h3_cells_from_polygon, get_h3_cells_from_multipolygon
from modules.common_types import Coordinate, H3CellId


def process_polygon(polygon: Polygon, resolution: int) -> list[H3CellId]:
    coordinates = [Coordinate(lat=y, lon=x) for x, y in polygon.exterior.coords]
    return get_h3_cells_from_polygon(coordinates, resolution)


def process_multipolygon(multipolygon: MultiPolygon, resolution: int) -> list[H3CellId]:
    p = []
    for polygon in multipolygon.geoms:
        coordinates = [Coordinate(lat=y, lon=x) for x, y in polygon.exterior.coords]
        p.append(coordinates)
    return get_h3_cells_from_multipolygon(p, resolution)


def get_h3_cells_from_wkb(wkb: str, resolution: int) -> list[H3CellId]:
    p: Polygon | MultiPolygon = from_wkb(wkb)

    if p.geom_type == "Polygon":
        return process_polygon(p, resolution)

    if p.geom_type == "MultiPolygon":
        return process_multipolygon(p, resolution)

    raise ValueError(
        f"Invalid WKB data. Expected a Polygon. Geometry type is: {p.geom_type}"
    )
