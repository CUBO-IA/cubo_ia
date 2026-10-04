"""Menú principal con selección por flechas y pantalla de controles."""

import pygame

from src.settings import WIDTH, HEIGHT, HIGHLIGHT_COLOR, TEXT_COLOR, OVERLAY_COLOR
from src.states.base import State, font
from src.systems.background import Background
from src.systems.assets import Images


OPTIONS = ("JUGAR", "CONTROLES", "SALIR")

CONTROLS_TEXT = (
    ("Moverse", "A / D  o  flechas izquierda / derecha"),
    ("Saltar", "ESPACIO, W, flecha arriba o Z (mantener = más alto)"),
    ("Correr", "SHIFT o X"),
    ("Pausa", "P o ENTER"),
    ("Menú", "ESC"),
)


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)

        self.title_font = font(96)
        self.option_font = font(44)
        self.small_font = font(28)

        self.selected = 0
        self.show_controls = False
        self.scroll = 0.0
        self.frame = 0

        self.background = Background("pradera")
        game.audio.play_music("music_menu")

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.show_controls:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                self.show_controls = False
            return

        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(OPTIONS)
            self.game.audio.play("bump")

        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(OPTIONS)
            self.game.audio.play("bump")

        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._choose(OPTIONS[self.selected])

        elif event.key == pygame.K_ESCAPE:
            self.next_state = "quit"

    def _choose(self, option):
        if option == "JUGAR":
            self.game.audio.play("coin")
            self.game.audio.stop_music()
            self.game.session.reset()
            self.next_state = "level_intro"

        elif option == "CONTROLES":
            self.show_controls = True

        elif option == "SALIR":
            self.next_state = "quit"

    def update(self):
        self.frame += 1
        self.scroll += 0.8

    def draw(self, screen):
        self.background.draw(screen, self.scroll)

        # Suelo decorativo
        tile = Images.get("ground_top_pradera")
        tw = tile.get_width()
        offset = int(self.scroll) % tw
        for x in range(-offset, WIDTH + tw, tw):
            screen.blit(tile, (x, HEIGHT - tw * 2))
            screen.blit(Images.get("ground_fill_pradera"), (x, HEIGHT - tw))

        # Personaje corriendo
        player = Images.get(f"player_small_walk{(self.frame // 8) % 3 + 1}")
        screen.blit(player, player.get_rect(midbottom=(WIDTH // 2, HEIGHT - tw * 2)))

        self.draw_text(screen, self.title_font, "AVENTURA PIXEL", (WIDTH // 2, 110), HIGHLIGHT_COLOR)

        if self.show_controls:
            self._draw_controls(screen)
            return

        for i, option in enumerate(OPTIONS):
            selected = i == self.selected
            color = HIGHLIGHT_COLOR if selected else TEXT_COLOR
            label = f"> {option} <" if selected else option
            self.draw_text(screen, self.option_font, label, (WIDTH // 2, 230 + i * 56), color)

        self.draw_text(screen, self.small_font, "Flechas: elegir    ENTER: aceptar", (WIDTH // 2, 410))

    def _draw_controls(self, screen):
        panel = pygame.Surface((760, 280), pygame.SRCALPHA)
        panel.fill((*OVERLAY_COLOR, 200))
        screen.blit(panel, panel.get_rect(center=(WIDTH // 2, 290)))

        self.draw_text(screen, self.option_font, "CONTROLES", (WIDTH // 2, 180), HIGHLIGHT_COLOR)

        for i, (action, keys) in enumerate(CONTROLS_TEXT):
            y = 225 + i * 36
            label = self.small_font.render(action, True, HIGHLIGHT_COLOR)
            value = self.small_font.render(keys, True, TEXT_COLOR)
            screen.blit(label, (WIDTH // 2 - 350, y))
            screen.blit(value, (WIDTH // 2 - 200, y))

        self.draw_text(screen, self.small_font, "ENTER - Volver", (WIDTH // 2, 420))
