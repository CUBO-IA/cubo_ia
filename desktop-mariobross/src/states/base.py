"""Clase base para todos los estados/pantallas."""

import pygame

from src.settings import TEXT_COLOR, SHADOW_COLOR


class State:
    def __init__(self, game):
        self.game = game
        self.next_state = None

    # Interfaz que llama Game en cada frame
    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    # Utilidad: texto con sombra centrado
    @staticmethod
    def draw_text(screen, font, text, center, color=TEXT_COLOR):
        shadow = font.render(text, True, SHADOW_COLOR)
        surface = font.render(text, True, color)

        rect = surface.get_rect(center=center)
        screen.blit(shadow, rect.move(3, 3))
        screen.blit(surface, rect)


def font(size):
    """Fuente por defecto de Pygame (incluida en el .exe)."""
    return pygame.font.Font(None, size)
