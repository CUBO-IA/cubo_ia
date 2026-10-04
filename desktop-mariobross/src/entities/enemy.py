"""Enemigos.

Slime  : camina, se puede aplastar saltándole encima.
Erizo  : camina, tiene púas -> no se puede pisar; da media vuelta en los bordes.
Ambos mueren si el jugador golpea el bloque sobre el que están.
"""

import pygame

from src.settings import (
    TILE,
    GRAVITY_FALL,
    SLIME_SPEED,
    SPIKY_SPEED,
    DEATH_Y,
    MAX_FALL_SPEED,
)
from src.systems.physics import apply_gravity, move_x, move_y
from src.systems.collision import move_and_collide, ground_ahead
from src.systems.assets import Images


class Enemy:
    stompable = True
    turns_at_edges = False
    speed = 1.0
    size = (30, 28)
    sprite = "slime"

    def __init__(self, col, row):
        self.rect = pygame.Rect(0, 0, *self.size)
        self.rect.midbottom = (col * TILE + TILE // 2, (row + 1) * TILE)
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        self.velocity_x = -self.speed
        self.velocity_y = 0.0
        self.on_ground = False
        self.ground = None

        self.active = False
        self.alive = True
        self.squashed_timer = 0     # > 0: aplastado, desaparece al llegar a 0
        self.knocked = False        # derribado: cae boca arriba sin colisiones
        self.removed = False
        self.anim = 0

    @property
    def harmful(self):
        return self.alive and not self.knocked and self.squashed_timer == 0

    # -----------------------------------------------------------
    def stomp(self):
        self.alive = False
        self.squashed_timer = 30
        self.velocity_x = 0

    def knock(self, direction=1):
        self.alive = False
        self.knocked = True
        self.velocity_y = -7
        self.velocity_x = 1.5 * direction

    # -----------------------------------------------------------
    def update(self, world):
        if self.removed or not self.active:
            return

        self.anim += 1

        if self.squashed_timer > 0:
            self.squashed_timer -= 1
            if self.squashed_timer == 0:
                self.removed = True
            return

        if self.knocked:
            self.velocity_y = min(self.velocity_y + 0.5, MAX_FALL_SPEED)
            move_x(self, self.velocity_x)
            move_y(self, self.velocity_y)
        else:
            if self.turns_at_edges and self.on_ground:
                direction = 1 if self.velocity_x > 0 else -1
                if not ground_ahead(self, world, direction):
                    self.velocity_x = -self.velocity_x

            apply_gravity(self, GRAVITY_FALL)
            result = move_and_collide(self, world)

            if result.hit_wall:
                self.velocity_x = -self.velocity_x

            # No salir por el borde izquierdo del nivel
            if self.rect.left <= 0:
                self.rect.left = 0
                self.pos_x = 0.0
                self.velocity_x = self.speed

        if self.rect.top > DEATH_Y:
            self.removed = True

    # -----------------------------------------------------------
    def draw(self, screen, camera):
        if self.removed:
            return

        if self.squashed_timer > 0:
            name = f"{self.sprite}_flat"
        else:
            name = f"{self.sprite}_{(self.anim // 12) % 2 + 1}"

        image = Images.get(name, flip=self.velocity_x > 0)

        if self.knocked:
            image = pygame.transform.flip(image, False, True)

        draw_rect = camera.apply(self.rect)
        screen.blit(image, image.get_rect(midbottom=draw_rect.midbottom))


class Slime(Enemy):
    stompable = True
    turns_at_edges = False
    speed = SLIME_SPEED
    size = (30, 26)
    sprite = "slime"


class Spiky(Enemy):
    stompable = False
    turns_at_edges = True
    speed = SPIKY_SPEED
    size = (30, 28)
    sprite = "spiky"


ENEMY_TYPES = {
    "E": Slime,
    "K": Spiky,
}
