"""Cámara horizontal: convierte coordenadas de mundo a pantalla.

Como en los plataformas clásicos, solo avanza hacia la derecha:
el jugador no puede volver a la zona que ya quedó atrás.
"""

from src.settings import WIDTH


class Camera:
    def __init__(self, level_width):
        self.level_width = level_width
        self.offset_x = 0.0
        self.dead_zone = WIDTH * 0.42   # el jugador se mantiene cerca del centro

    def update(self, target):
        desired = target.rect.centerx - self.dead_zone

        if desired > self.offset_x:
            self.offset_x = desired

        max_offset = max(0, self.level_width - WIDTH)
        self.offset_x = max(0.0, min(self.offset_x, max_offset))

    @property
    def left(self):
        return int(self.offset_x)

    def apply(self, rect):
        return rect.move(-int(self.offset_x), 0)

    def is_visible(self, rect, margin=0):
        return (
            rect.right >= self.offset_x - margin
            and rect.left <= self.offset_x + WIDTH + margin
        )
