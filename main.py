from pathlib import Path
import os
import multiprocessing

from modules.parse_utils import read_tsv, read_tsv_queue, get_name_from_geojson
from modules.wbk_utils import get_h3_cells_from_wkb
from modules.serializer import cell_ids_to_bytes
from modules.sql_writer import SQLWriter, SQLWriterCellsCount, SQLRegion, SQLRegionCellsCount


PATH_TO_FILE: str = "/Users/d.shipilov/vkmaps/h3-regions/town-city-village.jsonl"
FILENAME = Path(PATH_TO_FILE).stem

H3_RESOLUTION: int = 11


def sql_insert(rows: multiprocessing.Queue) -> None:
    sql_writer = SQLWriterCellsCount(FILENAME)
    while True:
        row = rows.get()
        if row is None: # wait for Poison pill
            del sql_writer
            break
        sql_writer.insert_region(row)


def h3_long_operation(region_from_json: str) -> SQLRegion | None:
    try:
        blob_of_h3_indexes: bytes = cell_ids_to_bytes(
            get_h3_cells_from_wkb(region_from_json.wkb, H3_RESOLUTION)
        )
    except Exception as e:
        print(e)
        return None

    region_name = get_name_from_geojson(region_from_json.attributes_geojson)
    sql_region = SQLRegion(region_from_json.id, region_name, blob_of_h3_indexes)
    return sql_region


def h3_long_opearation_count_cells(region_from_json: str) -> SQLRegionCellsCount:
    try:
        cells = get_h3_cells_from_wkb(region_from_json.wkb, H3_RESOLUTION)
    except Exception as e:
        print(e)
        return None

    region_name = get_name_from_geojson(region_from_json.attributes_geojson)
    sql_region = SQLRegionCellsCount(region_from_json.id, region_name, len(cells))
    return sql_region


def multiprocessing_main():
    # Create the queues
    lines_from_file = multiprocessing.Queue()
    sql_rows = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=sql_insert, args=(sql_rows,))
    p2 = multiprocessing.Process(
        target=read_tsv_queue, args=(PATH_TO_FILE, lines_from_file)
    )

    p1.start()
    p2.start()

    # Create a process pool and map the process_data function to the input queue
    with multiprocessing.Pool() as pool:
        for sql_row in pool.imap_unordered(
            h3_long_opearation_count_cells, iter(lines_from_file.get, None)
        ):
            sql_rows.put(sql_row)

    # Signal for the end of the processing
    sql_rows.put(None)

    # Wait for the processes to finish
    p1.join()
    p2.join()


def sync_main():
    sql_writer = SQLWriter(FILENAME)

    for region_from_json in read_tsv(PATH_TO_FILE):
        try:
            blob_of_h3_indexes: bytes = cell_ids_to_bytes(
                get_h3_cells_from_wkb(region_from_json.wkb, H3_RESOLUTION)
            )
        except Exception as e:
            print(e)
            continue

        region_name = get_name_from_geojson(region_from_json.attributes_geojson)

        sql_region = SQLRegion(region_from_json.id, region_name, blob_of_h3_indexes)

        sql_writer.insert_region(sql_region)



def remove_db():
    db_path = Path(__file__).parent / f"{FILENAME}.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def main():
    remove_db()

    # sync_main()
    multiprocessing_main()


if __name__ == "__main__":
    main()
