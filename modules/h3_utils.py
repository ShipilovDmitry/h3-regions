import h3
from modules.common_types import H3CellId, Coordinate


def get_h3_cells_from_polygon(
    polygon: list[Coordinate], resolution: int
) -> list[H3CellId]:
    h3_formatted_polygon = [(coord.lat, coord.lon) for coord in polygon]
    shape = h3.LatLngPoly(h3_formatted_polygon)

    string_cells = h3.h3shape_to_cells(shape, resolution)
    cells = [h3.str_to_int(cell) for cell in string_cells]

    return cells


def get_h3_cells_from_multipolygon(
    multipolygon: list[list[Coordinate]], resolution: int
) -> list[H3CellId]:
    formatted_multipolygon = [
        [(coord.lat, coord.lon) for coord in polygon] for polygon in multipolygon
    ]
    h3_multipolygon = [h3.LatLngPoly(polygon) for polygon in formatted_multipolygon]
    shape = h3.LatLngMultiPoly(*h3_multipolygon)
    string_cells = h3.h3shape_to_cells(shape, resolution)
    cells = [h3.str_to_int(cell) for cell in string_cells]
    return cells
