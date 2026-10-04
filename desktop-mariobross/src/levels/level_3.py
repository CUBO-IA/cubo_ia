"""Nivel 3 — Fortaleza. Plataformas móviles sobre abismos y el reto final."""

from src.levels.builder import LevelBuilder


def build():
    b = LevelBuilder(212, "3", "fortaleza")

    # ---- Puerta de la fortaleza -------------------------------------
    b.ground(0, 30)
    b.start(3)
    b.row(9, 9, "BMB")
    b.enemy(15, "K")
    b.column(20, 10, 12)
    b.enemy(24)
    b.enemy(26)

    # ---- Plataformas móviles horizontales ---------------------------
    b.moving_platform(33, 11, width_tiles=3, axis="x", distance=5, speed=1.3)
    b.coins(36, 8, 3)
    b.ground(44, 60)
    b.row(47, 9, "?B?")
    b.enemy(52, "K")
    b.enemy(56)

    # ---- Escalones flotantes -----------------------------------------
    b.row(63, 11, "SS")
    b.row(67, 9, "SS")
    b.row(71, 7, "SS")
    b.coins(71, 6, 2)
    b.row(75, 9, "SS")
    b.ground(79, 105)
    b.row(84, 9, "BNB")
    b.enemy(88)
    b.enemy(90)
    b.enemy(92, "K")
    b.column(97, 10, 12)
    b.column(101, 9, 12)

    # ---- Ascensores verticales ----------------------------------------
    b.moving_platform(108, 8, width_tiles=2, axis="y", distance=4, speed=1.0)
    b.moving_platform(112, 8, width_tiles=2, axis="y", distance=4, speed=1.4)
    b.coins(109, 5, 2)
    b.coins(112, 5, 2)
    b.ground(116, 150)
    b.row(123, 9, "M")
    b.enemy(128, "K")
    b.enemy(131)
    b.enemy(133)
    b.row(136, 5, "BBBBBB")
    b.row(136, 9, "B?BB?B")
    b.enemy(144, "K")
    b.enemy(146, "K")

    # ---- Puente final con plataforma móvil --------------------------
    b.moving_platform(153, 11, width_tiles=4, axis="x", distance=6, speed=1.4)
    b.ground(164, 211)
    b.enemy(170)
    b.enemy(172)
    b.enemy(174, "K")
    b.stairs_up(180, 5)
    b.column(185, 8, 12)
    b.coins(188, 9, 4)
    b.enemy(195, "K")
    b.door(204)

    return b.build()
