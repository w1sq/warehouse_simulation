import json
import random
from dataclasses import dataclass
from typing import List
import string


@dataclass
class Tile:
    """Class representing tile of warehouse"""

    row: int
    letter: str
    info: dict = None

    def __eq__(self, other) -> bool:
        if isinstance(other, Tile):
            if self.row == other.row and self.letter == other.letter:
                return True
        return False


def read_scheme(filename="warehouse.json") -> dict[dict]:
    """Read warehouse scheme from file."""
    with open(filename, "r", encoding="utf-8") as file:
        file_scheme = json.loads(file.read())
        python_scheme = {int(key): value for key, value in file_scheme.items()}
        return python_scheme


class Greedy:
    """Class represting greedy algorithm that processes warehouse schemas"""

    def __init__(self, warehouse_sheme: dict[dict], robots_amount: int = 1):
        self._warehouse_sheme = warehouse_sheme
        self._robots_amount = robots_amount

    def _get_colored_tiles(self, color: str) -> List[Tile]:
        colored_tiles: List[Tile] = []
        for row_id, row in self._warehouse_sheme.items():
            for tile_letter, tile_info in row.items():
                if tile_info["color"] == color:
                    tile = Tile(row=row_id, letter=tile_letter, info=tile_info)
                    colored_tiles.append(tile)
        return colored_tiles

    def _color_tiles(self, bare_tiles: List[Tile]) -> List[Tile]:
        for row_id, row in self._warehouse_sheme.items():
            for tile_letter, tile_info in row.items():
                for bare_tile in bare_tiles:
                    if row_id == bare_tile.row and tile_letter == bare_tile.letter:
                        bare_tile.info = tile_info
        return bare_tiles

    def _get_neighbour_tiles(self, tile: Tile) -> List[Tile]:
        alphabet = string.ascii_lowercase
        print(tile)
        possible_rows = tile.row + 1, tile.row - 1
        tile_letter_index = alphabet.index(tile.letter)
        possible_letters_indexes = tile_letter_index + 1, tile_letter_index - 1
        bare_tiles = []
        for possible_row in possible_rows:
            if possible_row in range(0, len(self._warehouse_sheme.keys())):
                bare_tiles.append(Tile(row=possible_row, letter=tile.letter))
        for possible_letter_index in possible_letters_indexes:
            if possible_letter_index in range(
                0, len([self._warehouse_sheme.values()][0])
            ):
                bare_tiles.append(
                    Tile(row=tile.row, letter=alphabet[possible_letter_index])
                )
        colored_tiles = self._color_tiles(bare_tiles)
        return colored_tiles

    def _create_route(self, start: Tile, finish: Tile):
        current_tile = start
        while current_tile != finish:
            neighbour_tiles = self._get_neighbour_tiles(current_tile)
            print(neighbour_tiles)
            break

    def process_scheme(self):
        start_tile = random.choice(self._get_colored_tiles("green"))
        target_tile = random.choice(self._get_colored_tiles("yellow"))
        self._create_route(start_tile, target_tile)


if __name__ == "__main__":
    warehouse_sheme = read_scheme("warehouse.json")
    greedy = Greedy(warehouse_sheme)
    greedy.process_scheme()
