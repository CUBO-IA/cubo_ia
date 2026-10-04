"""Lista ordenada de niveles. Para añadir uno: crear level_N.py con build()."""

from src.levels import level_1, level_2, level_3

LEVELS = [
    level_1.build,
    level_2.build,
    level_3.build,
]

LEVEL_TITLES = [
    "Pradera",
    "Cueva",
    "Fortaleza",
]
