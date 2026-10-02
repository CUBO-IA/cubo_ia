# Tipo de dato: dict (diccionarios clave-valor)
persona = {"nombre": "Fernando", "edad": 30, "pais": "El Salvador"}
persona["profesion"] = "Ingeniero"

print(persona, type(persona))
print("Nombre:", persona["nombre"])
for clave, valor in persona.items():
    print(clave, "->", valor)
