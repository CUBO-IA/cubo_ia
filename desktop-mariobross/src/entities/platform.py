"""Bloques del mapa y plataformas móviles."""

import math

import pygame

from src.settings import TILE
from src.systems.assets import Images


SOLID_KINDS = {"ground", "stone", "brick", "bonus", "used"}


class Tile:
    """Un bloque del mapa (suelo, piedra, ladrillo, bloque bonus...)."""

    one_way = False

    def __init__(self, col, row, kind, content=None, theme="pradera"):
        self.col = col
        self.row = row
        self.kind = kind
        self.content = content          # "coin", "multi", "crystal" o None
        self.theme = theme
        self.multi_left = 10 if content == "multi" else 0
        self.multi_timer = 0

        self.rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
        self.bump_timer = 0
        self.top_variant = True         # lo fija el nivel (suelo con borde)

    @property
    def prev_top(self):
        return self.rect.top

    @property
    def solid(self):
        return self.kind in SOLID_KINDS

    def bump(self):
        self.bump_timer = 12

    def update(self):
        if self.bump_timer > 0:
            self.bump_timer -= 1

    def _image_name(self, frame):
        if self.kind == "ground":
            part = "top" if self.top_variant else "fill"
            return f"ground_{part}_{self.theme}"

        if self.kind == "bonus":
            return f"bonus_{(frame // 10) % 4 if (frame // 10) % 4 < 3 else 1}"

        return self.kind

    def draw(self, screen, camera, frame):
        offset = 0

        if self.bump_timer > 0:
            offset = -int(math.sin((12 - self.bump_timer) / 12 * math.pi) * 10)

        image = Images.get(self._image_name(frame))
        screen.blit(image, camera.apply(self.rect).move(0, offset))


class MovingPlatform:
    """Plataforma atravesable desde abajo que se mueve en X o en Y."""

    one_way = True
    kind = "moving"

    def __init__(self, col, row, width_tiles, axis, distance_tiles, speed):
        self.rect = pygame.Rect(col * TILE, row * TILE, width_tiles * TILE, TILE // 2)
        self.axis = axis
        self.start = self.rect.x if axis == "x" else self.rect.y
        self.distance = distance_tiles * TILE
        self.speed = speed
        self.pos = float(self.start)
        self.direction = 1

        self.dx = 0
        self.dy = 0
        self._prev_top = self.rect.top

    @property
    def prev_top(self):
        return self._prev_top

    def update(self):
        self._prev_top = self.rect.top
        old_x, old_y = self.rect.x, self.rect.y

        self.pos += self.speed * self.direction

        if self.pos > self.start + self.distance:
            self.pos = self.start + self.distance
            self.direction = -1
        elif self.pos < self.start:
            self.pos = self.start
            self.direction = 1

        if self.axis == "x":
            self.rect.x = round(self.pos)
        else:
            self.rect.y = round(self.pos)

        self.dx = self.rect.x - old_x
        self.dy = self.rect.y - old_y

    def draw(self, screen, camera, frame):
        image = Images.get("platform")
        draw_rect = camera.apply(self.rect)

        for i in range(self.rect.width // TILE):
            screen.blit(image, (draw_rect.x + i * TILE, draw_rect.y))
