"""Objetos y efectos: monedas, cristal de poder, puerta de meta y partículas."""

import pygame

from src.settings import TILE, GRAVITY_FALL, CRYSTAL_SPEED, DEATH_Y, TEXT_COLOR, SHADOW_COLOR
from src.systems.physics import apply_gravity
from src.systems.collision import move_and_collide
from src.systems.assets import Images


class Coin:
    """Moneda colocada en el nivel."""

    def __init__(self, col, row):
        self.rect = pygame.Rect(0, 0, 18, 26)
        self.rect.center = (col * TILE + TILE // 2, row * TILE + TILE // 2)
        self.collected = False

    def draw(self, screen, camera, frame):
        if self.collected:
            return

        image = Images.get(f"coin_{(frame // 8) % 4 + 1}")
        screen.blit(image, image.get_rect(center=camera.apply(self.rect).center))


class Crystal:
    """Cristal de poder: sale del bloque, avanza y cae como un objeto físico."""

    def __init__(self, tile_rect):
        self.rect = pygame.Rect(0, 0, 28, 28)
        self.rect.midbottom = tile_rect.midbottom
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.target_bottom = tile_rect.top

        self.velocity_x = CRYSTAL_SPEED
        self.velocity_y = 0.0
        self.on_ground = False
        self.ground = None

        self.emerging = True
        self.collected = False
        self.removed = False

    def update(self, world):
        if self.emerging:
            self.pos_y -= 1
            self.rect.y = round(self.pos_y)

            if self.rect.bottom <= self.target_bottom:
                self.rect.bottom = self.target_bottom
                self.pos_y = float(self.rect.y)
                self.emerging = False
            return

        apply_gravity(self, GRAVITY_FALL)
        result = move_and_collide(self, world)

        if result.hit_wall:
            self.velocity_x = -self.velocity_x

        if self.rect.top > DEATH_Y:
            self.removed = True

    def draw(self, screen, camera, frame):
        image = Images.get("crystal")
        screen.blit(image, image.get_rect(midbottom=camera.apply(self.rect).midbottom))


class Door:
    """Meta del nivel."""

    def __init__(self, col, row):
        # Ocupa 1 celda de ancho y 2 de alto, apoyada en la fila indicada
        self.rect = pygame.Rect(col * TILE, (row - 1) * TILE, TILE, TILE * 2)
        self.trigger = self.rect.inflate(-14, 0)

    def draw(self, screen, camera, frame):
        image = Images.get("door")
        screen.blit(image, image.get_rect(midbottom=camera.apply(self.rect).midbottom))


# ---------------------------------------------------------------
# Efectos (sin colisión)
# ---------------------------------------------------------------
class CoinPop:
    """Moneda que salta de un bloque bonus."""

    def __init__(self, tile_rect):
        self.x = tile_rect.centerx
        self.y = float(tile_rect.top - 10)
        self.velocity_y = -9.0
        self.timer = 0
        self.done = False

    def update(self):
        self.timer += 1
        self.velocity_y += 0.6
        self.y += self.velocity_y

        if self.timer > 30:
            self.done = True

    def draw(self, screen, camera, frame):
        image = Images.get(f"coin_{(frame // 3) % 4 + 1}")
        x = self.x - camera.offset_x
        screen.blit(image, image.get_rect(center=(x, int(self.y))))


class Debris:
    """Trozo de ladrillo roto."""

    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.done = False

    def update(self):
        self.velocity_y += 0.6
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y > DEATH_Y:
            self.done = True

    def draw(self, screen, camera, frame):
        image = Images.get("debris")
        screen.blit(image, (int(self.x - camera.offset_x), int(self.y)))


class ScorePopup:
    """Texto flotante con los puntos ganados."""

    _font = None

    def __init__(self, x, y, text):
        if ScorePopup._font is None:
            ScorePopup._font = pygame.font.Font(None, 26)

        self.x = x
        self.y = float(y)
        self.text = text
        self.timer = 0
        self.done = False

    def update(self):
        self.timer += 1
        self.y -= 1.0

        if self.timer > 45:
            self.done = True

    def draw(self, screen, camera, frame):
        x = self.x - camera.offset_x
        shadow = self._font.render(self.text, True, SHADOW_COLOR)
        surface = self._font.render(self.text, True, TEXT_COLOR)
        rect = surface.get_rect(center=(x, int(self.y)))
        screen.blit(shadow, rect.move(2, 2))
        screen.blit(surface, rect)
