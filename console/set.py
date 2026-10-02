# Tipo de dato: set (conjuntos, sin duplicados ni orden)
a = {1, 2, 3, 3}
b = {3, 4, 5}
a.add(10)

print(a, type(a))
print("Unión:", a | b)
print("Intersección:", a & b)
print("Diferencia:", a - b)
