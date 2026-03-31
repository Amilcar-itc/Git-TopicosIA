import random
import math
from Utilerias.FuncionesDeMapeo import funcion_objetivo, generar_swaps


def aceptar_solucion(delta, temperatura):
    if delta < 0:
        return True
    else:
        prob = math.exp(-delta / temperatura)
        return random.random() < prob


def enfriar(temperatura, alpha):
    return temperatura * alpha


def recosido_simulado(matriz_costos, ruta_inicial,
                      temperatura_inicial=500,
                      alpha=0.98,
                      iteraciones=500,
                      vecinos_por_iteracion=5):

    ruta_actual = ruta_inicial
    mejor_ruta = ruta_actual

    costo_actual = funcion_objetivo(matriz_costos, ruta_actual)
    mejor_costo = costo_actual

    temperatura = temperatura_inicial

    historial_costos = [costo_actual]

    for _ in range(iteraciones):

        for _ in range(vecinos_por_iteracion):

            vecinos = generar_swaps(ruta_actual)
            vecino = random.choice(vecinos)

            costo_vecino = funcion_objetivo(matriz_costos, vecino)
            delta = costo_vecino - costo_actual

            if aceptar_solucion(delta, temperatura):
                ruta_actual = vecino
                costo_actual = costo_vecino

                if costo_actual < mejor_costo:
                    mejor_ruta = ruta_actual
                    mejor_costo = costo_actual

        temperatura = enfriar(temperatura, alpha)
        historial_costos.append(costo_actual)

    return mejor_ruta, historial_costos