
# Calculo de la Funcion Objetivo
def funcion_objetivo(matriz_de_costos, ruta):
    cd, tiendas = ruta
    # Si no hay tiendas, costo es 0
    if not tiendas:
        return 0

    costo_total = matriz_de_costos[cd][tiendas[0]] # Inicializa con la ida a la primera tienda

    # Suma entre tiendas
    for i in range(len(tiendas) - 1):
        origen = tiendas[i]
        destino = tiendas[i + 1]
        costo_total += matriz_de_costos[origen][destino]

    # Regreso al centro de distribucion
    costo_total += matriz_de_costos[tiendas[-1]][cd]

    return costo_total

# Imprimir una ruta y su costo segun su area de distribucion
def imprimir_ruta(matriz_de_costos, ruta):
    valor = funcion_objetivo(matriz_de_costos, ruta)
    cd = ruta[0]
    tiendas = ruta[1]
    print(f"Ruta area de distribucion {cd}: {tiendas} -> Costo total: {valor:.4f}")

# Funcion generadora de vecinos por swapeo
def generar_swaps(ruta):
    cd, tiendas = ruta
    vecinos = []
    n = len(tiendas)

    if n < 2:
        return []

    # Swaps consecutivos
    for i in range(n - 1):
        nueva = tiendas.copy()
        nueva[i], nueva[i + 1] = nueva[i + 1], nueva[i]
        vecinos.append((cd, nueva))

    # Swap primero y ultimo
    nueva = tiendas.copy()
    nueva[0], nueva[-1] = nueva[-1], nueva[0]
    vecinos.append((cd, nueva))

    return vecinos

def rutas_iguales(ruta_1, ruta_2):
    return ruta_1 == ruta_2


# Calculo de la Funcion Objetivo
def funcion_objetivo(matriz_de_costos, ruta):
    cd, tiendas = ruta
    # Si no hay tiendas, costo es 0
    if not tiendas:
        return 0

    costo_total = matriz_de_costos[cd][tiendas[0]] # Inicializa con la ida a la primera tienda

    # Suma entre tiendas
    for i in range(len(tiendas) - 1):
        origen = tiendas[i]
        destino = tiendas[i + 1]
        costo_total += matriz_de_costos[origen][destino]

    # Regreso al centro de distribucion
    costo_total += matriz_de_costos[tiendas[-1]][cd]

    return costo_total

# Imprimir una ruta y su costo segun su area de distribucion
def imprimir_ruta(matriz_de_costos, ruta):
    valor = funcion_objetivo(matriz_de_costos, ruta)
    cd = ruta[0]
    tiendas = ruta[1]
    print(f"Ruta area de distribucion {cd}: {tiendas} -> Costo total: {valor:.4f}")

# Funcion generadora de vecinos por swapeo
def generar_swaps(ruta):
    cd, tiendas = ruta
    vecinos = []
    n = len(tiendas)

    if n < 2:
        return []

    # Swaps consecutivos
    for i in range(n - 1):
        nueva = tiendas.copy()
        nueva[i], nueva[i + 1] = nueva[i + 1], nueva[i]
        vecinos.append((cd, nueva))

    # Swap primero y ultimo
    nueva = tiendas.copy()
    nueva[0], nueva[-1] = nueva[-1], nueva[0]
    vecinos.append((cd, nueva))

    return vecinos

def rutas_iguales(ruta_1, ruta_2):
    return ruta_1 == ruta_2