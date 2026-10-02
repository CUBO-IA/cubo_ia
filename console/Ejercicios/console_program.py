import random

opciones = ["piedra", "papel", "tijera"]
gana_a = {"piedra": "tijera", "papel": "piedra", "tijera": "papel"}
marcador = {"jugador": 0, "pc": 0}

while True:
    jugador = input("Elige piedra, papel o tijera (o 'salir'): ").lower()
    if jugador == "salir":
        break
    if jugador not in opciones:
        print("Opción inválida.")
        continue

    pc = random.choice(opciones)
    print(f"La PC eligió: {pc}")

    if jugador == pc:
        print("Empate.")
    elif gana_a[jugador] == pc:
        print("¡Ganaste esta ronda!")
        marcador["jugador"] += 1
    else:
        print("Ganó la PC.")
        marcador["pc"] += 1

    print(f"Marcador -> Tú: {marcador['jugador']} | PC: {marcador['pc']}\n")

print("Marcador final:", marcador)