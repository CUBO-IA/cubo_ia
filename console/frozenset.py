# Tipo de dato: frozenset (conjunto inmutable)
vocales = frozenset("aeiou")

print(vocales, type(vocales))
print("'a' en vocales:", "a" in vocales)
# vocales.add("y")  -> AttributeError: es inmutable
