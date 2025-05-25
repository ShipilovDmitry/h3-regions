from modules.elevation.elevation import get_hexagon, triangulate_hexagon, calculate_triangle_centroid

def test_triangulation():
    id = '8711aa7aaffffff'
    hexagon = get_hexagon(id)
    print(hexagon)


    triangles = triangulate_hexagon(hexagon)
    print(triangles)

    centers = [calculate_triangle_centroid(trianlge) for trianlge in triangles]
    print(centers)
