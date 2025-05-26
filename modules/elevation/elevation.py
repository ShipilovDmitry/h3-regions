# Read cell ids line by line
# Get lat-lon vertecies for cell
# Triangulate cell with 6 triangules
# Get centers of 6 triangules
# Go to /elevation for each triangle center asyncronously
# Average elevation value
# Write to the file
from typing import Iterator
from modules.common_types import Coordinate
from modules.elevation.api import fetch_elevation, async_fetch_elevation
import h3
from dataclasses import dataclass
import math
import csv
import aiohttp


@dataclass
class Hexagon:
    center: Coordinate
    vertices: list[Coordinate]


@dataclass
class Triangle:
    first: Coordinate
    second: Coordinate
    third: Coordinate


def read_cell(filename: str) -> Iterator[str]:
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            if i % 10000 == 0:
                print(f"Processed {i} rows")
            yield line


def get_hexagon(cell_id: str) -> Hexagon:
    tuple_of_tuples = h3.cell_to_boundary(cell_id)
    vertices: list[Coordinate] = []
    for pair in tuple_of_tuples:
        vertices.append(Coordinate(pair[0], pair[1]))
    center_lat, center_lon = h3.cell_to_latlng(cell_id)
    return Hexagon(Coordinate(center_lat, center_lon), vertices)


def triangulate_hexagon(hexagon: Hexagon) -> list[Triangle]:
    triangles: list[Triangle] = []
    for i in range(len(hexagon.vertices)):
        triangle = Triangle(
            hexagon.center,
            hexagon.vertices[i],
            hexagon.vertices[(i + 1) % len(hexagon.vertices)],
        )
        triangles.append(triangle)
    return triangles


def calculate_triangle_centroid(triangle: Triangle) -> Coordinate:
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2, lat3, lon3 = map(
        math.radians,
        [
            triangle.first.lat,
            triangle.first.lon,
            triangle.second.lat,
            triangle.second.lon,
            triangle.third.lat,
            triangle.third.lon,
        ],
    )

    # Calculate the centroid using the average of the vertices
    x = (
        math.cos(lat1) * math.cos(lon1)
        + math.cos(lat2) * math.cos(lon2)
        + math.cos(lat3) * math.cos(lon3)
    ) / 3
    y = (
        math.cos(lat1) * math.sin(lon1)
        + math.cos(lat2) * math.sin(lon2)
        + math.cos(lat3) * math.sin(lon3)
    ) / 3
    z = (math.sin(lat1) + math.sin(lat2) + math.sin(lat3)) / 3

    # Convert the centroid back to latitude and longitude
    lon = math.atan2(y, x)
    hyp = math.sqrt(x * x + y * y)
    lat = math.atan2(z, hyp)

    # Convert radians back to degrees
    lat, lon = map(math.degrees, [lat, lon])

    return Coordinate(lat, lon)

def average_russia_heights(path_to_cells: str) -> None:
    with open('average_russia_7.csv', mode='w', newline='') as average_heights:
        writer = csv.writer(average_heights)
        writer.writerow(['CellId, AverageHeight'])
        for cell_id in read_cell(path_to_cells):
            hexagon = get_hexagon(cell_id)
            triangles = triangulate_hexagon(hexagon)
            centers = [calculate_triangle_centroid(trianlge) for trianlge in triangles]
            heights = fetch_elevation(centers)
            if heights is None or len(heights) == 0:
                continue
            average_height = sum(heights) / len(heights)
            cell_id_no_n = cell_id[:-1]
            writer.writerow([cell_id_no_n, average_height])


async def async_average_russia_heights(path_to_cells:str) -> None:
    with open('average_russia_7.csv', mode='w', newline='') as average_heights:
        writer = csv.writer(average_heights)
        writer.writerow(['CellId, AverageHeight'])
        async with aiohttp.ClientSession() as session:
            for cell_id in read_cell(path_to_cells):
                hexagon = get_hexagon(cell_id)
                triangles = triangulate_hexagon(hexagon)
                centers = [calculate_triangle_centroid(trianlge) for trianlge in triangles]
                heights = await async_fetch_elevation(session, centers)
                if heights is None or len(heights) == 0:
                    continue
                average_height = sum(heights) / len(heights)
                cell_id_no_n = cell_id[:-1]
                writer.writerow([cell_id_no_n, average_height])
