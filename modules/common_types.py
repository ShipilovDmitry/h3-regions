from dataclasses import dataclass

from typing import TypeAlias


@dataclass
class RegionFromJson:
    id: str
    attributes_geojson: str
    wkb: str


H3CellId: TypeAlias = int


@dataclass
class Coordinate:
    lat: float
    lon: float


class HexagonsBLOB:
    amount: int
    hexagons: list[H3CellId]
