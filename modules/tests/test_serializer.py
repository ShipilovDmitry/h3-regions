from modules.serializer import cell_ids_to_bytes, bytes_to_cell_ids
import h3
from modules.draw_polygon_h3 import draw_cells
import sqlite3


def test_cell_ids_to_bytes():
    # define a sample list of H3CellId values
    cell_ids = [617700169965371391, 617700169958031359, 617700169961701375]

    # call the function with the sample H3CellId values
    result = cell_ids_to_bytes(cell_ids)

    # check the output against the expected result
    expected_result = b"\x03\x00\x00\x00\x00\x00\x00\x00\xff\xff{(\x08\x83\x92\x08\xff\xff\x0b(\x08\x83\x92\x08\xff\xffC(\x08\x83\x92\x08"
    assert result == expected_result


def test_bytes_to_cell_ids():
    # define a sample blob of bytes
    blob = b"\x03\x00\x00\x00\x00\x00\x00\x00\xff\xff{(\x08\x83\x92\x08\xff\xff\x0b(\x08\x83\x92\x08\xff\xffC(\x08\x83\x92\x08"

    # call the function with the sample blob of bytes
    result = bytes_to_cell_ids(blob)

    # check the output against the expected result
    expected_result = [617700169965371391, 617700169958031359, 617700169961701375]
    assert result == expected_result


def test_draw_cells_from_bytes():
    return
    db_path = "/Users/d.shipilov/vkmaps/h3-regions/artifacts/town-city-village-10-level.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    result: bytes = cursor.execute(
        "SELECT hexagons FROM regions WHERE id = '71000000017CE494'"
    ).fetchall()[0][0]
    cells = bytes_to_cell_ids(result)

    str_cells = [h3.int_to_str(cell) for cell in cells]

    draw_cells(str_cells)
