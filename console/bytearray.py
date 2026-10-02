# Tipo de dato: bytearray (secuencia mutable de bytes)
buffer = bytearray(b"hola")
buffer[0] = ord("H")
buffer.append(33)  # '!'

print(buffer, type(buffer))
