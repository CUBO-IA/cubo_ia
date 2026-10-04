"""Reglas físicas generales: gravedad, aceleración y fricción.

Las funciones trabajan sobre cualquier entidad con:
    pos_x, pos_y, velocity_x, velocity_y, rect
"""

from src.settings import MAX_FALL_SPEED


def apply_gravity(entity, gravity):
    """Acelera la caída y limita la velocidad máxima."""
    entity.velocity_y += gravity

    if entity.velocity_y > MAX_FALL_SPEED:
        entity.velocity_y = MAX_FALL_SPEED


def approach(value, target, step):
    """Mueve value hacia target sin pasarse (aceleración/fricción suave)."""
    if value < target:
        return min(value + step, target)

    if value > target:
        return max(value - step, target)

    return value


def move_x(entity, dx):
    entity.pos_x += dx
    entity.rect.x = round(entity.pos_x)


def move_y(entity, dy):
    entity.pos_y += dy
    entity.rect.y = round(entity.pos_y)


def sync_position(entity):
    """Copia rect -> posición float tras corregir una colisión."""
    entity.pos_x = float(entity.rect.x)
    entity.pos_y = float(entity.rect.y)
