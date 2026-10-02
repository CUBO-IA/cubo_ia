# Tipo de dato: bytes (secuencia inmutable de bytes)
datos = b"Hola"
codificado = "Señal".encode("utf-8")

print(datos, type(datos))
print(codificado, type(codificado))
print(list(datos), codificado.decode("utf-8"))
