from dataclasses import dataclass

@dataclass
class Region:
    id: str
    attributes_geojson: str
    wkb: str
