from typing import Iterator
from modules.common_types import RegionFromJson
import pandas as pd
import io
import json
import multiprocessing


def read_tsv(file_path: str) -> Iterator[RegionFromJson]:
    with open(file_path, "r") as file:
        for line in file:
            df = pd.read_csv(io.StringIO(line), sep="\t")
            id, attributes_geojson, wbk = df.columns[0], df.columns[1], df.columns[2]
            yield RegionFromJson(id, attributes_geojson, wbk)


def read_tsv_queue(file_path: str, queue: multiprocessing.Queue) -> None:
    with open(file_path, "r") as file:
        for line in file:
            df = pd.read_csv(io.StringIO(line), sep="\t")
            id, attributes_geojson, wbk = df.columns[0], df.columns[1], df.columns[2]
            queue.put(RegionFromJson(id, attributes_geojson, wbk))
    queue.put(None)


def get_name_from_geojson(geojson: str) -> str:
    data = json.loads(geojson)
    df = pd.DataFrame(data["properties"])

    result = str()
    default: pd.DataFrame = df["locales"]["default"]

    if "address" in default:
        address: pd.DataFrame = df["locales"]["default"]["address"]
        if "country" in address:
            result = str(address["country"])

        if "region" in address:
            result = ",".join([result, address["region"]])
    result = default["name"] if result == "" else ",".join([result, default["name"]])
    return result
