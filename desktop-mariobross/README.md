# Aventura Pixel

Juego de plataformas 2D en Python + Pygame, inspirado en los clásicos del género, con personajes, gráficos, música y niveles originales.

## Requisitos

- Windows 11 x64
- Python 3.13 (64 bits)
- Pygame 2.x

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecutar

```powershell
python main.py
```

## Controles

| Acción | Teclas |
|---|---|
| Moverse | A / D o flechas |
| Saltar | ESPACIO, W, flecha arriba o Z (mantener = salto más alto) |
| Correr | SHIFT o X |
| Pausa | P o ENTER |
| Menú | ESC |

## Cómo se juega

- 3 mundos: **Pradera**, **Cueva** y **Fortaleza**. Llega a la puerta del final de cada uno.
- **Slime** (verde): se elimina saltándole encima.
- **Erizo** (púas): no se puede pisar; esquívalo o golpea el bloque sobre el que camina.
- **Bloques dorados**: golpéalos desde abajo para sacar monedas o un **cristal**.
- **Cristal**: te hace grande. Grande puedes romper ladrillos y aguantar un golpe.
- 100 monedas = 1 vida extra. Al acabar un nivel, el tiempo restante se convierte en puntos.

## Estructura

```
main.py                 punto de entrada
src/game.py             bucle principal y máquina de estados
src/settings.py         configuración (física, puntuación, colores...)
src/states/             menú, intro de nivel, juego, game over, victoria
src/entities/           jugador, enemigos, bloques/plataformas, objetos
src/systems/            física, colisiones, cámara, audio, HUD, fondo, recursos
src/levels/             builder.py + level_1..3 (diseño de cada nivel)
assets/                 imágenes, sonidos e icono
tools/generate_assets.py  regenera todos los recursos originales
build.bat               genera el .exe
```

## Editar niveles

Cada nivel está en `src/levels/level_N.py` y se diseña con funciones legibles:

```python
b.ground(0, 62)          # suelo de la columna 0 a la 62
b.row(19, 9, "B?BMB")    # ladrillo, bonus moneda, ladrillo, bonus cristal, ladrillo
b.enemy(24)              # slime  (b.enemy(30, "K") = erizo)
b.stairs_up(116, 4)      # escalera
b.door(180)              # meta
```

Ver la leyenda completa en `src/levels/builder.py`.

## Regenerar gráficos y sonidos

```powershell
python tools\generate_assets.py
```

Para usar arte propio basta con reemplazar el PNG/WAV con el mismo nombre en `assets/`.

## Generar el .exe

```powershell
.\.venv\Scripts\Activate.ps1
.\build.bat
```

Resultado: `dist\AventuraPixel.exe` (incluye Python, Pygame, recursos e icono).
