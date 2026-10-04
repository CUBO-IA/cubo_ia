"""Genera todos los recursos originales del juego (sprites, sonidos e icono).

Uso (desde la raíz del proyecto, con el .venv activo):
    python tools/generate_assets.py

Los archivos se escriben en assets/images, assets/sounds y assets/icon.
Se pueden reemplazar después por arte definitivo con el mismo nombre.
"""

import math
import os
import random
import struct
import sys
import wave

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "assets", "images")
SOUNDS = os.path.join(ROOT, "assets", "sounds")
ICON = os.path.join(ROOT, "assets", "icon")

SCALE = 3
TILE = 36

# =====================================================================
# SPRITES (pixel art definido como texto)
# =====================================================================
PALETTE = {
    ".": None,
    "H": (40, 175, 170),    # capucha
    "h": (22, 115, 120),
    "S": (245, 200, 160),   # piel
    "E": (30, 30, 40),      # ojos
    "X": (200, 40, 40),
    "G": (250, 210, 80),    # gafas
    "O": (245, 130, 40),    # bufanda
    "B": (55, 75, 150),     # chaqueta
    "b": (35, 45, 95),
    "P": (115, 80, 55),     # pantalón
    "K": (55, 38, 30),      # botas
    "W": (255, 255, 255),
    # enemigos
    "g": (40, 120, 50),
    "L": (110, 210, 90),
    "s": (190, 190, 205),
    "R": (180, 70, 50),
    "r": (120, 40, 30),
    # objetos
    "Y": (255, 215, 60),
    "y": (200, 150, 20),
    "Z": (255, 250, 200),
    "M": (220, 70, 200),
    "m": (140, 40, 150),
    "C": (120, 230, 255),
}

HEAD_SMALL = [
    "..hHHHHh..",
    ".hHHHHHHh.",
    ".hGGHHGGh.",
    ".hSSSSSSh.",
    "..SSESSE..",
    "..SSSSSS..",
    ".OOOOOOOO.",
]

SMALL_BODY = {
    "idle": [".OBBBBBBB.", "SBBBBBBBBS", "..PPPPPP..", "..PP..PP..", ".KKK..KKK."],
    "walk1": [".OBBBBBBB.", ".SBBBBBBS.", "..PPPPPP..", ".PP....PP.", "KKK....KKK"],
    "walk2": [".OBBBBBBB.", "..BBBBBBS.", "..PPPPP...", "...PPP....", "...KKK...."],
    "walk3": [".OBBBBBBB.", ".SBBBBBBS.", "..PPPPPP..", "..PP.PP...", ".KKK.KKK.."],
    "jump": ["SOBBBBBBBS", ".BBBBBBBB.", "..PPPPPP..", ".PP...PP..", "KK.....KK."],
}

HEAD_BIG = [
    "..hHHHHh..",
    ".hHHHHHHh.",
    ".hHHHHHHh.",
    ".hGGHHGGh.",
    ".hSSSSSSh.",
    "..SSESSE..",
    "..SSSSSS..",
    "..SSSSSS..",
    ".OOOOOOOO.",
]

BIG_TORSO = [
    ".OOBBBBBB.",
    "BBBBBBBBBB",
    "SBBBBBBBBS",
    "SBBBBBBBBS",
    ".BBBBBBBB.",
    ".bbbbbbbb.",
]

BIG_LEGS = {
    "idle": ["..PPPPPP..", "..PPPPPP..", "..PP..PP..", "..PP..PP..", "..PP..PP..", ".KKK..KKK.", ".KKK..KKK."],
    "walk1": ["..PPPPPP..", "..PPPPPP..", ".PP....PP.", ".PP....PP.", "PP......PP", "KKK....KKK", "KK......KK"],
    "walk2": ["..PPPPPP..", "..PPPPP...", "...PPPP...", "...PPP....", "...PPP....", "...KKK....", "...KKK...."],
    "walk3": ["..PPPPPP..", "..PPPPPP..", "..PP.PP...", "..PP..PP..", ".PP...PP..", ".KKK..KKK.", "KKK...KKK."],
    "jump": ["..PPPPPP..", "..PPPPPP..", ".PP...PP..", "PP.....PP.", "PP......PP", "KK......KK", "K........K"],
}

DEAD_SMALL = [
    "..hHHHHh..",
    ".hHHHHHHh.",
    ".hGGHHGGh.",
    ".hSSSSSSh.",
    "..SXSSXS..",
    "..SSEESS..",
    "SOOOOOOOOS",
    "SBBBBBBBBS",
    ".BBBBBBBB.",
    "..PPPPPP..",
    "..PP..PP..",
    ".KKK..KKK.",
]

SLIME = {
    "slime_1": [
        "...gggg...",
        "..gLLLLg..",
        ".gLLLLLLg.",
        ".gWELWELg.",
        "gLWWLWWLLg",
        "gLLLLLLLLg",
        "gLLLLLLLLg",
        ".gggggggg.",
    ],
    "slime_2": [
        "..........",
        "...gggg...",
        ".ggLLLLgg.",
        "gLWELWELLg",
        "gLWWLWWLLg",
        "gLLLLLLLLg",
        "gLLLLLLLLg",
        "gggggggggg",
    ],
    "slime_flat": [
        "..gggggg..",
        ".gLLLLLLg.",
        "gLELLLELLg",
        "gggggggggg",
    ],
}

SPIKY = {
    "spiky_1": [
        "..s..s..s.",
        ".ss.ss.ss.",
        "sssssssss.",
        "sRRRRRRRss",
        "RWERRRRRRs",
        "RRRRRRRRRs",
        ".rRRRRRRr.",
        ".KK....KK.",
    ],
    "spiky_2": [
        "..s..s..s.",
        ".ss.ss.ss.",
        "sssssssss.",
        "sRRRRRRRss",
        "RWERRRRRRs",
        "RRRRRRRRRs",
        ".rRRRRRRr.",
        "...KK.KK..",
    ],
}

COIN_FRAMES = [
    ["..yy..", ".yYYy.", "yYZYYy", "yYZYYy", "yYZYYy", "yYZYYy", ".yYYy.", "..yy.."],
    ["..yy..", "..yY..", ".yZYy.", ".yZYy.", ".yZYy.", ".yZYy.", "..yY..", "..yy.."],
    ["..y...", "..y...", "..Z...", "..Y...", "..Y...", "..Y...", "..y...", "..y..."],
    ["..yy..", "..Yy..", ".yYZy.", ".yYZy.", ".yYZy.", ".yYZy.", "..Yy..", "..yy.."],
]

CRYSTAL = [
    "....W....",
    "...mMm...",
    "..mMCMm..",
    ".mMCCWMm.",
    "mMMCCCMMm",
    ".mMMCMMm.",
    "..mMMMm..",
    "...mMm...",
    "....m....",
]


def sprite(rows, scale=SCALE):
    width = max(len(r) for r in rows)
    surface = pygame.Surface((width * scale, len(rows) * scale), pygame.SRCALPHA)

    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            color = PALETTE.get(char)
            if color is not None:
                surface.fill(color, (x * scale, y * scale, scale, scale))

    return surface


def save(surface, name):
    pygame.image.save(surface, os.path.join(IMAGES, f"{name}.png"))


def make_characters():
    for frame, body in SMALL_BODY.items():
        save(sprite(HEAD_SMALL + body), f"player_small_{frame}")

    for frame, legs in BIG_LEGS.items():
        torso = list(BIG_TORSO)
        if frame == "jump":
            torso[2] = ".BBBBBBBB."
            torso[1] = "SBBBBBBBBS"
        save(sprite(HEAD_BIG + torso + legs), f"player_big_{frame}")

    save(sprite(DEAD_SMALL), "player_small_dead")

    for name, rows in {**SLIME, **SPIKY}.items():
        save(sprite(rows), name)

    for i, rows in enumerate(COIN_FRAMES):
        save(sprite(rows), f"coin_{i + 1}")

    save(sprite(CRYSTAL), "crystal")


# =====================================================================
# BLOQUES (dibujados con primitivas)
# =====================================================================
GROUND_COLORS = {
    "pradera": {"top": (90, 190, 80), "top_dark": (55, 140, 60), "dirt": (150, 95, 55), "speck": (115, 70, 40)},
    "cueva": {"top": (120, 110, 150), "top_dark": (85, 75, 110), "dirt": (70, 62, 90), "speck": (50, 44, 66)},
    "fortaleza": {"top": (150, 150, 165), "top_dark": (105, 105, 120), "dirt": (90, 80, 95), "speck": (65, 58, 70)},
}


def bevel_block(base, light, dark, size=TILE):
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    s.fill(base)
    pygame.draw.rect(s, light, (0, 0, size, 3))
    pygame.draw.rect(s, light, (0, 0, 3, size))
    pygame.draw.rect(s, dark, (0, size - 3, size, 3))
    pygame.draw.rect(s, dark, (size - 3, 0, 3, size))
    return s


def make_blocks():
    rng = random.Random(7)

    for theme, c in GROUND_COLORS.items():
        fill = pygame.Surface((TILE, TILE))
        fill.fill(c["dirt"])
        for _ in range(9):
            x, y = rng.randrange(2, TILE - 5), rng.randrange(2, TILE - 5)
            fill.fill(c["speck"], (x, y, 3, 3))
        save(fill, f"ground_fill_{theme}")

        top = fill.copy()
        top.fill(c["top"], (0, 0, TILE, 9))
        for x in range(0, TILE, 6):
            top.fill(c["top"], (x, 9, 3, 3))
        top.fill(c["top_dark"], (0, 9, TILE, 0))
        pygame.draw.line(top, c["top_dark"], (0, 8), (TILE, 8), 1)
        save(top, f"ground_top_{theme}")

    save(bevel_block((125, 125, 140), (175, 175, 190), (75, 75, 90)), "stone")
    save(bevel_block((105, 70, 45), (135, 95, 65), (70, 45, 30)), "used")

    # Ladrillo genérico
    brick = pygame.Surface((TILE, TILE))
    brick.fill((70, 40, 30))
    mortar_h = 2
    for row in range(3):
        y = row * 12
        offset = 0 if row % 2 == 0 else -9
        for col in range(-1, 3):
            x = col * 18 + offset
            pygame.draw.rect(brick, (190, 95, 55), (x + 1, y + 1, 16, 12 - mortar_h))
            pygame.draw.rect(brick, (220, 130, 80), (x + 1, y + 1, 16, 2))
    save(brick, "brick")

    debris = pygame.Surface((12, 12), pygame.SRCALPHA)
    debris.fill((190, 95, 55))
    debris.fill((220, 130, 80), (0, 0, 12, 3))
    save(debris, "debris")

    # Bloque bonus: dorado con un rombo-estrella propio, 3 brillos
    for i, glow in enumerate(((240, 180, 50), (255, 205, 80), (255, 230, 140))):
        s = bevel_block(glow, (255, 245, 190), (170, 110, 30))
        cx = cy = TILE // 2
        points = [(cx, cy - 11), (cx + 4, cy - 4), (cx + 11, cy), (cx + 4, cy + 4),
                  (cx, cy + 11), (cx - 4, cy + 4), (cx - 11, cy), (cx - 4, cy - 4)]
        pygame.draw.polygon(s, (150, 80, 20), [(x + 1, y + 1) for x, y in points])
        pygame.draw.polygon(s, (255, 255, 255), points)
        for x, y in ((4, 4), (TILE - 7, 4), (4, TILE - 7), (TILE - 7, TILE - 7)):
            s.fill((170, 110, 30), (x, y, 3, 3))
        save(s, f"bonus_{i}")

    # Plataforma móvil (madera con remaches)
    plank = pygame.Surface((TILE, TILE // 2), pygame.SRCALPHA)
    plank.fill((160, 115, 70))
    plank.fill((200, 150, 95), (0, 0, TILE, 3))
    plank.fill((100, 70, 45), (0, TILE // 2 - 3, TILE, 3))
    for x in (5, TILE - 8):
        plank.fill((70, 70, 80), (x, 7, 3, 3))
    save(plank, "platform")

    # Puerta de meta
    door = pygame.Surface((TILE + 8, TILE * 2 + 4), pygame.SRCALPHA)
    w, h = door.get_size()
    pygame.draw.rect(door, (120, 120, 135), (0, 10, w, h - 10), border_top_left_radius=20, border_top_right_radius=20)
    pygame.draw.rect(door, (120, 70, 40), (5, 16, w - 10, h - 16), border_top_left_radius=16, border_top_right_radius=16)
    for x in range(10, w - 8, 8):
        pygame.draw.line(door, (90, 50, 28), (x, 20), (x, h), 2)
    pygame.draw.circle(door, (250, 210, 80), (w - 13, h // 2 + 10), 3)
    pygame.draw.line(door, (230, 230, 230), (w // 2, 10), (w // 2, -2), 2)
    pygame.draw.polygon(door, (250, 80, 80), [(w // 2, 0), (w // 2 + 14, 4), (w // 2, 8)])
    save(door, "door")


# =====================================================================
# FONDOS
# =====================================================================
def make_backgrounds():
    rng = random.Random(11)
    width = 960

    # Pradera: montañas lejanas + colinas con arbustos y nubes
    far = pygame.Surface((width, 360), pygame.SRCALPHA)
    for i in range(6):
        x = i * 180 - 40
        peak = 120 + rng.randrange(60)
        for sx in (x - width, x, x + width):   # copias en los bordes = sin cortes
            pygame.draw.polygon(far, (120, 170, 200), [(sx, 360), (sx + 120, peak), (sx + 240, 360)])
            # nieve: triángulo semejante en la cima
            pygame.draw.polygon(far, (235, 245, 255), [(sx + 102, peak + 18), (sx + 120, peak), (sx + 138, peak + 18)])
    for i in range(5):
        cx, cy = i * 200 + 60, 60 + rng.randrange(80)
        for dx, r in ((0, 18), (20, 24), (44, 18)):
            pygame.draw.circle(far, (255, 255, 255), (cx + dx, cy), r)
    save(far, "bg_far_pradera")

    near = pygame.Surface((width, 200), pygame.SRCALPHA)
    for i in range(5):
        cx = i * 192 + 80
        top = 60 + rng.randrange(30)
        for shift in (-width, 0, width):   # repetir en los bordes = sin cortes
            pygame.draw.ellipse(near, (95, 175, 100), (cx - 140 + shift, top, 300, 260))
    for i in range(7):
        cx = i * 150 + 40
        for dx in (0, 22, 44):
            pygame.draw.circle(near, (60, 150, 70), (cx + dx, 150), 18)
    save(near, "bg_near_pradera")

    # Cueva: estalactitas y rocas
    far = pygame.Surface((width, 540), pygame.SRCALPHA)
    for i in range(16):
        x = i * 64 + rng.randrange(20)
        pygame.draw.polygon(far, (55, 50, 80), [(x, 0), (x + 20, 120 + rng.randrange(120)), (x + 40, 0)])
    for i in range(10):
        x = i * 100 + rng.randrange(30)
        pygame.draw.polygon(far, (50, 45, 75), [(x, 540), (x + 30, 300 + rng.randrange(120)), (x + 60, 540)])
    for _ in range(30):
        pygame.draw.circle(far, (120, 230, 255, 120), (rng.randrange(width), rng.randrange(400)), 2)
    save(far, "bg_far_cueva")

    near = pygame.Surface((width, 220), pygame.SRCALPHA)
    for i in range(8):
        x = i * 130 + rng.randrange(30)
        pygame.draw.polygon(near, (40, 36, 60), [(x, 220), (x + 50, 40 + rng.randrange(80)), (x + 100, 220)])
    save(near, "bg_near_cueva")

    # Fortaleza: luna, torres y almenas
    far = pygame.Surface((width, 540), pygame.SRCALPHA)
    for _ in range(40):
        far.fill((255, 255, 255), (rng.randrange(width), rng.randrange(260), 2, 2))
    for i in range(6):
        x = i * 170 + 20
        top = 220 + rng.randrange(80)
        pygame.draw.rect(far, (45, 25, 55), (x, top, 60, 540 - top))
        for k in range(4):
            pygame.draw.rect(far, (45, 25, 55), (x + k * 16, top - 12, 10, 12))
        pygame.draw.rect(far, (250, 200, 90), (x + 24, top + 30, 10, 16))
    save(far, "bg_far_fortaleza")

    near = pygame.Surface((width, 180), pygame.SRCALPHA)
    pygame.draw.rect(near, (60, 30, 55), (0, 70, width, 110))
    for x in range(0, width, 40):
        pygame.draw.rect(near, (60, 30, 55), (x, 50, 24, 20))
    save(near, "bg_near_fortaleza")


# =====================================================================
# ICONO
# =====================================================================
def make_icon():
    base = sprite(HEAD_SMALL + SMALL_BODY["idle"], scale=1)
    icon = pygame.Surface((64, 64), pygame.SRCALPHA)
    pygame.draw.rect(icon, (40, 60, 120), (0, 0, 64, 64), border_radius=12)
    pygame.draw.rect(icon, (250, 210, 80), (0, 0, 64, 64), 3, border_radius=12)
    big = pygame.transform.scale(base, (40, 48))
    icon.blit(big, big.get_rect(center=(32, 33)))
    png_path = os.path.join(ICON, "icon.png")
    pygame.image.save(icon, png_path)

    # .ico con PNG embebido (válido en Windows Vista+), sin dependencias extra
    sizes = []
    for size in (256, 64, 48, 32, 16):
        surf = pygame.transform.smoothscale(icon, (size, size)) if size != 64 else icon
        tmp = os.path.join(ICON, f"_tmp_{size}.png")
        pygame.image.save(surf, tmp)
        with open(tmp, "rb") as f:
            sizes.append((size, f.read()))
        os.remove(tmp)

    header = struct.pack("<HHH", 0, 1, len(sizes))
    offset = 6 + 16 * len(sizes)
    entries, blobs = b"", b""
    for size, data in sizes:
        dim = 0 if size >= 256 else size
        entries += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(data), offset)
        blobs += data
        offset += len(data)

    with open(os.path.join(ICON, "icon.ico"), "wb") as f:
        f.write(header + entries + blobs)


# =====================================================================
# SONIDO (síntesis simple tipo chiptune)
# =====================================================================
RATE = 22050


def note_freq(name):
    """'C4', 'F#5', 'R' (silencio) -> Hz."""
    if name == "R":
        return 0.0
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    pitch, octave = name[:-1], int(name[-1])
    midi = 12 * (octave + 1) + names[pitch]
    return 440.0 * 2 ** ((midi - 69) / 12)


def osc(kind, phase):
    if kind == "square":
        return 1.0 if (phase % 1.0) < 0.5 else -1.0
    if kind == "pulse":
        return 1.0 if (phase % 1.0) < 0.25 else -1.0
    if kind == "triangle":
        p = phase % 1.0
        return 4 * p - 1 if p < 0.5 else 3 - 4 * p
    return math.sin(2 * math.pi * phase)


def tone(freq_start, freq_end, duration, kind="square", volume=0.4, decay=True):
    n = int(RATE * duration)
    out, phase = [], 0.0
    for i in range(n):
        t = i / n
        freq = freq_start + (freq_end - freq_start) * t
        phase += freq / RATE
        env = (1 - t) if decay else (1.0 if t < 0.9 else (1 - t) * 10)
        out.append(osc(kind, phase) * volume * env if freq > 0 else 0.0)
    return out


def noise(duration, volume=0.4):
    rng = random.Random(3)
    n = int(RATE * duration)
    return [(rng.random() * 2 - 1) * volume * (1 - i / n) for i in range(n)]


def sequence(notes, step, kind="square", volume=0.35, decay=True):
    out = []
    for name, beats in notes:
        f = note_freq(name)
        out += tone(f, f, step * beats, kind, volume, decay)
    return out


def mix(*tracks):
    length = max(len(t) for t in tracks)
    return [sum(t[i] for t in tracks if i < len(t)) for i in range(length)]


def write_wav(samples, name):
    path = os.path.join(SOUNDS, f"{name}.wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        frames = b"".join(struct.pack("<h", int(max(-1.0, min(1.0, s)) * 30000)) for s in samples)
        w.writeframes(frames)


def make_sfx():
    write_wav(tone(320, 760, 0.16, "square", 0.3), "jump")
    write_wav(tone(220, 560, 0.20, "square", 0.3), "jump_big")
    write_wav(tone(988, 988, 0.06, "square", 0.3, False) + tone(1319, 1319, 0.30, "square", 0.3), "coin")
    write_wav(mix(noise(0.08, 0.3), tone(500, 120, 0.12, "triangle", 0.5)), "stomp")
    write_wav(tone(140, 110, 0.09, "triangle", 0.6), "bump")
    write_wav(mix(noise(0.30, 0.45), tone(200, 60, 0.3, "triangle", 0.4)), "break")
    write_wav(sequence([(n, 1) for n in ("G4", "B4", "D5", "G5", "B5")], 0.05, "pulse", 0.3), "powerup_appear")
    write_wav(sequence([(n, 1) for n in ("C5", "E5", "G5", "C6", "D5", "F#5", "A5", "D6", "E5", "G#5", "B5", "E6")], 0.045, "square", 0.3), "powerup")
    write_wav(sequence([(n, 1) for n in ("E5", "C5", "A4", "E4", "C4")], 0.07, "square", 0.3), "shrink")
    write_wav(sequence([("B4", 1), ("F5", 1), ("R", 1), ("F5", 1), ("F5", 1.5), ("E5", 1.5), ("D5", 1.5), ("C5", 3)], 0.11, "square", 0.3), "death")
    write_wav(sequence([("G4", 1), ("C5", 1), ("E5", 1), ("G5", 2), ("E5", 1), ("G5", 4),
                        ("A4", 1), ("D5", 1), ("F5", 1), ("A5", 2), ("F5", 1), ("A5", 4),
                        ("B4", 1), ("E5", 1), ("G#5", 1), ("B5", 6)], 0.09, "square", 0.3), "level_clear")
    write_wav(sequence([("C5", 2), ("G4", 2), ("E4", 2), ("A4", 1.5), ("B4", 1.5), ("A4", 1.5), ("G#4", 2), ("A#4", 2), ("G#4", 2), ("G4", 6)], 0.13, "square", 0.3), "game_over")
    victory = sequence([("C5", 1), ("E5", 1), ("G5", 1), ("C6", 3), ("G5", 1), ("C6", 4),
                        ("D5", 1), ("F5", 1), ("A5", 1), ("D6", 3), ("A5", 1), ("D6", 4),
                        ("E5", 1), ("G5", 1), ("B5", 1), ("E6", 3), ("D6", 1), ("C6", 2), ("D6", 2), ("C6", 8)], 0.1, "square", 0.3)
    bass = sequence([("C3", 6), ("C3", 4), ("D3", 6), ("D3", 4), ("E3", 6), ("G3", 4), ("C3", 8)], 0.1, "triangle", 0.5)
    write_wav(mix(victory, bass), "victory")
    write_wav(sequence([(n, 1) for n in ("E5", "G5", "E6", "C6", "D6", "G6")], 0.08, "square", 0.3), "one_up")
    write_wav(tone(880, 880, 0.06, "square", 0.25) + tone(0, 0, 0.04) + tone(660, 660, 0.08, "square", 0.25), "pause")


# Música: melodías originales generadas a partir de una progresión de acordes
SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
}


def midi_to_freq(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def compose(root, scale, chords, bpm, seed, lead_kind, bars_repeat=2):
    """Bajo en negras + melodía de corcheas sobre los acordes (determinista)."""
    rng = random.Random(seed)
    step = 60 / bpm / 2           # corchea
    degrees = SCALES[scale]

    def degree_note(d, octave):
        return root + 12 * octave + degrees[d % 7] + 12 * (d // 7)

    lead, bass = [], []
    motif = None

    for repeat in range(bars_repeat):
        for bar, chord in enumerate(chords):
            chord_tones = [chord, chord + 2, chord + 4]

            # Motivo de 8 corcheas; se reutiliza con variación para dar coherencia
            if motif is None or bar % 2 == 0:
                motif = []
                for i in range(8):
                    if i % 2 == 0:
                        motif.append(rng.choice(chord_tones) + rng.choice((0, 7)))
                    else:
                        motif.append(None if rng.random() < 0.25 else rng.choice(chord_tones) + rng.choice((0, 1, 7)))

            for i, d in enumerate(motif):
                if d is None:
                    lead += [0.0] * int(RATE * step)
                else:
                    f = midi_to_freq(degree_note(d, 1))
                    lead += tone(f, f, step, lead_kind, 0.16)

            for i in range(4):
                d = chord if i % 2 == 0 else chord + 4
                f = midi_to_freq(degree_note(d, -1))
                bass += tone(f, f, step * 2, "triangle", 0.30, decay=False)

    return mix(lead, bass)


def make_music():
    write_wav(compose(60, "major", [0, 3, 4, 0, 5, 3, 4, 4], 150, 1, "pulse"), "music_pradera")
    write_wav(compose(57, "minor", [0, 5, 3, 4, 0, 5, 6, 4], 108, 2, "triangle"), "music_cueva")
    write_wav(compose(62, "minor", [0, 0, 5, 4, 0, 3, 6, 4], 160, 3, "square"), "music_fortaleza")
    write_wav(compose(65, "major", [0, 5, 3, 4], 120, 4, "pulse"), "music_menu")


# =====================================================================
def main():
    for folder in (IMAGES, SOUNDS, ICON):
        os.makedirs(folder, exist_ok=True)

    pygame.init()
    pygame.display.set_mode((1, 1))

    print("Sprites...")
    make_characters()
    make_blocks()
    make_backgrounds()
    print("Icono...")
    make_icon()
    print("Efectos de sonido...")
    make_sfx()
    print("Música...")
    make_music()

    pygame.quit()
    print("Listo: recursos generados en assets/")


if __name__ == "__main__":
    sys.exit(main())
