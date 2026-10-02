# Tipo de dato: memoryview (vista de memoria sin copiar datos)
buffer = bytearray(b"ABCDEF")
vista = memoryview(buffer)
vista[0] = ord("Z")

print(vista, type(vista))
print(vista[1:3].tobytes(), buffer)
