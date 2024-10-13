from modules.parse_utils import get_name_from_geojson
from pathlib import Path
import pytest


@pytest.mark.parametrize(("asset_name", "expected"), [("attributes.geojson", "Москва")])
def test_get_name_from_geojson(asset_name: str, expected: str):
    asset_path = Path(__file__).parent / "assets" / asset_name
    with open(asset_path, "r") as f:
        geojson = f.read()

    result = get_name_from_geojson(geojson)
    assert result == expected
