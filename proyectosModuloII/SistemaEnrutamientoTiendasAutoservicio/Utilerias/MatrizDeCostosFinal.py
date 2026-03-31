import pandas as pd
import os

# La siguiente funcion multiplica las matrices de los archivos "matriz_costos_combustible" y
# "matriz_distancias" para obtener una matriz calculada que represente una matriz de costos final

def generar_matriz_costos():
    # Obtener ruta base del proyecto (sube una carpeta desde Utilerias)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construir rutas a los archivos
    ruta_costos = os.path.join(base_dir, "MaterialesDeReferencia", "matriz_costos_combustible.xlsx")
    ruta_distancias = os.path.join(base_dir, "MaterialesDeReferencia", "matriz_distancias.xlsx")

    # Leer archivos ignorando la primera fila
    matriz_costos = pd.read_excel(ruta_costos, skiprows=1, header=None)
    matriz_distancias = pd.read_excel(ruta_distancias, skiprows=1, header=None)

    # Convertir a listas
    A = matriz_costos.values
    B = matriz_distancias.values

    # Multiplica las matrices
    resultado = A * B
    """print("A[0][0]:", A[0][0])
    print("B[0][0]:", B[0][0])
    print("A[0][1]:", A[0][1])
    print("B[0][1]:", B[0][1])
    print("Resultado[0][0]:", resultado[0][0])
    print("Resultado[0][1]:", resultado[0][1])"""
    return resultado

# Llama a la funcion "generar_matriz_costos" e imprime la matriz de costos final
def imprimir_matriz_costos():
    matriz = generar_matriz_costos()

    print("Matriz de costos final:\n")
    for fila in matriz:
        print(fila)


# Calcula la prioridad con la que se va a asignar cada tienda con su centro de distribucion
def calcular_prioridades(costos, centros, tiendas):
    prioridades = []

    for tienda in tiendas:
        costos_a_centros = []

        for cd in centros:
            costos_a_centros.append((cd, costos[cd][tienda]))

        # ordenar por costo
        costos_a_centros.sort(key=lambda x: x[1])

        cd1, c1 = costos_a_centros[0]
        cd2, c2 = costos_a_centros[1]

        prioridad = c2 - c1

        prioridades.append((tienda, prioridad, costos_a_centros))

    return prioridades

# Imprime las prioridades por tienda
def imprimir_prioridades():
    # 1. Generar matriz de costos
    matriz_costos = generar_matriz_costos()
    n = len(matriz_costos)
    # 2. Definir centros y tiendas
    centros = list(range(10))           # 0 - 9
    tiendas = list(range(10, n))        # 10 - 99 (si n=100)
    # 3. Calcular prioridades
    prioridades = calcular_prioridades(matriz_costos, centros, tiendas)
    # 4. Ordenar de mayor a menor prioridad
    prioridades.sort(key=lambda x: x[1], reverse=True)
    # 5. Imprimir resultados
    print("\nPrioridades de tiendas:\n")
    for tienda, prioridad, _ in prioridades:
        print(f"Tienda {tienda} -> Prioridad: {prioridad:.4f}")

# Genera las areas de distribucion asignando las tiendas a su respectivo centro de distribución
def asignar_tiendas_a_centros(prioridades, centros, capacidad_max=14):
    asignacion = {cd: [] for cd in centros}

    for tienda, _, opciones in prioridades:
        for cd, _ in opciones:
            if len(asignacion[cd]) < capacidad_max:
                asignacion[cd].append(tienda)
                break

    return asignacion

# Imprime las asignaciones de tiendas a centros
def imprimir_asignaciones():

    matriz_costos = generar_matriz_costos()
    n = len(matriz_costos)

    # Definir centros y tiendas
    centros = list(range(10))
    tiendas = list(range(10, n))

    prioridades = calcular_prioridades(matriz_costos, centros, tiendas)
    prioridades.sort(key=lambda x: x[1], reverse=True)

    areas = asignar_tiendas_a_centros(prioridades, centros)

    print("\nÁreas de distribución:\n")
    for cd in centros:
        tiendas_asignadas = areas[cd]
        print(f"Centro {cd}: {len(tiendas_asignadas)} tiendas")

        # imprimir lista
        print(f"  Tiendas: {tiendas_asignadas}\n")

# Funcion que simplifica el proceso para devolver el vector de areas de distribucion
# Genera una estructura de datos portable sin depender del vector "centros"
def generar_areas_de_distribucion():
    matriz_costos = generar_matriz_costos()
    n = len(matriz_costos)

    # Definir centros y tiendas
    centros = list(range(10))
    tiendas = list(range(10, n))

    prioridades = calcular_prioridades(matriz_costos, centros, tiendas)
    prioridades.sort(key=lambda x: x[1], reverse=True)
    asignacion = asignar_tiendas_a_centros(prioridades, centros)

    areas = []
    for cd, tiendas_asignadas in asignacion.items():
        areas.append((cd, tiendas_asignadas))
    areas.sort(key=lambda x: x[0])
    return areas

# Funcion que devuelve el total de nodos en las areas de distribucion, debe dar 90
def validar_areas(areas):
    total = sum(len(tiendas) for _, tiendas in areas)
    print(f"Total de tiendas asignadas: {total}")

# Imprime las areas de distribucion usando su estructura de datos portable
def imprimir_areas_de_distribucion():
    areas = generar_areas_de_distribucion()
    validar_areas(areas)
    print("\nÁreas de distribución:\n")

    for cd, tiendas in areas:
        print(f"Centro {cd}: {len(tiendas)} tiendas")
        print(f"  Tiendas: {tiendas}\n")