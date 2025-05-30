import h3
from modules.region_to_hexagons.common_types import H3CellId

def get_h3_cells_from_polygon(
    polygon: list[tuple[float, float]], resolution: int
) -> list[H3CellId]:
    shape = h3.LatLngPoly(polygon)

    string_cells = h3.h3shape_to_cells(shape, resolution)
    cells = [h3.str_to_int(cell) for cell in string_cells]

    return cells


def get_h3_cells_from_multipolygon(
    multipolygon: list[list[tuple[float, float]]], resolution: int
) -> list[H3CellId]:
    h3_polygons = [h3.LatLngPoly(polygon) for polygon in multipolygon]
    shape = h3.LatLngMultiPoly(*h3_polygons)
    string_cells = h3.h3shape_to_cells(shape, resolution)
    cells = [h3.str_to_int(cell) for cell in string_cells]
    return cells
