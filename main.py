# from modules.elevation.elevation import async_average_russia_heights
from modules.region_to_hexagons.api import create_region_hexagons_db


# async def main():
#     await async_average_russia_heights('/Users/d.shipilov/workspace/blink/h3-regions/cells-russia-7.txt')

def main():
    h3_resolution = 5
    create_region_hexagons_db("/Users/d.shipilov/workspace/blink/h3-regions/only-moscow.jsonl", h3_resolution)



# if __name__ == "__main__":
#     asyncio.run(main())

if __name__ == "__main__":
    main()
