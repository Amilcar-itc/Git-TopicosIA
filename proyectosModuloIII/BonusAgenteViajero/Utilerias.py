# ============================================================
# Utilerias.py
# ============================================================

import os


def cargar_mapa(verbose=False):
    """
    Carga el archivo Mapa.txt ubicado en la misma carpeta que este
    archivo (Utilerias.py) y lo convierte en una estructura con:

        encabezado: lista con los nombres de las ciudades.
        tabla: matriz bidimensional de números enteros.

    El archivo tiene el siguiente formato:
        - La primera fila contiene los nombres de las ciudades.
        - La primera columna de cada fila contiene el nombre de la ciudad.
        - El resto de los valores son distancias entre ciudades.

    Parámetros:
        verbose (bool): Si es True, imprime el encabezado y la tabla.

    Retorna:
        [encabezado, tabla]

        encabezado = [
            'Madrid',
            'Barcelona',
            'Valencia',
            ...
        ]

        tabla = [
            [0, 303, 442, ...],
            [303, 0, 409, ...],
            [442, 409, 0, ...],
            ...
        ]
    """

    # ========================================================
    # OBTENER RUTA DEL ARCHIVO
    # ========================================================

    carpeta_actual = os.path.dirname(
        os.path.abspath(__file__)
    )

    ruta_archivo = os.path.join(
        carpeta_actual,
        "Mapa.txt"
    )

    # ========================================================
    # VERIFICAR EXISTENCIA DEL ARCHIVO
    # ========================================================

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"No se encontró el archivo:\n{ruta_archivo}"
        )

    # ========================================================
    # LEER ARCHIVO COMPLETO
    # ========================================================

    with open(
        ruta_archivo,
        "r",
        encoding="utf-8"
    ) as archivo:

        contenido = archivo.read()

    # ========================================================
    # CONVERTIR TEXTO A MATRIZ DE CADENAS
    # ========================================================

    matriz = []

    # Cada salto de línea genera una nueva fila
    filas = contenido.strip().split("\n")

    for fila_texto in filas:

        # Eliminar espacios y saltos residuales
        fila_texto = fila_texto.strip()

        # Cada coma genera una nueva columna
        columnas = fila_texto.split(",")

        # Limpiar espacios alrededor de cada valor
        fila = []

        for valor in columnas:
            fila.append(valor.strip())

        matriz.append(fila)

    # ========================================================
    # EXTRAER ENCABEZADO
    # ========================================================

    # La primera fila tiene:
    # ['', 'Madrid', 'Barcelona', ...]
    encabezado = matriz[0][1:]

    # ========================================================
    # EXTRAER TABLA NUMÉRICA
    # ========================================================

    tabla = []

    # Se omite la primera fila
    for fila in matriz[1:]:

        # Se omite la primera columna (nombre de la ciudad)
        valores = fila[1:]

        fila_numerica = []

        for valor in valores:
            fila_numerica.append(int(valor))

        tabla.append(fila_numerica)

    # ========================================================
    # IMPRESIÓN OPCIONAL
    # ========================================================

    if verbose:

        print("\n==================================================")
        print("ENCABEZADO")
        print("==================================================")
        print(encabezado)

        print("\n==================================================")
        print("TABLA")
        print("==================================================")

        for fila in tabla:
            print(fila)

    # ========================================================
    # RETORNAR ESTRUCTURA
    # ========================================================

    return [encabezado, tabla]