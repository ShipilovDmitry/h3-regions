from typing import Iterator
from modules.common_types import RegionFromJson
import pandas as pd
import io
import json


def read_tsv(file_path: str) -> Iterator[RegionFromJson]:
    with open(file_path, "r") as file:
        for line in file:
            df = pd.read_csv(io.StringIO(line), sep="\t")
            id, attributes_geojson, wbk = df.columns[0], df.columns[1], df.columns[2]
            yield RegionFromJson(id, attributes_geojson, wbk)

def get_name_from_geojson(geojson: str) -> str:
    data = json.loads(geojson)
    df = pd.DataFrame(data["properties"])
    return df["locales"]["en"]["name"]
