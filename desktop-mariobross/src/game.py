"""Núcleo del juego: ventana, bucle principal y máquina de estados.

Un único bucle:  eventos -> actualizar -> dibujar -> flip
El estado activo (menú, juego, game over...) decide qué hacer en cada paso.
"""

import pygame

from src.settings import WIDTH, HEIGHT, FPS, TITLE, STARTING_LIVES
from src.systems.assets import resource_path
from src.systems.audio import Audio

from src.states.menu import MenuState
from src.states.level_intro import LevelIntroState
from src.states.play import PlayState
from src.states.game_over import GameOverState
from src.states.victory import VictoryState

from src.levels import LEVELS


class Session:
    """Datos que sobreviven entre niveles dentro de una partida."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.coins = 0
        self.lives = STARTING_LIVES
        self.level_index = 0
        self.player_big = False

    @property
    def level_count(self):
        return len(LEVELS)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self._set_icon()

        self.clock = pygame.time.Clock()
        self.running = True

        self.audio = Audio()
        self.session = Session()

        self.states = {
            "menu": MenuState,
            "level_intro": LevelIntroState,
            "play": PlayState,
            "game_over": GameOverState,
            "victory": VictoryState,
        }

        self.state = None
        self.change_state("menu")

    def _set_icon(self):
        try:
            pygame.display.set_icon(pygame.image.load(resource_path("icon", "icon.png")))
        except (pygame.error, FileNotFoundError):
            pass

    # -----------------------------------------------------------
    # Estados
    # -----------------------------------------------------------
    def change_state(self, name):
        if name == "quit":
            self.running = False
            return

        self.state = self.states[name](self)

    # -----------------------------------------------------------
    # Bucle principal
    # -----------------------------------------------------------
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            self.state.handle_event(event)

    def update(self):
        self.state.update()

        if self.state.next_state is not None:
            self.change_state(self.state.next_state)

    def draw(self):
        if self.running:
            self.state.draw(self.screen)
