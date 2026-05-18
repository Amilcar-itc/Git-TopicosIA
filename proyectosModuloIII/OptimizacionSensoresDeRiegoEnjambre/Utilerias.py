import os
import random
import pandas as pd
import math


def cargar_dataset(verbose=False):
    """
    Carga el archivo Dataset_Enjambre.xlsx ubicado en la misma carpeta
    que este archivo (Utilerias.py), sin depender del directorio desde
    el cual se ejecute Python.

    Parámetros:
        verbose (bool): Si es True, imprime la tabla cargada.

    Retorna:
        pandas.DataFrame: Dataset cargado desde el archivo Excel.
    """

    # Obtener la ruta absoluta de la carpeta donde está Utilerias.py
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta completa al archivo Excel
    ruta_archivo = os.path.join(carpeta_actual, "Dataset_Enjambre.xlsx")

    # Verificar que el archivo exista
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"No se encontró el archivo:\n{ruta_archivo}"
        )

    # Leer el archivo Excel
    dataset = pd.read_excel(ruta_archivo)

    # Imprimir el dataset si se solicita
    if verbose:
        print("\n=== DATASET CARGADO ===")
        print(f"Archivo: {ruta_archivo}\n")
        print(dataset)

    # Regresar el DataFrame
    return dataset

def generar_enjambre(n_particulas, n_sensores, dataset, verbose=False):
    """
    Genera el enjambre inicial para el algoritmo PSO.

    Parámetros:
        n_particulas (int): Número de partículas del enjambre.
        n_sensores (int): Número de sensores por partícula.
        dataset (DataFrame): Tabla cargada con pandas.
        verbose (bool): Si es True, imprime las partículas generadas.

    Retorna:
        list: Enjambre con la estructura:

        enjambre = [
            particula,
            ...
        ]

        particula = [
            posicion_actual,
            velocidad,
            optimo_local
        ]

        posicion_actual = [
            vector_variables,
            valor_fitness
        ]

        optimo_local = [
            vector_variables,
            valor_fitness
        ]
    """

    # Obtener límites del mapa a partir del dataset
    menor_x = dataset["Latitud"].min()
    mayor_x = dataset["Latitud"].max()

    menor_y = dataset["Longitud"].min()
    mayor_y = dataset["Longitud"].max()

    # Rangos utilizados para inicializar velocidades pequeñas
    rango_x = mayor_x - menor_x
    rango_y = mayor_y - menor_y

    # Lista principal del enjambre
    enjambre = []

    # Generar partículas
    for _ in range(n_particulas):

        # Vector de variables [x1, y1, x2, y2, ...]
        vector_variables = []

        # Vector de velocidad [vx1, vy1, vx2, vy2, ...]
        vector_velocidad = []

        # Generar sensores
        for _ in range(n_sensores):

            # Posición aleatoria dentro del mapa
            px = (rango_x * random.random()) + menor_x
            py = (rango_y * random.random()) + menor_y

            # Velocidad aleatoria pequeña (puede ser positiva o negativa)
            vx = (random.random() * 2 - 1) * rango_x * 0.1
            vy = (random.random() * 2 - 1) * rango_y * 0.1

            # Guardar posición
            vector_variables.append(px)
            vector_variables.append(py)

            # Guardar velocidad
            vector_velocidad.append(vx)
            vector_velocidad.append(vy)

        # Fitness inicial
        valor_fitness = 0.0

        # Posición actual = [variables, fitness]
        posicion_actual = [
            vector_variables,
            valor_fitness
        ]

        # Óptimo local = copia de la posición inicial
        optimo_local = [
            vector_variables.copy(),
            valor_fitness
        ]

        # Partícula = [posición_actual, velocidad, óptimo_local]
        particula = [
            posicion_actual,
            vector_velocidad,
            optimo_local
        ]

        # Agregar al enjambre
        enjambre.append(particula)

    # Impresión opcional
    if verbose:
        print("\n=== ENJAMBRE GENERADO ===\n")

        for i, particula in enumerate(enjambre, start=1):
            print(f"Partícula {i}")
            print("x,y")

            vector = particula[0][0]  # posición_actual -> vector_variables

            for j in range(n_sensores):
                x = vector[2 * j]
                y = vector[2 * j + 1]
                print(f"{x:.6f}, {y:.6f}")

            print()

    return enjambre


class FuncionFitness:
    """
    Objeto encargado de evaluar partículas del algoritmo PSO.
    """

    def __init__(
        self,
        dataset,
        #peso_humedad=1.0,
        peso_temperatura=1.0,
        peso_salinidad=1.0,
        peso_cultivo=1.0,
        peso_maiz=1.0,
        peso_chile=1.0,
        peso_tomate=1.0
    ):

        self.dataset = dataset

        # Pesos generales
        #self.peso_humedad = peso_humedad
        self.peso_temperatura = peso_temperatura
        self.peso_salinidad = peso_salinidad
        self.peso_cultivo = peso_cultivo

        # Sub pesos por cultivo
        self.peso_maiz = peso_maiz
        self.peso_chile = peso_chile
        self.peso_tomate = peso_tomate

    # ============================================================
    # FUNCIÓN PRINCIPAL
    # ============================================================

    def evaluar_particula(self, vector_variables, verbose=False):
        """
        Evalúa una partícula.

        Parámetros:
            vector_variables:
                [x1, y1, x2, y2, ...]

            verbose:
                imprime información de sensores

        Retorna:
            [fitness, promedios]
        """

        sensores = []

        suma_fitness = 0.0

        suma_humedad = 0.0
        suma_temperatura = 0.0
        suma_salinidad = 0.0

        n_sensores = len(vector_variables) // 2

        # ========================================================
        # EVALUAR SENSORES
        # ========================================================

        for i in range(n_sensores):

            sx = vector_variables[i * 2]
            sy = vector_variables[i * 2 + 1]

            datos_sensor = self.estimar_sensor(sx, sy)

            sensores.append(datos_sensor)

            suma_fitness += datos_sensor["fitness"]

            suma_humedad += datos_sensor["humedad"]
            suma_temperatura += datos_sensor["temperatura"]
            suma_salinidad += datos_sensor["salinidad"]

        # ========================================================
        # PROMEDIOS DE LA PARTÍCULA
        # ========================================================

        promedio_humedad = suma_humedad / n_sensores
        promedio_temperatura = suma_temperatura / n_sensores
        promedio_salinidad = suma_salinidad / n_sensores

        promedios = {
            "humedad": promedio_humedad,
            "temperatura": promedio_temperatura,
            "salinidad": promedio_salinidad
        }

        # ========================================================
        # VERBOSE
        # ========================================================

        if verbose:

            print("\n=== EVALUACIÓN DE PARTÍCULA ===\n")

            for i, sensor in enumerate(sensores, start=1):

                print(f"Sensor {i}")

                print(
                    f"Posición: "
                    f"({sensor['x']:.6f}, {sensor['y']:.6f})"
                )

                print(
                    f"Humedad: "
                    f"{sensor['humedad']:.4f}"
                )

                print(
                    f"Temperatura: "
                    f"{sensor['temperatura']:.4f}"
                )

                print(
                    f"Salinidad: "
                    f"{sensor['salinidad']:.4f}"
                )

                print(
                    f"Fitness sensor: "
                    f"{sensor['fitness']:.4f}"
                )

                print()

            print("PROMEDIOS DE PARTÍCULA")

            print(
                f"Humedad promedio: "
                f"{promedio_humedad:.4f}"
            )

            print(
                f"Temperatura promedio: "
                f"{promedio_temperatura:.4f}"
            )

            print(
                f"Salinidad promedio: "
                f"{promedio_salinidad:.4f}"
            )

            print(
                f"\nFITNESS TOTAL: "
                f"{suma_fitness:.4f}\n"
            )

        return [suma_fitness, promedios]

    # ============================================================
    # ESTIMAR SENSOR
    # ============================================================

    def estimar_sensor(self, sx, sy):

        suma_pesos = 0.0

        suma_humedad = 0.0
        suma_temperatura = 0.0
        suma_salinidad = 0.0

        suma_cultivo = 0.0

        # ========================================================
        # RECORRER DATASET
        # ========================================================

        for _, cultivo in self.dataset.iterrows():

            cx = cultivo["Latitud"]
            cy = cultivo["Longitud"]

            distancia = self.calcular_distancia(
                sx, sy,
                cx, cy
            )

            # Evitar división entre cero
            peso_distancia = 1 / (distancia + 0.000001)

            # Variables numéricas
            humedad = cultivo["Humedad (%)"]
            temperatura = cultivo["Temperatura (°C)"]
            salinidad = cultivo["Salinidad (dS/m)"]

            # Peso de cultivo
            cultivo_str = str(cultivo["Cultivo"]).lower()

            peso_cultivo = self.obtener_peso_cultivo(
                cultivo_str
            )

            peso_total = (
                peso_distancia *
                peso_cultivo
            )

            suma_pesos += peso_total

            suma_humedad += humedad * peso_total

            suma_temperatura += temperatura * peso_total

            suma_salinidad += salinidad * peso_total

            suma_cultivo += peso_cultivo

        # ========================================================
        # PROMEDIOS PONDERADOS
        # ========================================================

        promedio_humedad = suma_humedad / suma_pesos

        promedio_temperatura = (
            suma_temperatura / suma_pesos
        )

        promedio_salinidad = (
            suma_salinidad / suma_pesos
        )

        promedio_cultivo = (
            suma_cultivo / len(self.dataset)
        )

        # ========================================================
        # FITNESS DEL SENSOR
        # ========================================================

        fitness = 0.0

        """fitness += (
            promedio_humedad *
            self.peso_humedad
        ) """

        fitness += (
            promedio_temperatura *
            self.peso_temperatura
        )

        fitness += (
            promedio_salinidad *
            self.peso_salinidad
        )

        fitness += (
            promedio_cultivo *
            self.peso_cultivo
        )

        return {
            "x": sx,
            "y": sy,
            "humedad": promedio_humedad,
            "temperatura": promedio_temperatura,
            "salinidad": promedio_salinidad,
            "fitness": fitness
        }

    # ============================================================
    # PESO POR CULTIVO
    # ============================================================

    def obtener_peso_cultivo(self, cultivo):

        if "maiz" in cultivo:
            return self.peso_maiz

        if "chile" in cultivo:
            return self.peso_chile

        if "tomate" in cultivo:
            return self.peso_tomate

        return 1.0

    # ============================================================
    # DISTANCIA EUCLIDIANA
    # ============================================================

    def calcular_distancia(
        self,
        x1, y1,
        x2, y2
    ):

        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

def evaluar_enjambre(enjambre, fitness, verbose=False):
    """
    Evalúa todas las partículas del enjambre utilizando el objeto
    FuncionFitness.

    Parámetros:
        enjambre (list): Lista de partículas.
        fitness (FuncionFitness): Objeto ya instanciado.
        verbose (bool): Si es True, imprime un resumen por partícula.

    Retorna:
        optimo_enjambre = [
            vector_variables,
            valor_fitness
        ]

    Notas:
        - El objetivo es maximizar el fitness.
        - Se actualiza:
            * partícula.posición_actual.valor_fitness
            * partícula.óptimo_local si la posición actual es mejor
    """

    # Mejor solución del enjambre
    mejor_indice = -1
    mejor_fitness = float("-inf")
    mejor_variables = None

    # ============================================================
    # RECORRER PARTÍCULAS
    # ============================================================

    for i, particula in enumerate(enjambre):

        # --------------------------------------------------------
        # Obtener vector de variables de la posición actual
        # --------------------------------------------------------
        vector_variables = particula[0][0]

        # --------------------------------------------------------
        # Evaluar partícula (sin verbose interno)
        # --------------------------------------------------------
        valor_fitness, promedios = fitness.evaluar_particula(
            vector_variables,
            verbose=False
        )

        # --------------------------------------------------------
        # Guardar fitness en la posición actual
        # --------------------------------------------------------
        particula[0][1] = valor_fitness

        # --------------------------------------------------------
        # Actualizar óptimo local (pbest)
        # --------------------------------------------------------
        if valor_fitness > particula[2][1]:
            particula[2][0] = vector_variables.copy()
            particula[2][1] = valor_fitness

        # --------------------------------------------------------
        # Actualizar mejor partícula del enjambre
        # --------------------------------------------------------
        if valor_fitness > mejor_fitness:
            mejor_indice = i
            mejor_fitness = valor_fitness
            mejor_variables = vector_variables.copy()

        # --------------------------------------------------------
        # Impresión opcional
        # --------------------------------------------------------
        if verbose:
            print(f"\nPartícula {i + 1}")
            print(f"Humedad promedio:     {promedios['humedad']:.4f}")
            print(f"Temperatura promedio: {promedios['temperatura']:.4f}")
            print(f"Salinidad promedio:   {promedios['salinidad']:.4f}")
            print(f"Fitness:              {valor_fitness:.4f}")

    # ============================================================
    # CREAR ÓPTIMO DEL ENJAMBRE
    # ============================================================

    optimo_enjambre = [
        mejor_variables,
        mejor_fitness
    ]

    # ============================================================
    # IMPRESIÓN FINAL
    # ============================================================

    if verbose:
        print("\n========================================")
        print("MEJOR PARTÍCULA DEL ENJAMBRE")
        print("========================================")
        print(f"Número de partícula: {mejor_indice + 1}")
        print(f"Fitness:             {mejor_fitness:.4f}")

    return optimo_enjambre

class MovimientoParticulas:

    def __init__(
        self,
        w,
        c1,
        c2,
        n_sensores
    ):

        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.n_sensores = n_sensores

    # ============================================================
    # DISTANCIA EUCLIDIANA
    # ============================================================

    def calcular_distancia(
        self,
        x1, y1,
        x2, y2
    ):

        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

    # ============================================================
    # CALCULAR PRIORIDAD
    # ============================================================

    def calcular_prioridad(
        self,
        px,
        py,
        vector_sensores_vecinos
    ):

        distancia_1 = float("inf")
        distancia_2 = float("inf")

        indice_1 = -1

        for sensor in vector_sensores_vecinos:

            indice = sensor[0]
            sx = sensor[1]
            sy = sensor[2]

            distancia = self.calcular_distancia(
                px, py,
                sx, sy
            )

            if distancia < distancia_1:

                distancia_2 = distancia_1
                distancia_1 = distancia
                indice_1 = indice

            elif distancia < distancia_2:

                distancia_2 = distancia

        if distancia_2 == float("inf"):
            prioridad = 999999.0
        else:
            prioridad = distancia_2 - distancia_1

        return [indice_1, prioridad]

    # ============================================================
    # IMPRIMIR ÓPTIMO SOCIAL
    # ============================================================

    def imprimir_optimo_social(
        self,
        vector_comparado
    ):

        print("\n========================================")
        print("ÓPTIMO SOCIAL")
        print("========================================")

        print(
            f"{'Índice':<10}"
            f"{'X':<18}"
            f"{'Y':<18}"
        )

        for i in range(self.n_sensores):

            x = vector_comparado[i * 2]
            y = vector_comparado[i * 2 + 1]

            print(
                f"{i:<10}"
                f"{x:<18.6f}"
                f"{y:<18.6f}"
            )

    # ============================================================
    # IMPRIMIR TABLA SIMPLE
    # ============================================================

    def imprimir_tabla_particula(
        self,
        vector_posicion,
        vector_velocidad,
        vector_local,
        titulo
    ):

        print("\n========================================")
        print(titulo)
        print("========================================")

        print(
            f"{'Sensor':<10}"
            f"{'PX':<14}"
            f"{'PY':<14}"
            f"{'LBEST_X':<14}"
            f"{'LBEST_Y':<14}"
            f"{'VX':<14}"
            f"{'VY':<14}"
        )

        for i in range(self.n_sensores):

            px = vector_posicion[i * 2]
            py = vector_posicion[i * 2 + 1]

            lpx = vector_local[i * 2]
            lpy = vector_local[i * 2 + 1]

            vx = vector_velocidad[i * 2]
            vy = vector_velocidad[i * 2 + 1]

            print(
                f"{i:<10}"
                f"{px:<14.6f}"
                f"{py:<14.6f}"
                f"{lpx:<14.6f}"
                f"{lpy:<14.6f}"
                f"{vx:<14.6f}"
                f"{vy:<14.6f}"
            )

    # ============================================================
    # ORDENAR PARTÍCULA
    # ============================================================

    def ordenar_particula(
        self,
        vector_posicion,
        vector_velocidad,
        vector_comparado,
        verbose=False,
        titulo="PARTÍCULA"
    ):

        vector_auxiliar = []
        vector_comparado_auxiliar = []

        for i in range(self.n_sensores):

            px = vector_posicion[i * 2]
            py = vector_posicion[i * 2 + 1]

            if vector_velocidad is not None:

                vx = vector_velocidad[i * 2]
                vy = vector_velocidad[i * 2 + 1]

            else:

                vx = 0.0
                vy = 0.0

            pcx = vector_comparado[i * 2]
            pcy = vector_comparado[i * 2 + 1]

            vector_auxiliar.append([
                0,
                0,
                px,
                py,
                vx,
                vy
            ])

            vector_comparado_auxiliar.append([
                i,
                pcx,
                pcy
            ])

        vector_ordenado = []

        while len(vector_auxiliar) > 0:

            for sensor in vector_auxiliar:

                resultado = self.calcular_prioridad(
                    sensor[2],
                    sensor[3],
                    vector_comparado_auxiliar
                )

                sensor[0] = resultado[0]
                sensor[1] = resultado[1]

            mejor_sensor = max(
                vector_auxiliar,
                key=lambda s: s[1]
            )

            nuevo_indice = mejor_sensor[0]

            vector_ordenado.append([
                nuevo_indice,
                mejor_sensor[2],
                mejor_sensor[3],
                mejor_sensor[4],
                mejor_sensor[5]
            ])

            vector_auxiliar.remove(mejor_sensor)

            vector_comparado_auxiliar = [
                sensor
                for sensor in vector_comparado_auxiliar
                if sensor[0] != nuevo_indice
            ]

        vector_ordenado.sort(
            key=lambda sensor: sensor[0]
        )

        vector_variables = []
        vector_velocidades = []

        for sensor in vector_ordenado:

            px = sensor[1]
            py = sensor[2]

            vx = sensor[3]
            vy = sensor[4]

            vector_variables.append(px)
            vector_variables.append(py)

            vector_velocidades.append(vx)
            vector_velocidades.append(vy)

        return [
            vector_variables,
            vector_velocidades
        ]

    # ============================================================
    # ORDENAR PARTÍCULA COMPLETA
    # ============================================================

    def ordenar_particula_completa(
        self,
        particula,
        optimo_social,
        verbose=False
    ):

        resultado_actual = self.ordenar_particula(
            particula[0][0],
            particula[1],
            optimo_social[0],
            verbose=False
        )

        resultado_local = self.ordenar_particula(
            particula[2][0],
            None,
            optimo_social[0],
            verbose=False
        )

        nueva_particula = [

            [
                resultado_actual[0],
                particula[0][1]
            ],

            resultado_actual[1],

            [
                resultado_local[0],
                particula[2][1]
            ]
        ]

        return nueva_particula

    # ============================================================
    # MOVIMIENTO PSO
    # ============================================================

    def movimiento(
        self,
        particula,
        optimo_social,
        verbose=False
    ):

        # ========================================================
        # IMPRIMIR TABLA ORIGINAL
        # ========================================================

        if verbose:

            self.imprimir_tabla_particula(
                particula[0][0],
                particula[1],
                particula[2][0],
                "PARTÍCULA ORIGINAL"
            )

        # ========================================================
        # ORDENAR PARTÍCULA
        # ========================================================

        particula_ordenada = self.ordenar_particula_completa(
            particula,
            optimo_social,
            verbose=False
        )

        posicion_actual = particula_ordenada[0][0]
        velocidad_actual = particula_ordenada[1]
        optimo_local = particula_ordenada[2][0]

        # ========================================================
        # IMPRIMIR TABLA ORDENADA
        # ========================================================

        if verbose:

            self.imprimir_tabla_particula(
                posicion_actual,
                velocidad_actual,
                optimo_local,
                "PARTÍCULA ORDENADA"
            )

        # ========================================================
        # NUEVOS VECTORES
        # ========================================================

        nueva_posicion = []
        nueva_velocidad = []

        # ========================================================
        # TABLA DE MOVIMIENTO
        # ========================================================

        if verbose:

            print("\n==============================================================")
            print("APLICACIÓN DE MOVIMIENTO")
            print("==============================================================")

            print(
                f"{'Var':<6}"
                f"{'X(t)':<12}"
                f"{'w*v':<12}"
                f"{'c1*r1*(pbest-x)':<22}"
                f"{'c2*r2*(gbest-x)':<22}"
                f"{'V(t+1)':<14}"
                f"{'X(t+1)':<14}"
            )

        # ========================================================
        # RECORRER VARIABLES
        # ========================================================

        for i in range(len(posicion_actual)):

            xt = posicion_actual[i]
            vt = velocidad_actual[i]

            pbest = optimo_local[i]
            gbest = optimo_social[0][i]

            r1 = random.random()
            r2 = random.random()

            # ----------------------------------------------------
            # COMPONENTES
            # ----------------------------------------------------

            componente_inercia = self.w * vt

            componente_cognitivo = (
                self.c1 *
                r1 *
                (pbest - xt)
            )

            componente_social = (
                self.c2 *
                r2 *
                (gbest - xt)
            )

            # ----------------------------------------------------
            # NUEVA VELOCIDAD
            # ----------------------------------------------------

            nueva_v = (
                componente_inercia +
                componente_cognitivo +
                componente_social
            )

            # ----------------------------------------------------
            # NUEVA POSICIÓN
            # ----------------------------------------------------

            nueva_x = xt + nueva_v

            nueva_velocidad.append(nueva_v)
            nueva_posicion.append(nueva_x)

            # ----------------------------------------------------
            # VERBOSE
            # ----------------------------------------------------

            if verbose:

                nombre_variable = (
                    f"S{i//2 + 1}-X"
                    if i % 2 == 0
                    else f"S{i//2 + 1}-Y"
                )

                print(
                    f"{nombre_variable:<6}"
                    f"{xt:<12.6f}"
                    f"{componente_inercia:<12.6f}"
                    f"{componente_cognitivo:<22.6f}"
                    f"{componente_social:<22.6f}"
                    f"{nueva_v:<14.6f}"
                    f"{nueva_x:<14.6f}"
                )

        # ========================================================
        # RECONSTRUIR PARTÍCULA
        # ========================================================

        nueva_particula = [

            [
                nueva_posicion,
                particula[0][1]
            ],

            nueva_velocidad,

            [
                optimo_local,
                particula[2][1]
            ]
        ]

        return nueva_particula