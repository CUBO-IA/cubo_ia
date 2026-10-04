"""Herramienta para diseñar niveles de forma legible.

El mapa es una cuadrícula de LEVEL_ROWS filas. Cada carácter es una celda:

    X  suelo                 S  bloque de piedra (indestructible)
    B  ladrillo (se rompe si el jugador es grande)
    ?  bloque bonus con moneda
    N  bloque bonus con varias monedas
    M  bloque bonus con cristal de poder
    C  moneda                E  slime (se puede pisar)
    K  erizo (púas)          D  puerta de meta
    @  inicio del jugador

Fila 0 = arriba, fila 14 = abajo. El suelo normal ocupa las filas 13 y 14.
"""

from src.settings import LEVEL_ROWS

GROUND_ROW = 13


class LevelBuilder:
    def __init__(self, width, name, theme):
        self.width = width
        self.name = name
        self.theme = theme
        self.grid = [[" "] * width for _ in range(LEVEL_ROWS)]
        self.moving = []

    # -----------------------------------------------------------
    # Primitivas
    # -----------------------------------------------------------
    def set(self, col, row, char):
        if 0 <= col < self.width and 0 <= row < LEVEL_ROWS:
            self.grid[row][col] = char
        return self

    def ground(self, start, end, top=GROUND_ROW):
        """Suelo sólido desde la columna start hasta end (incluida)."""
        for col in range(start, end + 1):
            for row in range(top, LEVEL_ROWS):
                self.set(col, row, "X")
        return self

    def row(self, start, row, text):
        """Escribe una secuencia horizontal, p.ej. 'B?B?B'."""
        for i, char in enumerate(text):
            if char != ".":
                self.set(start + i, row, char)
        return self

    def column(self, col, top, bottom, char="S"):
        for row in range(top, bottom + 1):
            self.set(col, row, char)
        return self

    def stairs_up(self, start, height, base=GROUND_ROW - 1):
        """Escalera ascendente de piedra hacia la derecha."""
        for step in range(height):
            self.column(start + step, base - step, base)
        return self

    def stairs_down(self, start, height, base=GROUND_ROW - 1):
        for step in range(height):
            self.column(start + step, base - (height - 1 - step), base)
        return self

    def coins(self, start, row, count, gap=1):
        for i in range(count):
            self.set(start + i * gap, row, "C")
        return self

    def enemy(self, col, kind="E", row=GROUND_ROW - 1):
        return self.set(col, row, kind)

    def start(self, col, row=GROUND_ROW - 1):
        return self.set(col, row, "@")

    def door(self, col, row=GROUND_ROW - 1):
        return self.set(col, row, "D")

    def moving_platform(self, col, row, width_tiles=3, axis="x", distance=4, speed=1.2):
        self.moving.append((col, row, width_tiles, axis, distance, speed))
        return self

    # -----------------------------------------------------------
    def build(self):
        return {
            "name": self.name,
            "theme": self.theme,
            "rows": ["".join(row) for row in self.grid],
            "moving": list(self.moving),
        }
