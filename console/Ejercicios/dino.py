import os, sys, time, random

os.system("")  # Activa colores ANSI en el CMD de Windows
VERDE, GRIS, RESET = "\033[92m", "\033[90m", "\033[0m"

# --- Lectura de teclado sin bloquear (Windows / Linux-Mac) ---
if os.name == "nt":
    import msvcrt
    def tecla():
        if msvcrt.kbhit():
            k = msvcrt.getch()
            if k in (b"\x00", b"\xe0"):
                return "arriba" if msvcrt.getch() == b"H" else ""
            return k.decode(errors="ignore").lower()
        return ""
else:
    import termios, tty, select, atexit
    fd = sys.stdin.fileno(); viejo = termios.tcgetattr(fd); tty.setcbreak(fd)
    atexit.register(lambda: termios.tcsetattr(fd, termios.TCSADRAIN, viejo))
    def tecla():
        return sys.stdin.read(1).lower() if select.select([sys.stdin], [], [], 0)[0] else ""

ANCHO, ALTO, DX = 70, 14, 4
DINO = ["    __ ",
        "   / _)",
        " _/ /  ",
        "/_|_|  "]
CACTUS = [["| |", "|_|", " | "], ["|_|", " | "], [" | ", "|||", " | "]]

def dibujar(y, obstaculos, puntos):
    grid = [[(" ", "")] * ANCHO for _ in range(ALTO)]
    for x, forma in obstaculos:                       # Cactus
        for i, fila in enumerate(forma):
            r = ALTO - len(forma) + i
            for j, c in enumerate(fila):
                if 0 <= int(x) + j < ANCHO and c != " ":
                    grid[r][int(x) + j] = (c, GRIS)
    for i, fila in enumerate(DINO):                   # Dinosaurio verde
        r = ALTO - len(DINO) + i - round(y)
        for j, c in enumerate(fila):
            if c != " ":
                grid[r][DX + j] = (c, VERDE)
    lineas = [f"Puntos: {puntos:05d}   [ESPACIO / W / Flecha arriba] saltar   [Q] salir"]
    lineas += ["".join(col + c + RESET if col else c for c, col in fila) for fila in grid]
    lineas.append("=" * ANCHO)
    sys.stdout.write("\033[H" + "\n".join(lineas)); sys.stdout.flush()

def jugar():
    y, vy, obstaculos, puntos, vel, siguiente = 0.0, 0.0, [], 0, 1.0, 20
    while True:
        k = tecla()
        if k == "q":
            return None
        if k in (" ", "w", "arriba") and y == 0:
            vy = 1.8
        y, vy = max(0.0, y + vy), vy - 0.25
        if y == 0: vy = 0.0
        for o in obstaculos: o[0] -= vel
        obstaculos = [o for o in obstaculos if o[0] > -4]
        siguiente -= vel
        if siguiente <= 0:
            obstaculos.append([ANCHO, random.choice(CACTUS)])
            siguiente = random.randint(25, 45)
        puntos += 1
        vel = min(2.0, 1 + puntos / 600)
        for x, forma in obstaculos:                   # Colisión
            if int(x) <= DX + 5 and int(x) + len(forma[0]) - 1 >= DX + 1 and round(y) < len(forma):
                dibujar(y, obstaculos, puntos)
                return puntos
        dibujar(y, obstaculos, puntos)
        time.sleep(0.05)

sys.stdout.write("\033[2J\033[?25l")  # Limpia pantalla y oculta cursor
try:
    while True:
        puntos = jugar()
        if puntos is None:
            break
        print(f"\n\n   GAME OVER  -  Puntos: {puntos}   |   [R] reiniciar   [Q] salir")
        k = ""
        while k not in ("r", "q"):
            k = tecla(); time.sleep(0.05)
        if k == "q":
            break
        sys.stdout.write("\033[2J")
finally:
    sys.stdout.write("\033[?25h" + RESET + "\n")
