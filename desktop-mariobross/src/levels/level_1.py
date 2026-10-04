"""Nivel 1 — Pradera. Introduce saltos, bloques, slimes y el cristal."""

from src.levels.builder import LevelBuilder


def build():
    b = LevelBuilder(190, "1", "pradera")

    # ---- Zona inicial -------------------------------------------------
    b.ground(0, 62)
    b.start(3)

    b.row(14, 9, "?")
    b.row(19, 9, "B?BMB")
    b.row(21, 5, "?")
    b.enemy(24)

    b.column(30, 11, 12)                 # pilar bajo
    b.coins(33, 10, 3)
    b.column(38, 10, 12)                 # pilar medio
    b.enemy(42)
    b.enemy(44)
    b.column(48, 10, 12)

    b.row(53, 9, "BNB")
    b.coins(53, 5, 3)
    b.enemy(58)

    # ---- Primer hueco (2 celdas) -------------------------------------
    b.ground(65, 92)
    b.row(70, 9, "B?B")
    b.row(73, 5, "BBBBBB")
    b.coins(74, 4, 4)
    b.enemy(76)
    b.enemy(78)
    b.row(84, 9, "??")
    b.enemy(88, "K")                     # primer erizo: no se puede pisar

    # ---- Segundo hueco (3 celdas) ------------------------------------
    b.ground(96, 140)
    b.row(100, 9, "BMB")
    b.coins(104, 10, 5)
    b.enemy(108)
    b.enemy(110)
    b.stairs_up(116, 4)
    b.stairs_down(120, 4)
    b.enemy(127)
    b.row(130, 9, "B?B?B")
    b.coins(131, 5, 3, gap=2)

    # ---- Escalera final y meta ---------------------------------------
    b.ground(144, 189)
    b.enemy(150)
    b.enemy(152, "K")
    b.stairs_up(160, 6)
    b.column(166, 7, 12)                 # cima de la escalera
    b.column(167, 7, 12)
    b.coins(172, 10, 3)
    b.door(180)

    return b.build()
