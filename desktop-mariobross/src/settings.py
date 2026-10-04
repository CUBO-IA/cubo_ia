"""Configuración general de Aventura Pixel.

Todos los números "mágicos" del juego viven aquí para poder ajustarlos
sin tocar la lógica.
"""

# ---------------------------------------------------------------
# Ventana
# ---------------------------------------------------------------
WIDTH = 960
HEIGHT = 540
FPS = 60
TITLE = "Aventura Pixel"

# ---------------------------------------------------------------
# Mundo
# ---------------------------------------------------------------
TILE = 36                    # tamaño de cada celda del mapa (px)
LEVEL_ROWS = 15              # 15 * 36 = 540 -> el nivel ocupa toda la altura
DEATH_Y = HEIGHT + 120       # por debajo de esto el jugador muere

# ---------------------------------------------------------------
# Física del jugador (unidades: píxeles por frame a 60 FPS)
# ---------------------------------------------------------------
WALK_SPEED = 3.6
RUN_SPEED = 6.0
ACCEL_GROUND = 0.30
ACCEL_AIR = 0.20
FRICTION = 0.28

GRAVITY = 0.55               # gravedad mientras se mantiene el salto subiendo
GRAVITY_FALL = 1.10          # gravedad al soltar el salto o al caer (salto variable)
MAX_FALL_SPEED = 12          # siempre menor que TILE para no atravesar bloques

JUMP_SPEED = -11.6
JUMP_SPEED_RUN = -12.6       # salto un poco más alto si se corre a tope
STOMP_BOUNCE = -8.0          # rebote al pisar un enemigo
STOMP_BOUNCE_HELD = -11.0    # rebote si se mantiene el salto

COYOTE_FRAMES = 6            # margen para saltar justo después de dejar el borde
JUMP_BUFFER_FRAMES = 6       # margen para pulsar salto justo antes de aterrizar

INVULNERABLE_FRAMES = 120    # tras recibir daño

# Tamaños del jugador (hitbox)
PLAYER_SMALL_SIZE = (26, 34)
PLAYER_BIG_SIZE = (28, 66)

# ---------------------------------------------------------------
# Enemigos e ítems
# ---------------------------------------------------------------
SLIME_SPEED = 1.0
SPIKY_SPEED = 1.3
ENEMY_ACTIVATE_MARGIN = 120  # se activan al acercarse a la pantalla

CRYSTAL_SPEED = 1.6

# ---------------------------------------------------------------
# Partida
# ---------------------------------------------------------------
STARTING_LIVES = 3
LEVEL_TIME = 300             # segundos de juego por nivel
COINS_FOR_LIFE = 100

SCORE_COIN = 200
SCORE_STOMP = 100
SCORE_BRICK = 50
SCORE_CRYSTAL = 1000
SCORE_TIME_BONUS = 50        # por cada segundo restante

# ---------------------------------------------------------------
# Colores (placeholders si falta algún sprite)
# ---------------------------------------------------------------
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (20, 20, 30)
HIGHLIGHT_COLOR = (255, 210, 80)
OVERLAY_COLOR = (10, 10, 20)

# Temas visuales de cada nivel
THEMES = {
    "pradera": {
        "sky_top": (110, 180, 250),
        "sky_bottom": (190, 230, 255),
        "hills": (90, 170, 110),
        "music": "music_pradera",
    },
    "cueva": {
        "sky_top": (20, 18, 35),
        "sky_bottom": (45, 40, 70),
        "hills": (60, 55, 90),
        "music": "music_cueva",
    },
    "fortaleza": {
        "sky_top": (25, 15, 45),
        "sky_bottom": (120, 50, 70),
        "hills": (70, 35, 60),
        "music": "music_fortaleza",
    },
}

# ---------------------------------------------------------------
# Audio
# ---------------------------------------------------------------
MUSIC_VOLUME = 0.45
SFX_VOLUME = 0.6
