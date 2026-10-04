"""Marcador superior: puntos, monedas, mundo, tiempo y vidas."""

import pygame

from src.settings import WIDTH, TEXT_COLOR, SHADOW_COLOR, HIGHLIGHT_COLOR
from src.systems.assets import Images


class HUD:
    def __init__(self):
        self.label_font = pygame.font.Font(None, 24)
        self.value_font = pygame.font.Font(None, 32)

    def _column(self, screen, x, label, value, color=TEXT_COLOR):
        for font, text, y, col in (
            (self.label_font, label, 10, HIGHLIGHT_COLOR),
            (self.value_font, value, 30, color),
        ):
            shadow = font.render(text, True, SHADOW_COLOR)
            surface = font.render(text, True, col)
            rect = surface.get_rect(midtop=(x, y))
            screen.blit(shadow, rect.move(2, 2))
            screen.blit(surface, rect)

    def draw(self, screen, session, level_name, time_left):
        step = WIDTH // 5

        self._column(screen, step * 0 + step // 2, "PUNTOS", f"{session.score:06d}")
        self._column(screen, step * 1 + step // 2, "MONEDAS", f"x{session.coins:02d}")
        self._column(screen, step * 2 + step // 2, "MUNDO", level_name)

        time_color = (255, 90, 90) if time_left <= 60 else TEXT_COLOR
        self._column(screen, step * 3 + step // 2, "TIEMPO", f"{max(0, time_left):03d}", time_color)
        self._column(screen, step * 4 + step // 2, "VIDAS", f"x{session.lives}")

        coin = Images.get("coin_1")
        screen.blit(coin, coin.get_rect(midright=(step * 1 + step // 2 - 34, 42)))
