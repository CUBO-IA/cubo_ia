"""Nivel 2 — Cueva. Techo bajo, más erizos y huecos más largos."""

from src.levels.builder import LevelBuilder


def build():
    b = LevelBuilder(200, "2", "cueva")

    # Techo de piedra en toda la cueva (filas 0-1)
    for col in range(0, 200):
        b.set(col, 0, "S")
    for col in range(10, 175):
        b.set(col, 1, "B")

    # ---- Entrada -------------------------------------------------------
    b.ground(0, 40)
    b.start(3)
    b.row(10, 9, "?B?B?")
    b.enemy(18)
    b.enemy(20)
    b.row(24, 9, "M")
    b.column(28, 10, 12)
    b.enemy(32, "K")
    b.coins(34, 6, 5)
    b.row(33, 7, "BBBBBBB")

    # ---- Islas -------------------------------------------------------
    b.ground(44, 52)                      # hueco de 3
    b.enemy(49)
    b.ground(57, 63)                      # hueco de 4 (corre)
    b.coins(54, 9, 2)
    b.ground(67, 90)
    b.row(70, 9, "BBNBB")
    b.enemy(74, "K")
    b.enemy(80)
    b.enemy(82)
    b.column(86, 10, 12)

    # ---- Pasillo con bloques en dos alturas -------------------------
    b.ground(94, 130)
    b.row(96, 9, "B?B")
    b.row(100, 5, "BBBB?BBB")
    b.coins(101, 4, 6)
    b.enemy(104, "K")
    b.enemy(108)
    b.enemy(110)
    b.row(114, 9, "M")
    b.stairs_up(120, 3)
    b.column(123, 10, 12)
    b.stairs_down(124, 3)
    b.enemy(128, "K")

    # ---- Plataformas de piedra sobre el abismo ----------------------
    b.row(134, 11, "SSS")
    b.row(140, 10, "SSS")
    b.coins(140, 9, 3)
    b.row(146, 11, "SSS")
    b.ground(152, 199)
    b.enemy(156)
    b.enemy(158, "K")
    b.enemy(162)

    # ---- Salida -----------------------------------------------------
    b.stairs_up(170, 4)
    b.column(174, 9, 12)
    b.coins(178, 9, 4)
    b.door(190)

    return b.build()
