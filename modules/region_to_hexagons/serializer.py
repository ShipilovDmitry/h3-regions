from modules.region_to_hexagons.common_types import H3CellId
import struct


def cell_ids_to_bytes(cell_ids: list[H3CellId]) -> bytes:
    byte_array = bytearray()
    try:
        byte_array.extend(struct.pack("Q", len(cell_ids)))

        for cell_id in cell_ids:
            byte_array.extend(struct.pack("Q", cell_id))
    except struct.error as e:
        raise ValueError("Error serializing blob.\n") from e
    return bytes(byte_array)


def bytes_to_cell_ids(blob: bytes) -> list[H3CellId]:
    try:
        cell_ids = []
        num_cells = struct.unpack("Q", blob[0:8])[0]
        for i in range(num_cells):
            cell_ids.append(struct.unpack("Q", blob[8 + i * 8 : 16 + i * 8])[0])
    except struct.error as e:
        raise ValueError("Error deserializing blob.\n" + str(e)) from e
    return cell_ids
