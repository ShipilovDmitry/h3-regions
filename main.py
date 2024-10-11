from pathlib import Path

PATH_TO_FILE = "/Users/d.shipilov/vkmaps/h3-regions/town-city-village.jsonl"
FILENAME = Path(PATH_TO_FILE).stem

print(FILENAME)
