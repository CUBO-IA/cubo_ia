"""Convierte el mapa de texto en objetos del mundo y ofrece consultas rápidas."""

from src.settings import TILE, LEVEL_ROWS, WIDTH
from src.entities.platform import Tile, MovingPlatform
from src.entities.enemy import ENEMY_TYPES
from src.entities.item import Coin, Door


TILE_CHARS = {
    "X": ("ground", None),
    "S": ("stone", None),
    "B": ("brick", None),
    "?": ("bonus", "coin"),
    "N": ("bonus", "multi"),
    "M": ("bonus", "crystal"),
}


class Level:
    def __init__(self, data):
        self.name = data["name"]
        self.theme = data["theme"]

        rows = data["rows"]
        self.cols = max(len(r) for r in rows)
        self.width = self.cols * TILE
        self.height = LEVEL_ROWS * TILE

        self.tiles = [[None] * self.cols for _ in range(LEVEL_ROWS)]
        self.coins = []
        self.enemies = []
        self.door = None
        self.start = (2 * TILE, (LEVEL_ROWS - 2) * TILE)

        for row, line in enumerate(rows):
            for col, char in enumerate(line):
                self._spawn(char, col, row)

        self.moving_platforms = [MovingPlatform(*spec) for spec in data.get("moving", [])]

        self._mark_ground_tops()

    def _spawn(self, char, col, row):
        if char in TILE_CHARS:
            kind, content = TILE_CHARS[char]
            self.tiles[row][col] = Tile(col, row, kind, content, self.theme)

        elif char == "C":
            self.coins.append(Coin(col, row))

        elif char in ENEMY_TYPES:
            self.enemies.append(ENEMY_TYPES[char](col, row))

        elif char == "D":
            self.door = Door(col, row)

        elif char == "@":
            self.start = (col * TILE + TILE // 2, (row + 1) * TILE)

    def _mark_ground_tops(self):
        for row in range(LEVEL_ROWS):
            for col in range(self.cols):
                tile = self.tiles[row][col]
                if tile is not None and tile.kind == "ground":
                    above = self.tile_at(col, row - 1)
                    tile.top_variant = above is None or above.kind != "ground"

    # -----------------------------------------------------------
    # Consultas
    # -----------------------------------------------------------
    def tile_at(self, col, row):
        if 0 <= row < LEVEL_ROWS and 0 <= col < self.cols:
            return self.tiles[row][col]
        return None

    def remove_tile(self, tile):
        self.tiles[tile.row][tile.col] = None

    def solids_near(self, rect):
        """Sólidos que podrían tocar rect (búsqueda por celdas, O(1))."""
        col_start = max(0, rect.left // TILE - 1)
        col_end = min(self.cols - 1, rect.right // TILE + 1)
        row_start = max(0, rect.top // TILE - 1)
        row_end = min(LEVEL_ROWS - 1, rect.bottom // TILE + 1)

        found = []

        for row in range(row_start, row_end + 1):
            line = self.tiles[row]
            for col in range(col_start, col_end + 1):
                tile = line[col]
                if tile is not None and tile.solid:
                    found.append(tile)

        if self.moving_platforms:
            area = rect.inflate(TILE * 2, TILE * 2)
            for platform in self.moving_platforms:
                if area.colliderect(platform.rect):
                    found.append(platform)

        return found

    def visible_tiles(self, camera):
        col_start = max(0, int(camera.offset_x) // TILE - 1)
        col_end = min(self.cols - 1, (int(camera.offset_x) + WIDTH) // TILE + 1)

        for row in range(LEVEL_ROWS):
            line = self.tiles[row]
            for col in range(col_start, col_end + 1):
                if line[col] is not None:
                    yield line[col]
