from pathlib import Path
import os

from modules.parse_utils import read_tsv, get_name_from_geojson
from modules.wbk_utils import get_polygon_from_wkb
from modules.h3_utils import get_h3_cells_from_polygon
from modules.serializer import cell_ids_to_bytes
from modules.sql_writer import SQLWriter, SQLRegion


PATH_TO_FILE: str = "/Users/d.shipilov/vkmaps/h3-regions/town-city-village.jsonl"
FILENAME = Path(PATH_TO_FILE).stem

H3_RESOLUTION: int = 10


def main():
    db_path = Path(__file__).parent / f"{FILENAME}.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    sql_writer = SQLWriter(FILENAME)

    for i, region_from_json in enumerate(read_tsv(PATH_TO_FILE)):
        try:
            blob_of_h3_indexes: bytes = cell_ids_to_bytes(
                get_h3_cells_from_polygon(
                    get_polygon_from_wkb(region_from_json.wkb), H3_RESOLUTION
                )
            )
        except Exception as e:
            print(e)
            continue

        region_name = get_name_from_geojson(region_from_json.attributes_geojson)

        sql_region = SQLRegion(region_from_json.id, region_name, blob_of_h3_indexes)

        sql_writer.insert_region(sql_region)


if __name__ == "__main__":
    main()
