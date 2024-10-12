from modules.serializer import cell_ids_to_bytes, bytes_to_cell_ids

def test_cell_ids_to_bytes():
    # define a sample list of H3CellId values
    cell_ids = [617700169965371391, 617700169958031359, 617700169961701375]

    # call the function with the sample H3CellId values
    result = cell_ids_to_bytes(cell_ids)

    # check the output against the expected result
    expected_result = b'\x03\x00\x00\x00\x00\x00\x00\x00\xff\xff{(\x08\x83\x92\x08\xff\xff\x0b(\x08\x83\x92\x08\xff\xffC(\x08\x83\x92\x08'
    assert result == expected_result

def test_bytes_to_cell_ids():
    # define a sample blob of bytes
    blob = b'\x03\x00\x00\x00\x00\x00\x00\x00\xff\xff{(\x08\x83\x92\x08\xff\xff\x0b(\x08\x83\x92\x08\xff\xffC(\x08\x83\x92\x08'

    # call the function with the sample blob of bytes
    result = bytes_to_cell_ids(blob)

    # check the output against the expected result
    expected_result = [617700169965371391, 617700169958031359, 617700169961701375]
    assert result == expected_result