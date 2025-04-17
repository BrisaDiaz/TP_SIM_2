import matplotlib.pyplot as plt
import math

def generar_histograma(numeros, cantidad_intervalos, titulo="Distribución de Frecuencias", etiqueta_x="Valores", etiqueta_y="Frecuencia"):
    if not numeros:
        print("No hay números para generar el histograma.")
        return

    if cantidad_intervalos is None:
        # Calcular un número de intervalos razonable si no se proporciona
        cantidad_intervalos = int(math.sqrt(len(numeros)))  # Regla de la raíz cuadrada

        # Generar el histograma con más opciones de personalización
    n, bins, patches = plt.hist(numeros, bins=cantidad_intervalos, rwidth=0.8, edgecolor='black', alpha=0.7)

    # Mostrar las marcas de las clases (límites de los intervalos) en el eje x
    plt.xticks(bins)

    # Añadir etiquetas de frecuencia encima de las barras (opcional)
    for count, rect in zip(n, patches):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 0.5, f'{int(count)}',
                 ha='center', va='bottom')

    plt.title(titulo)
    plt.xlabel(etiqueta_x)
    plt.ylabel(etiqueta_y)
    plt.grid(axis='y', linestyle='--', alpha=0.6)  # Añadir una grilla horizontal para facilitar la lectura
    plt.tight_layout()  # Ajustar el layout para evitar que las etiquetas se superpongan
    plt.show()

def mostrar_tabla(resultado_prueba, nombre_distribución):
    print("=" * 60)
    print("H0: Los numeros siguen una distribución", nombre_distribución)
    print("=" * 60)
    print(f"{'Prueba de Chi-Cuadrado':^60}")
    print("=" * 60)
    print(f"{'Intervalo':<20} | {'FO':<10} | {'FE':<10} | {'Chi^2':<10}")
    print("-" * 60)


    for intervalo,datos in resultado_prueba['intervalos'].items():
        lim_inf = f"{intervalo[0]:.2f}"
        lim_sup = f"{intervalo[1]:.2f}"

        etiqueta_intervalo = f"[{lim_inf}, {lim_sup})"
        fo = f"{datos['frecuencia_observada']:.2f}"
        fe = f"{datos['frecuencia_esperada']:.2f}"
        chi_cuadrado_intervalo = f"{datos['estadistico_chi_cuadrado']:.2f}"
        print(f"{etiqueta_intervalo:<20} | {fo:<10} | {fe:<10} | {chi_cuadrado_intervalo:<10}")


    print("-" * 60)
    sumatoria_f0 = f"{resultado_prueba['sumatoria_frecuencia_observada']:.2f}"
    sumatoria_fe = f"{resultado_prueba['sumatoria_frecuencia_esperada']:.2f}"
    chi_calculado = f"{resultado_prueba['chi_calculado']:.2f}"
    chi_tabulado = f"{resultado_prueba['chi_tabulado']:.2f}"
    cantidad_intervalos = len(resultado_prueba['intervalos'])
    aprueba =  resultado_prueba['aprueba_hipotesis_nula']
    print(f"{"":<20} | {sumatoria_f0:<10} | {sumatoria_fe:<10} | {chi_calculado:<10}")
    print("=" * 60)
    print(f"Cantidad de intervalos: {cantidad_intervalos}")
    print(f"Chi-Cuadrado Calculado: {chi_calculado}")

    print(
        f"Chi-Cuadrado Tabulado (GL={resultado_prueba['grados_de_libertad']}, α={1 - resultado_prueba['nivel_confianza']:.2f}): {chi_tabulado}")
    print("=" * 60)

    if aprueba is not None:
        if aprueba:
            print("\033[92mNo se rechaza la Hipótesis Nula\033[0m")  # Verde para éxito
        else:
            print("\033[91mNo se aprueba la Hipótesis Nula\033[0m")  # Rojo para fracaso
    else:
        print("No se pudo determinar si se aprueba la Hipótesis Nula.")

    print("=" * 60)
