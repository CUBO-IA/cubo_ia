"""Pantalla de victoria al completar el nivel 3."""

import math

import pygame

from src.settings import WIDTH, HEIGHT, HIGHLIGHT_COLOR
from src.states.base import State, font
from src.systems.assets import Images


class VictoryState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = font(96)
        self.text_font = font(36)
        self.timer = 0

        game.audio.stop_music()
        game.audio.play("victory")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.timer > 60:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.next_state = "menu"

    def update(self):
        self.timer += 1

    def draw(self, screen):
        screen.fill((20, 25, 60))

        # Lluvia de monedas
        coin = Images.get(f"coin_{(self.timer // 6) % 4 + 1}")
        for i in range(14):
            x = (i * 73 + 40) % WIDTH
            y = (self.timer * (2 + i % 3) + i * 97) % (HEIGHT + 40) - 40
            screen.blit(coin, (x, y))

        bob = int(math.sin(self.timer / 15) * 6)
        self.draw_text(screen, self.title_font, "¡VICTORIA!", (WIDTH // 2, HEIGHT // 2 - 90 + bob), HIGHLIGHT_COLOR)
        self.draw_text(screen, self.text_font, "Has completado Aventura Pixel", (WIDTH // 2, HEIGHT // 2 - 20))
        self.draw_text(screen, self.text_font, f"Puntuación final: {self.game.session.score:06d}", (WIDTH // 2, HEIGHT // 2 + 30))

        player = Images.get("player_big_jump")
        screen.blit(player, player.get_rect(midbottom=(WIDTH // 2, HEIGHT // 2 + 140 + bob)))

        if self.timer > 60:
            self.draw_text(screen, self.text_font, "ENTER - Volver al menú", (WIDTH // 2, HEIGHT - 50))
