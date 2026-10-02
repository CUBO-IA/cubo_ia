# Tipo de dato: list (listas, mutables y ordenadas)
numeros = [1, 2, 3, 4]
mixta = [1, "dos", 3.0, True]
numeros.append(5)
numeros[0] = 10

print(numeros, type(numeros))
print(mixta, type(mixta))
print("Primero:", numeros[0], "Rebanada:", numeros[1:3])
