from Utilerias import (
    cargar_dataset,
    generar_enjambre,
    evaluar_enjambre,
    FuncionFitness,
    MovimientoParticulas
)

import matplotlib.pyplot as plt


def main():

    # ============================================================
    # CONFIGURACIÓN FITNESS
    # ============================================================

    n_sensores = 25

    peso_temperatura = 0.3
    peso_salinidad = -0.5
    peso_cultivo = 0.4

    peso_maiz = 1.0
    peso_chile = 1.5
    peso_tomate = 0.8

    # ============================================================
    # CONFIGURACIÓN PSO
    # ============================================================

    n_particulas = 10
    iteraciones = 100

    w = 0.7
    c1 = 1.5
    c2 = 1.5

    # ============================================================
    # CARGAR DATASET
    # ============================================================

    dataset = cargar_dataset(
        verbose=False
    )

    # ============================================================
    # OBJETO FITNESS
    # ============================================================

    fitness = FuncionFitness(

        dataset=dataset,

        peso_temperatura=peso_temperatura,
        peso_salinidad=peso_salinidad,

        peso_cultivo=peso_cultivo,

        peso_maiz=peso_maiz,
        peso_chile=peso_chile,
        peso_tomate=peso_tomate
    )

    # ============================================================
    # OBJETO MOVIMIENTO
    # ============================================================

    movimiento = MovimientoParticulas(
        w=w,
        c1=c1,
        c2=c2,
        n_sensores=n_sensores
    )

    # ============================================================
    # GENERAR ENJAMBRE
    # ============================================================

    print("\n==================================================")
    print("GENERANDO ENJAMBRE")
    print("==================================================")

    enjambre = generar_enjambre(
        n_particulas=n_particulas,
        n_sensores=n_sensores,
        dataset=dataset,
        verbose=False
    )

    # ============================================================
    # EVALUACIÓN INICIAL
    # ============================================================

    print("\n==================================================")
    print("EVALUACIÓN INICIAL")
    print("==================================================")

    optimo_enjambre = evaluar_enjambre(
        enjambre,
        fitness,
        verbose=True
    )

    # ============================================================
    # ÓPTIMO SOCIAL INICIAL
    # ============================================================

    optimo_social = [
        optimo_enjambre[0][:],
        optimo_enjambre[1]
    ]

    # ============================================================
    # HISTORIAL FITNESS
    # ============================================================

    historial_fitness = [
        optimo_enjambre[1]
    ]

    mejor_fitness_inicial = optimo_enjambre[1]

    # ============================================================
    # ITERACIONES DEL ALGORITMO
    # ============================================================

    for iteracion in range(iteraciones):
        # --------------------------------------------------------
        # MOVER PARTÍCULAS
        # --------------------------------------------------------

        for i in range(len(enjambre)):

            enjambre[i] = movimiento.movimiento(
                enjambre[i],
                optimo_social,
                verbose=False
            )

        # --------------------------------------------------------
        # EVALUAR ENJAMBRE
        # --------------------------------------------------------

        optimo_enjambre = evaluar_enjambre(
            enjambre,
            fitness,
            verbose=False
        )

        historial_fitness.append(
            optimo_enjambre[1]
        )

        # --------------------------------------------------------
        # MOSTRAR RESULTADOS ITERACIÓN
        # --------------------------------------------------------

        print(
            f"ITERACIÓN {iteracion + 1}"" - Mejor fitness del enjambre: "
            f"{optimo_enjambre[1]:.6f}"
        )

        # --------------------------------------------------------
        # ACTUALIZAR ÓPTIMO SOCIAL
        # --------------------------------------------------------

        if optimo_enjambre[1] > optimo_social[1]:

            print("Nuevo óptimo social encontrado")

            optimo_social = [
                optimo_enjambre[0][:],
                optimo_enjambre[1]
            ]
    # ============================================================
    # RESULTADO FINAL
    # ============================================================

    print("\n==================================================")
    print("RESULTADO FINAL")
    print("==================================================")

    print(
        f"\nFitness óptimo global: "
        f"{optimo_social[1]:.6f}"
    )
        # ============================================================
    # EVALUAR PARTÍCULA GANADORA
    # ============================================================

    # La función evaluar_particula devuelve exactamente:
    # [
    #     suma_fitness,
    #     {
    #         "humedad": ...,
    #         "temperatura": ...,
    #         "salinidad": ...
    #     }
    # ]
    #
    # No devuelve la lista de sensores, por lo que para mostrar la
    # tabla final se vuelve a estimar cada sensor individualmente.

    resultado_final = fitness.evaluar_particula(
        optimo_social[0],
        verbose=False
    )

    # ------------------------------------------------------------
    # EXTRAER RESULTADOS GLOBALES
    # ------------------------------------------------------------

    fitness_total = resultado_final[0]

    promedios_particula = resultado_final[1]

    humedad_promedio = promedios_particula["humedad"]
    temperatura_promedio = promedios_particula["temperatura"]
    salinidad_promedio = promedios_particula["salinidad"]

    # ============================================================
    # TABLA DE SENSORES
    # ============================================================

    print("\n==================================================")
    print("SENSORES GANADORES")
    print("==================================================")

    print(
        f"{'Sensor':<10}"
        f"{'X':<14}"
        f"{'Y':<14}"
        f"{'Humedad':<14}"
        f"{'Temp':<14}"
        f"{'Salinidad':<14}"
        f"{'Fitness':<14}"
    )

    suma_fitness = 0.0

    n_sensores_final = len(optimo_social[0]) // 2

    for i in range(n_sensores_final):

        # Coordenadas del sensor
        x = optimo_social[0][i * 2]
        y = optimo_social[0][i * 2 + 1]

        # Recalcular los valores del sensor
        datos_sensor = fitness.estimar_sensor(x, y)

        humedad = datos_sensor["humedad"]
        temperatura = datos_sensor["temperatura"]
        salinidad = datos_sensor["salinidad"]
        fitness_sensor = datos_sensor["fitness"]

        suma_fitness += fitness_sensor

        print(
            f"{i + 1:<10}"
            f"{x:<14.6f}"
            f"{y:<14.6f}"
            f"{humedad:<14.4f}"
            f"{temperatura:<14.4f}"
            f"{salinidad:<14.4f}"
            f"{fitness_sensor:<14.4f}"
        )

    # ============================================================
    # PROMEDIOS FINALES
    # ============================================================

    print("\n==================================================")
    print("PROMEDIOS FINALES")
    print("==================================================")

    print(
        f"Humedad promedio:     "
        f"{humedad_promedio:.4f}"
    )

    print(
        f"Temperatura promedio: "
        f"{temperatura_promedio:.4f}"
    )

    print(
        f"Salinidad promedio:   "
        f"{salinidad_promedio:.4f}"
    )

    print(
        f"Fitness total:        "
        f"{fitness_total:.4f}"
    )

    print(
        f"Sumatoria fitness:    "
        f"{suma_fitness:.4f}"
    )

    # ============================================================
    # CRECIMIENTO / DECRECIMIENTO
    # ============================================================

    cambio_porcentual = (
        (
            optimo_social[1] -
            mejor_fitness_inicial
        )
        / abs(mejor_fitness_inicial)
    ) * 100

    print(
        f"Cambio porcentual respecto "
        f"al inicio: {cambio_porcentual:.2f}%"
    )

    # ============================================================
    # GRÁFICA
    # ============================================================

    plt.figure(figsize=(10, 5))

    plt.plot(
        historial_fitness,
        marker='o'
    )

    plt.title("Historial Fitness")
    plt.xlabel("Iteración")
    plt.ylabel("Fitness")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()