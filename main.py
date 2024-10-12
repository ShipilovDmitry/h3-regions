from pathlib import Path

from modules.parse_tsv import read_tsv
from modules.wbk_utils import get_polygon_from_wkb
from modules.h3_utils import get_h3_cells_from_polygon
from modules.serializer import cell_ids_to_bytes
from modules.sql_writer import SQLWriter, SQLRegion


PATH_TO_FILE: str = "/Users/d.shipilov/vkmaps/h3-regions/town-city-village.jsonl"
FILENAME = Path(PATH_TO_FILE).stem

H3_RESOLUTION: int = 10


def main():
    sql_writer = SQLWriter(FILENAME)

    for region_from_json in read_tsv(PATH_TO_FILE):
        blob_of_h3_indexes: bytes = cell_ids_to_bytes(
            get_h3_cells_from_polygon(
                get_polygon_from_wkb(region_from_json.wkb), H3_RESOLUTION
            )
        )

        sql_region = SQLRegion(
            region_from_json.id, region_from_json.name, blob_of_h3_indexes
        )
        sql_writer.insert_region(sql_region)
    

if __name__ == "__main__":
    main()
