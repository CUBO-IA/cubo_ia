"""Resolución de colisiones entidad <-> mundo.

Orden fijo en cada frame:
    1. mover en X  -> resolver choques laterales
    2. mover en Y  -> resolver suelo / techo
    3. sondear 1 px debajo -> on_ground

El mundo (Level) entrega solo los sólidos cercanos (búsqueda por grid),
así el coste no depende del tamaño del nivel.
"""

from src.systems.physics import move_x, move_y, sync_position


class CollisionResult:
    __slots__ = ("hit_wall", "head_hits", "landed")

    def __init__(self):
        self.hit_wall = False
        self.head_hits = []
        self.landed = False


def move_and_collide(entity, world):
    result = CollisionResult()

    # ---------------------------------------------------------
    # 1) Horizontal
    # ---------------------------------------------------------
    move_x(entity, entity.velocity_x)

    for solid in world.solids_near(entity.rect):
        if solid.one_way or not entity.rect.colliderect(solid.rect):
            continue

        if entity.velocity_x > 0:
            entity.rect.right = solid.rect.left
        elif entity.velocity_x < 0:
            entity.rect.left = solid.rect.right
        else:
            # Empujado sin velocidad propia: salir por el lado más cercano
            if entity.rect.centerx < solid.rect.centerx:
                entity.rect.right = solid.rect.left
            else:
                entity.rect.left = solid.rect.right

        result.hit_wall = True

    if result.hit_wall:
        sync_position(entity)

    # ---------------------------------------------------------
    # 2) Vertical
    # ---------------------------------------------------------
    bottom_before = entity.rect.bottom
    move_y(entity, entity.velocity_y)

    corrected = False

    for solid in world.solids_near(entity.rect):
        if not entity.rect.colliderect(solid.rect):
            continue

        if solid.one_way:
            # Plataformas atravesables: solo se pisan desde arriba
            top_limit = max(solid.rect.top, solid.prev_top) + 1
            if entity.velocity_y < 0 or bottom_before > top_limit:
                continue

        if entity.velocity_y > 0:
            entity.rect.bottom = solid.rect.top
            result.landed = True
            corrected = True

        elif entity.velocity_y < 0:
            entity.rect.top = solid.rect.bottom
            result.head_hits.append(solid)
            corrected = True

    if corrected:
        entity.velocity_y = 0
        sync_position(entity)

    # ---------------------------------------------------------
    # 3) ¿Está en el suelo?
    # ---------------------------------------------------------
    entity.ground = find_ground(entity, world)
    entity.on_ground = entity.ground is not None

    return result


def find_ground(entity, world):
    """Devuelve el sólido justo debajo (1 px) o None."""
    if entity.velocity_y < 0:
        return None

    probe = entity.rect.move(0, 1)

    for solid in world.solids_near(probe):
        if not probe.colliderect(solid.rect):
            continue

        if solid.one_way and entity.rect.bottom > solid.rect.top:
            continue

        return solid

    return None


def ground_ahead(entity, world, direction):
    """True si hay suelo delante (lo usan los enemigos para no caerse)."""
    x = entity.rect.right + 2 if direction > 0 else entity.rect.left - 2
    probe = entity.rect.copy()
    probe.width = 2
    probe.left = x
    probe.top = entity.rect.bottom + 1
    probe.height = 2

    for solid in world.solids_near(probe):
        if probe.colliderect(solid.rect):
            return True

    return False
