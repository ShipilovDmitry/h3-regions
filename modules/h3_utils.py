import h3
from modules.common_types import H3CellId, Coordinate


def get_h3_cells_from_polygon(
    polygon: list[Coordinate], resolution: int
) -> list[H3CellId]:
    list_of_tuples = [(coord.lat, coord.lon) for coord in polygon]
    shape = h3.LatLngPoly(list_of_tuples)

    string_cells = h3.h3shape_to_cells(shape, resolution)
    cells = [h3.str_to_int(cell) for cell in string_cells]

    return cells
