from Utilerias.FuncionesDeRepresentacion import generar_matriz_costos, generar_areas_de_distribucion
from Utilerias.FuncionesDeMapeo import imprimir_ruta
from Utilerias.FuncionesDeOptimizacion import recosido_simulado

import matplotlib.pyplot as plt

costos = generar_matriz_costos()
rutas = generar_areas_de_distribucion()

# Seleccion manual de ruta
r = 9
ruta = rutas[r]

print(f"\n==============================")
print(f"Área de distribución {r}")
print(f"==============================\n")

print("Ruta inicial:")
imprimir_ruta(costos, ruta)

temperatura = 500
alpha = 0.98
iteraciones = 500

mejor_ruta, historial = recosido_simulado(
    costos,
    ruta,
    temperatura,
    alpha,
    iteraciones
)

print("\nRuta optimizada:")
imprimir_ruta(costos, mejor_ruta)

# Grafica
plt.figure()
plt.plot(historial, marker='o', linestyle='-', color='red')
plt.title(f"Evolución de costo - Área {r}")
plt.xlabel("Iteraciones")
plt.ylabel("Costo")
plt.show()