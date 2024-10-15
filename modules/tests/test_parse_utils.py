from modules.parse_utils import get_name_from_geojson, read_tsv
import h3
from modules.wbk_utils import get_h3_cells_from_wkb, from_wkb
from shapely.geometry import MultiPolygon
from pathlib import Path
import pytest

ASSETS_DIR = Path(__file__).parent / "assets"


@pytest.mark.parametrize(
    ("asset_name", "expected"), [("attributes.geojson", "Россия,Москва,Москва")]
)
def test_get_name_from_geojson(asset_name: str, expected: str):
    asset_path = ASSETS_DIR / asset_name
    with open(asset_path, "r") as f:
        geojson = f.read()

    result = get_name_from_geojson(geojson)
    assert result == expected


def test_multipolygon_moscow() -> None:
    moscow_asset = "moscow_multipolygon.txt"
    asset_path = ASSETS_DIR / moscow_asset
    with open(asset_path, "r") as f:
        wkb = f.read()
    coordinates = get_h3_cells_from_wkb(wkb, 10)
    coordinates = [h3.int_to_str(coordinate) for coordinate in coordinates]
    # draw_cells(coordinates)


# for drawing polygon uncomment last line in function
def test_draw_polygon() -> None:
    huata_asset = "huata_polygon.txt"
    asset_path = ASSETS_DIR / huata_asset
    with open(asset_path, "r") as f:
        wkb = f.read()

    coordinates = get_h3_cells_from_wkb(wkb, 10)

    # draw_cells(polygon)


def test_draw_multipolygon() -> None:
    moscow_asset = "moscow_multipolygon.txt"
    asset_path = ASSETS_DIR / moscow_asset
    with open(asset_path, "r") as f:
        wkb = f.read()
    multipolygon: MultiPolygon = from_wkb(wkb)

    h3_polygons = [
        [(y, x) for x, y in polygon.exterior.coords] for polygon in multipolygon.geoms
    ]

    # draw_mulitpolygon(h3_polygons)
