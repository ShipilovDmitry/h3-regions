from shapely import from_wkb, Polygon, MultiPolygon
from modules.region_to_hexagons.h3_utils import get_h3_cells_from_polygon, get_h3_cells_from_multipolygon
from modules.region_to_hexagons.common_types import  H3CellId


def process_multipolygon(
    wkb_multipolygon: MultiPolygon, resolution: int
) -> list[H3CellId]:
    formatted_multipolygon = []
    for polygon in wkb_multipolygon.geoms:
        formatted_polygon = [(y, x) for x, y in polygon.exterior.coords]
        formatted_multipolygon.append(formatted_polygon)
    return get_h3_cells_from_multipolygon(formatted_multipolygon, resolution)


def get_h3_cells_from_wkb(wkb: str, resolution: int) -> list[H3CellId]:
    wkb_region: Polygon | MultiPolygon = from_wkb(wkb)

    if wkb_region.geom_type == "Polygon":
        formatted_polygon = [(y, x) for x, y in wkb_region.exterior.coords]
        return get_h3_cells_from_polygon(formatted_polygon, resolution)

    if wkb_region.geom_type == "MultiPolygon":
        return process_multipolygon(wkb_region, resolution)

    raise ValueError(
        "Invalid WKB data. Expected a Polygon."
    )
