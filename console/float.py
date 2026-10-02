# Tipo de dato: float (punto flotante)
precio = 19.99
temperatura = -3.5
cientifico = 1.5e3    # 1500.0
infinito = float("inf")
no_numero = float("nan")

for v in (precio, temperatura, cientifico, infinito, no_numero):
    print(v, type(v))
