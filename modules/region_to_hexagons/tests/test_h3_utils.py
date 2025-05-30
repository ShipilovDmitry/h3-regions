import pytest
from modules.h3_utils import get_h3_cells_from_polygon
from modules.common_types import Coordinate


@pytest.mark.parametrize(
    "polygon, resolution, expected_result",
    [
        (
            [
                Coordinate(lat=37.7749, lon=-122.4194),
                Coordinate(lat=37.7813, lon=-122.4124),
                Coordinate(lat=37.7757, lon=-122.4056),
                Coordinate(lat=37.7749, lon=-122.4194),
            ],
            9,
            [
                617700169965371391,
                617700169958031359,
                617700169961701375,
                617700169964847103,
                617700169961963519,
            ],
        )
    ],
)
def test_get_h3_cells_from_polygon(polygon, resolution, expected_result):
    # call the function with the input values
    prepared_polygon = [(coordinate.lat, coordinate.lon) for coordinate in polygon]
    result = get_h3_cells_from_polygon(prepared_polygon, resolution)

    # check the output against the expected result
    assert result == expected_result
