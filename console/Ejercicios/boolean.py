# Tipo de dato: bool (booleanos)

# --- Ejemplos básicos ---
activo = True
inactivo = False
comparacion = 5 > 3

print(activo, type(activo))
print(inactivo, type(inactivo))
print(comparacion, type(comparacion))
print(bool(0), bool(""), bool([]), bool(1), bool("a"))

# --- Ejercicio funcional: pedir nombre y edad por consola ---
nombre = input("Ingrese su nombre: ")
edad = int(input("Ingrese su edad: "))

# 1) Verificar si es menor de edad
es_menor = edad < 18
if es_menor:
    print(f"{nombre}, eres menor de edad.")
else:
    print(f"{nombre}, eres mayor de edad.")

# 2) Verificar si la edad es exactamente igual a 18 (resultado booleano)
es_igual_a_18 = edad == 18
print(f"¿La edad es igual a 18? {es_igual_a_18}")