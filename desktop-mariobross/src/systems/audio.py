"""Sistema de audio: música y efectos.

Si no hay dispositivo de audio o falta un archivo, el juego sigue sin sonido.
"""

import pygame

from src.settings import MUSIC_VOLUME, SFX_VOLUME
from src.systems.assets import resource_path


SOUND_NAMES = (
    "jump",
    "jump_big",
    "coin",
    "stomp",
    "bump",
    "break",
    "powerup_appear",
    "powerup",
    "shrink",
    "death",
    "level_clear",
    "game_over",
    "victory",
    "one_up",
    "pause",
)


class Audio:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self.current_music = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        except pygame.error:
            self.enabled = False
            return

        for name in SOUND_NAMES:
            try:
                sound = pygame.mixer.Sound(resource_path("sounds", f"{name}.wav"))
                sound.set_volume(SFX_VOLUME)
                self.sounds[name] = sound
            except (pygame.error, FileNotFoundError):
                pass

    def play(self, name):
        if not self.enabled:
            return

        sound = self.sounds.get(name)

        if sound is not None:
            sound.play()

    def play_music(self, name, loop=True):
        if not self.enabled or name == self.current_music:
            return

        try:
            pygame.mixer.music.load(resource_path("sounds", f"{name}.wav"))
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = name
        except (pygame.error, FileNotFoundError):
            self.current_music = None

    def stop_music(self):
        if not self.enabled:
            return

        pygame.mixer.music.stop()
        self.current_music = None

    def pause_music(self, paused):
        if not self.enabled:
            return

        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
