from modules.elevation.elevation import (
    get_hexagon,
    triangulate_hexagon,
    calculate_triangle_centroid,
)

from modules.elevation.api import fetch_elevation
import time
import csv


def test_triangulation():
    with open('russia_mean_heigts_7_level.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['CellId', 'AverageHeight'])
        start_time = time.time()
        id = "8711aa7aaffffff"
        hexagon = get_hexagon(id)

        triangles = triangulate_hexagon(hexagon)

        centers = [calculate_triangle_centroid(trianlge) for trianlge in triangles]
        heights = fetch_elevation(centers)
        average_height = sum(heights) / len(heights)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function execution time: {execution_time} seconds")
        writer.writerow([id, average_height])
