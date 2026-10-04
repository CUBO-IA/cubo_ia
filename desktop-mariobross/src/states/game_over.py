"""Pantalla de Game Over."""

import pygame

from src.settings import WIDTH, HEIGHT, HIGHLIGHT_COLOR
from src.states.base import State, font


class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = font(96)
        self.text_font = font(36)
        self.final_score = game.session.score
        self.timer = 0

        game.audio.stop_music()
        game.audio.play("game_over")

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN or self.timer < 30:
            return

        if event.key == pygame.K_RETURN:
            self.game.session.reset()
            self.next_state = "level_intro"

        elif event.key == pygame.K_ESCAPE:
            self.next_state = "menu"

    def update(self):
        self.timer += 1

    def draw(self, screen):
        screen.fill((15, 5, 10))
        self.draw_text(screen, self.title_font, "GAME OVER", (WIDTH // 2, HEIGHT // 2 - 70), (230, 70, 70))
        self.draw_text(screen, self.text_font, f"Puntuación: {self.final_score:06d}", (WIDTH // 2, HEIGHT // 2 + 10), HIGHLIGHT_COLOR)
        self.draw_text(screen, self.text_font, "ENTER - Reintentar    ESC - Menú", (WIDTH // 2, HEIGHT // 2 + 80))
