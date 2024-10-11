from typing import Iterator
from common_types import Region
import pandas as pd
import io

def read_tsv(file_path) -> Iterator[Region]:
    with open(file_path, 'r') as file:
        for line in file:
            df = pd.read_csv(io.StringIO(line), sep='\t')
            yield Region(df.columns[0], df.columns[1], df.columns[2])
