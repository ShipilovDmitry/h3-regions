from modules.parse_utils import get_name_from_geojson, read_tsv
from modules.wbk_utils import get_polygon_from_wkb, from_wkb
from shapely.geometry import Polygon, MultiPolygon
from modules.draw_polygon_h3 import draw_polygon
from pathlib import Path
import pytest

ASSETS_DIR = Path(__file__).parent / "assets"


@pytest.mark.parametrize(("asset_name", "expected"), [("attributes.geojson", "Москва")])
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
    with pytest.raises(ValueError):
        polygon = get_polygon_from_wkb(wkb)


# for drawing polygon uncomment last line in function
def test_draw_polygon() -> None:
    huata_asset = "huata_polygon.txt"
    asset_path = ASSETS_DIR / huata_asset
    with open(asset_path, "r") as f:
        wkb = f.read()

    polygon = get_polygon_from_wkb(wkb)

    list_of_tuples = [(coordinate.lat, coordinate.lon) for coordinate in polygon]
    # draw_polygon(list_of_tuples)


def test_draw_multipolygon() -> None:
    moscow_asset = "moscow_multipolygon.txt"
    asset_path = ASSETS_DIR / moscow_asset
    with open(asset_path, "r") as f:
        wkb = f.read()
    multipolygon = from_wkb(wkb)

    polygons = list(multipolygon.geoms)
    h3_polygons = [[(y, x) for x, y in polygon.exterior.coords] for polygon in polygons]

    # draw_polygon(h3_polygons , True)
