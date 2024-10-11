from dataclasses import dataclass
from typing import Iterator
import pandas as pd
import io


@dataclass
class Region:
    id: str
    attributes_geojson: str
    wkb: str

def read_tsv(file_path) -> Iterator[Region]:
    with open(file_path, 'r') as file:
        for line in file:
            df = pd.read_csv(io.StringIO(line), sep='\t')
            yield Region(df.columns[0], df.columns[1], df.columns[2])
