from modules.elevation.elevation import (
    get_hexagon,
    triangulate_hexagon,
    calculate_triangle_centroid,
)

from modules.elevation.api import fetch_elevation
import time


def test_triangulation():
    start_time = time.time()
    id = "8711aa7aaffffff"
    hexagon = get_hexagon(id)

    triangles = triangulate_hexagon(hexagon)

    centers = [calculate_triangle_centroid(trianlge) for trianlge in triangles]
    heights = fetch_elevation(centers)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Function execution time: {execution_time} seconds")
