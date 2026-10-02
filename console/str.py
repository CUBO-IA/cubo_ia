# Tipo de dato: str (cadenas de texto)
nombre = "Fernando"
frase = 'Hola mundo'
multilinea = """Texto
en varias líneas"""
formateado = f"Hola, {nombre}"

for v in (nombre, frase, multilinea, formateado):
    print(repr(v), type(v))
print(nombre.upper(), nombre[0], nombre[::-1], len(nombre))
