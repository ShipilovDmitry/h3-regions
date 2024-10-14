from modules.parse_utils import get_name_from_geojson, read_tsv
from modules.wbk_utils import get_polygon_from_wkb
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
    moscow_asset = "moscow.tsv"
    asset_path = ASSETS_DIR / moscow_asset
    for region in read_tsv(asset_path):
        with pytest.raises(ValueError):
            polygon = get_polygon_from_wkb(region.wkb)


def test_draw_polygon() -> None:
    # test for drawing testing
    # remove return for drawing
    return
    draw_polygon()