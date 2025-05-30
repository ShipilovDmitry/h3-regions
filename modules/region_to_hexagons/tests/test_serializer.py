from modules.region_to_hexagons.serializer import cell_ids_to_bytes, bytes_to_cell_ids
import h3
from modules.region_to_hexagons.draw_polygon_h3 import draw_cells
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
    # Moscow 71000000002585F7
    # Kazan 710000000027FD5C
    # Russia 71000000001B82D6
    db_path = "/Users/d.shipilov/workspace/blink/h3-regions/only-moscow-5.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    result: bytes = cursor.execute(
        "SELECT hexagons FROM regions WHERE id = '71000000002585F7'"
    ).fetchall()[0][0]
    cells = bytes_to_cell_ids(result)

    str_cells = [h3.int_to_str(cell) for cell in cells]
    # with open("cells-russia-7.txt", 'w') as f:
    #     for cell in str_cells:
    #         f.write(cell + '\n')

    draw_cells(str_cells)
