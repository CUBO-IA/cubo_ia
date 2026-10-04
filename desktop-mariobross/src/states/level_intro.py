"""Pantalla breve antes de cada nivel: mundo y vidas restantes."""

import pygame

from src.settings import WIDTH, HEIGHT, HIGHLIGHT_COLOR
from src.states.base import State, font
from src.systems.assets import Images
from src.levels import LEVEL_TITLES


class LevelIntroState(State):
    DURATION = 150

    def __init__(self, game):
        super().__init__(game)
        self.timer = 0
        self.title_font = font(64)
        self.text_font = font(40)
        game.audio.stop_music()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.next_state = "play"
            elif event.key == pygame.K_ESCAPE:
                self.next_state = "menu"

    def update(self):
        self.timer += 1
        if self.timer >= self.DURATION:
            self.next_state = "play"

    def draw(self, screen):
        screen.fill((0, 0, 0))
        session = self.game.session
        index = session.level_index

        self.draw_text(screen, self.title_font, f"MUNDO {index + 1}", (WIDTH // 2, HEIGHT // 2 - 80))
        self.draw_text(screen, self.text_font, LEVEL_TITLES[index], (WIDTH // 2, HEIGHT // 2 - 30), HIGHLIGHT_COLOR)

        icon = Images.get("player_big_idle" if session.player_big else "player_small_idle")
        screen.blit(icon, icon.get_rect(midright=(WIDTH // 2 - 10, HEIGHT // 2 + 50)))
        self.draw_text(screen, self.text_font, f"x  {session.lives}", (WIDTH // 2 + 40, HEIGHT // 2 + 50))

        self.draw_text(screen, font(28), f"PUNTOS {session.score:06d}", (WIDTH // 2, HEIGHT - 60))
