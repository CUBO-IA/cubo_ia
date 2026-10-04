"""Fondo con degradado y dos capas de parallax."""

import pygame

from src.settings import WIDTH, HEIGHT, THEMES
from src.systems.assets import Images


class Background:
    def __init__(self, theme):
        self.theme = theme
        colors = THEMES[theme]

        # Degradado pre-renderizado una sola vez (bajo consumo)
        self.sky = pygame.Surface((WIDTH, HEIGHT))
        top, bottom = colors["sky_top"], colors["sky_bottom"]

        for y in range(HEIGHT):
            t = y / (HEIGHT - 1)
            color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
            pygame.draw.line(self.sky, color, (0, y), (WIDTH, y))

        if theme == "fortaleza":
            # Luna fija en el cielo (no se repite con el parallax)
            pygame.draw.circle(self.sky, (250, 235, 200), (760, 110), 46)
            pygame.draw.circle(self.sky, self.sky.get_at((800, 60)), (780, 98), 40)

        self.far = Images.get(f"bg_far_{theme}")
        self.near = Images.get(f"bg_near_{theme}")

    def _draw_layer(self, screen, image, offset):
        width = image.get_width()
        if width <= 0:
            return

        x = -int(offset) % width - width

        while x < WIDTH:
            screen.blit(image, (x, HEIGHT - image.get_height()))
            x += width

    def draw(self, screen, camera_x):
        screen.blit(self.sky, (0, 0))
        self._draw_layer(screen, self.far, camera_x * 0.2)
        self._draw_layer(screen, self.near, camera_x * 0.5)
