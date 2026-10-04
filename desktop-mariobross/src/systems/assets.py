"""Carga de recursos (imágenes) compatible con desarrollo y con el .exe.

PyInstaller descomprime los recursos en una carpeta temporal
(sys._MEIPASS). resource_path() resuelve la ruta correcta en ambos casos.
"""

import os
import sys

import pygame


def resource_path(*parts):
    """Devuelve la ruta absoluta a un recurso dentro de assets/."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # src/systems/assets.py -> raíz del proyecto
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    return os.path.join(base, "assets", *parts)


class Images:
    """Caché de imágenes. Si falta un archivo devuelve un placeholder visible."""

    _cache = {}

    @classmethod
    def get(cls, name, flip=False):
        key = (name, flip)

        if key in cls._cache:
            return cls._cache[key]

        if flip:
            image = pygame.transform.flip(cls.get(name), True, False)
        else:
            image = cls._load(name)

        cls._cache[key] = image
        return image

    @staticmethod
    def _load(name):
        path = resource_path("images", f"{name}.png")

        try:
            image = pygame.image.load(path)

            if pygame.display.get_surface() is not None:
                image = image.convert_alpha()

            return image

        except (pygame.error, FileNotFoundError):
            # Placeholder magenta: deja claro qué sprite falta sin romper el juego
            surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            surface.fill((255, 0, 255, 200))
            return surface

    @classmethod
    def clear(cls):
        cls._cache.clear()
