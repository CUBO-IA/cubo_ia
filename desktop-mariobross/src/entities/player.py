"""Jugador: movimiento con inercia, salto variable, tamaño pequeño/grande."""

import pygame

from src.settings import (
    WALK_SPEED,
    RUN_SPEED,
    ACCEL_GROUND,
    ACCEL_AIR,
    FRICTION,
    GRAVITY,
    GRAVITY_FALL,
    JUMP_SPEED,
    JUMP_SPEED_RUN,
    COYOTE_FRAMES,
    JUMP_BUFFER_FRAMES,
    INVULNERABLE_FRAMES,
    PLAYER_SMALL_SIZE,
    PLAYER_BIG_SIZE,
    MAX_FALL_SPEED,
)
from src.systems.physics import apply_gravity, approach, move_y, sync_position
from src.systems.collision import move_and_collide
from src.systems.assets import Images


class Controls:
    """Estado de los controles en el frame actual."""

    def __init__(self):
        self.left = False
        self.right = False
        self.run = False
        self.jump_held = False
        self.jump_pressed = False   # solo True el frame en que se pulsa

    def read_keyboard(self):
        keys = pygame.key.get_pressed()
        self.left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        self.run = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_x]
        self.jump_held = (
            keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_z]
        )


JUMP_KEYS = (pygame.K_SPACE, pygame.K_UP, pygame.K_w, pygame.K_z)


class Player:
    def __init__(self, x, y, big=False):
        self.big = big
        w, h = PLAYER_BIG_SIZE if big else PLAYER_SMALL_SIZE

        # x, y = esquina inferior-centro de la celda de inicio
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.midbottom = (x, y)
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.on_ground = False
        self.ground = None
        self.facing = 1

        self.coyote = 0
        self.jump_buffer = 0

        self.invulnerable = 0
        self.transform_timer = 0      # animación de crecer/encoger (congela el juego)
        self.dead = False
        self.death_timer = 0

        self.anim_distance = 0.0
        self.events = []              # sonidos/eventos que PlayState consume

    # -----------------------------------------------------------
    # Tamaño
    # -----------------------------------------------------------
    def set_big(self, big):
        if big == self.big:
            return

        bottom, centerx = self.rect.bottom, self.rect.centerx
        self.big = big
        self.rect.size = PLAYER_BIG_SIZE if big else PLAYER_SMALL_SIZE
        self.rect.midbottom = (centerx, bottom)
        sync_position(self)
        self.transform_timer = 40

    def hurt(self):
        """Devuelve True si muere, False si solo encoge."""
        if self.invulnerable > 0 or self.dead:
            return False

        if self.big:
            self.set_big(False)
            self.invulnerable = INVULNERABLE_FRAMES
            self.events.append("shrink")
            return False

        self.die()
        return True

    def die(self):
        if self.dead:
            return

        self.dead = True
        self.death_timer = 0
        self.velocity_x = 0
        self.velocity_y = -11
        self.events.append("death")

    def bounce(self, speed):
        self.velocity_y = speed
        self.on_ground = False

    # -----------------------------------------------------------
    # Actualización
    # -----------------------------------------------------------
    def update(self, controls, world):
        if self.dead:
            self.death_timer += 1

            if self.death_timer > 30:     # pequeña pausa antes de caer
                self.velocity_y = min(self.velocity_y + 0.5, MAX_FALL_SPEED)
                move_y(self, self.velocity_y)

            return None

        if self.invulnerable > 0:
            self.invulnerable -= 1

        # Viajar con la plataforma móvil
        if self.ground is not None and getattr(self.ground, "kind", "") == "moving":
            self.pos_x += self.ground.dx
            self.pos_y += self.ground.dy
            self.rect.x = round(self.pos_x)
            self.rect.y = round(self.pos_y)

        self._horizontal_control(controls)
        self._jump_control(controls)

        gravity = GRAVITY if (self.velocity_y < 0 and controls.jump_held) else GRAVITY_FALL
        apply_gravity(self, gravity)

        result = move_and_collide(self, world)

        if result.hit_wall:
            self.velocity_x = 0

        # Distancia recorrida -> ciclo de animación al caminar
        self.anim_distance += abs(self.velocity_x)
        return result

    def _horizontal_control(self, controls):
        direction = int(controls.right) - int(controls.left)
        max_speed = RUN_SPEED if controls.run else WALK_SPEED

        if direction != 0:
            self.facing = direction
            accel = ACCEL_GROUND if self.on_ground else ACCEL_AIR

            # Derrape: cambiar de dirección frena más rápido
            if self.velocity_x * direction < 0 and self.on_ground:
                accel *= 2

            self.velocity_x = approach(self.velocity_x, direction * max_speed, accel)

        else:
            friction = FRICTION if self.on_ground else FRICTION * 0.3
            self.velocity_x = approach(self.velocity_x, 0, friction)

    def _jump_control(self, controls):
        self.coyote = COYOTE_FRAMES if self.on_ground else max(0, self.coyote - 1)

        if controls.jump_pressed:
            self.jump_buffer = JUMP_BUFFER_FRAMES
        else:
            self.jump_buffer = max(0, self.jump_buffer - 1)

        if self.jump_buffer > 0 and self.coyote > 0:
            fast = abs(self.velocity_x) > WALK_SPEED + 0.5
            self.velocity_y = JUMP_SPEED_RUN if fast else JUMP_SPEED
            self.jump_buffer = 0
            self.coyote = 0
            self.on_ground = False
            self.ground = None
            self.events.append("jump_big" if self.big else "jump")

    # -----------------------------------------------------------
    # Dibujo
    # -----------------------------------------------------------
    def _frame_name(self):
        size = "big" if self.big else "small"

        # Parpadeo entre tamaños mientras crece/encoge
        if self.transform_timer > 0:
            size = "big" if (self.transform_timer // 5) % 2 == (0 if self.big else 1) else "small"

        if self.dead:
            return "player_small_dead"

        if not self.on_ground:
            return f"player_{size}_jump"

        if abs(self.velocity_x) < 0.3:
            return f"player_{size}_idle"

        step = int(self.anim_distance / 14) % 3
        return f"player_{size}_walk{step + 1}"

    def draw(self, screen, camera):
        if self.invulnerable > 0 and (self.invulnerable // 4) % 2 == 0:
            return

        image = Images.get(self._frame_name(), flip=self.facing < 0)
        draw_rect = camera.apply(self.rect)
        image_rect = image.get_rect(midbottom=draw_rect.midbottom)
        screen.blit(image, image_rect)
