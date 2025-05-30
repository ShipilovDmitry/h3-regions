from pathlib import Path
import os
import multiprocessing
from modules.region_to_hexagons.parse_utils import read_tsv, read_tsv_queue, get_name_from_geojson
from modules.region_to_hexagons.wbk_utils import get_h3_cells_from_wkb
from modules.region_to_hexagons.serializer import cell_ids_to_bytes
from modules.region_to_hexagons.sql_writer import (
    SQLWriter,
    SQLWriterCellsCount,
    SQLRegion,
    SQLRegionCellsCount,
)
from functools import partial


def sql_insert(filename: str, rows: multiprocessing.Queue) -> None:
    sql_writer = SQLWriter(filename)
    while True:
        row = rows.get()
        if row is None:  # wait for Poison pill
            print("sql_insert: Poison pill")
            del sql_writer
            break
        sql_writer.insert_region(row)


def h3_long_operation(h3_resolution: int, region_from_json: str) -> SQLRegion | None:
    try:
        blob_of_h3_indexes: bytes = cell_ids_to_bytes(
            get_h3_cells_from_wkb(region_from_json.wkb, h3_resolution)
        )
    except Exception as e:
        print(e)
        return None

    region_name = get_name_from_geojson(region_from_json.attributes_geojson)
    sql_region = SQLRegion(region_from_json.id, region_name, blob_of_h3_indexes)
    return sql_region


def h3_long_opearation_count_cells(region_from_json: str) -> SQLRegionCellsCount:
    ...
    # try:
    #     cells = get_h3_cells_from_wkb(region_from_json.wkb, H3_RESOLUTION)
    # except Exception as e:
    #     print(e)
    #     return None

    # region_name = get_name_from_geojson(region_from_json.attributes_geojson)
    # sql_region = SQLRegionCellsCount(region_from_json.id, region_name, len(cells))
    # return sql_region


def multiprocessing_run(db_name:str, path_to_regions_json: str, h3_resolution: int):
    # Create the queues
    lines_from_file = multiprocessing.Queue()
    sql_rows = multiprocessing.Queue()
    

    p1 = multiprocessing.Process(target=sql_insert, args=(db_name, sql_rows,))
    p2 = multiprocessing.Process(
        target=read_tsv_queue, args=(path_to_regions_json, lines_from_file)
    )

    p1.start()
    p2.start()

    # Create a process pool and map the process_data function to the input queue
    with multiprocessing.Pool() as pool:
        for sql_row in pool.imap_unordered(
            partial(h3_long_operation, h3_resolution), iter(lines_from_file.get, None)
        ):
            sql_rows.put(sql_row)

    # Signal for the end of the processing
    print("multiprocessing_main: Poison pill")
    sql_rows.put(None)

    # Wait for the processes to finish
    p1.join()
    p2.join()

def remove_db(db_name: str):
    db_path = Path(__file__).parent.parent.parent / f"{db_name}.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def create_region_hexagons_db(path_to_regions_json: str, h3_resolution: int):
    db_name = f"{Path(path_to_regions_json).stem}-{h3_resolution}"
    remove_db(db_name)

    multiprocessing_run(db_name, path_to_regions_json, h3_resolution)
