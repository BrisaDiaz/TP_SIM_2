from TP2_PA.generadores import GeneradorExponencial, GeneradorUniforme, GeneradorPoisson, GeneradorNormal
from prueba_chi_cuadrado import  PruebaChiCuadrado
from distribuciones import Uniforme, Normal, Exponencial, Poisson

from ui import generar_histograma, mostrar_tabla

def obtener_entero_entre(mensaje, min=1, max=50000):
    while True:
        try:
            valor = int(input(mensaje))
            if min <= valor <= max:
                return valor
            else:
                print(f"Por favor, ingrese un número entero entre {min} y {max}.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")


def obtener_float_entre(mensaje, min=0.0, max=99.95):
    while True:
        try:
            valor = int(input(mensaje))
            if min <= valor <= max:
                return valor
            else:
                print(f"Por favor, ingrese un número flotante entre {min} y {max}.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número decimal.")

def obtener_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número decimal.")

def mostrar_numeros_interactivo(numeros, step=100, num_columnas=1):
    if not numeros:
        print("No hay números para mostrar.")
        return

    n = len(numeros)
    start = 0

    while True:
        end = min(start + step, n)
        print(f"\nMostrando números del {start + 1} al {end} (de {n}):")

        if num_columnas == 1:
            for i in range(start, end):
                if isinstance(numeros[i], float):
                    print(f"{numeros[i]:.2f}")
                else:
                    print(numeros[i])
        else:
            for i in range(start, end):
                if isinstance(numeros[i], float):
                    formatted_num = f"{numeros[i]:<15.2f}"
                else:
                    formatted_num = f"{numeros[i]:<15}"
                print(formatted_num, end="")
                if (i + 1 - start) % num_columnas == 0:
                    print()
        opcionesMensaje = ("\n OPCIONES: \n"
                    "a: Avanzar \n"
                    "v: Volver \n"
                    "s: Salir \n"
                    "")
        if n> step:
            print(opcionesMensaje)
            print()  # Nueva línea al final del bloque
            opcion = input("Ingrese una opción (a/v/s): ").lower()


            if opcion == 'a':
                start += step
                if start >= n:
                    print("Se ha llegado al final de la lista.")
                    start -= step
            elif opcion == 'v':
                start -= step
                if start < 0:
                    print("Se ha llegado al inicio de la lista.")
                    start = 0
            elif opcion == 's':
                break
            else:
                print("Opción inválida.")

            if start == n:
                start -= step
        else:
            break

def programa_main():
    print("\nGENERADOR DE VARIABLES ALEATORIAS")
    while True:
        print("\nSeleccione el tipo de distribución:")
        print("1. Uniforme")
        print("2. Exponencial")
        print("3. Normal")
        print("4. Poisson")
        print("5. Salir")
        opcion = input("Ingrese el número de la distribución: ")


        numeros = []
        distribution = None
        cantidad = 0
        nombre_distribucion = ""

        if opcion == '1':
            print("\n--- Distribución Uniforme ---")
            a = obtener_float("Ingrese el valor mínimo (a): ")
            b = obtener_float("Ingrese el valor máximo (b): ")
            while b <= a:
                print("El valor máximo (b) debe ser mayor que el valor mínimo (a).")
                b = obtener_float("Ingrese el valor máximo (b): ")

            cantidad = obtener_entero_entre("Ingrese la cantidad de números a generar (hasta 50000): ")
            generador = GeneradorUniforme(a, b)
            numeros = generador.generar_numeros(cantidad)
            print(f"\nSe generaron {len(numeros)} números con distribución Uniforme U({a:.2f}, {b:.2f}).")

            distribution = Uniforme(a,b)
            nombre_distribucion = f"uniforme U({a:.2f}, {b:.2f})"

        elif opcion == '2':
            print("\n--- Distribución Exponencial ---")
            media = obtener_float("Ingrese la media (o 1/lambda): ")
            while media <= 0:
                print("La media debe ser un valor positivo.")
                media = obtener_float("Ingrese la media (o 1/lambda): ")
            cantidad = obtener_entero_entre("Ingrese la cantidad de números a generar (hasta 50000): ")
            generador = GeneradorExponencial(media)
            numeros = generador.generar_numeros(cantidad)
            print(f"\nSe generaron {len(numeros)} números con distribución Exponencial con media {media:.2f}.")

            distribution = Exponencial(media)
            nombre_distribucion = f"exponencial Exp({media:.2f})"

        elif opcion == '3':
            print("\n--- Distribución Normal ---")
            media = obtener_float("Ingrese la media (mu): ")
            desviacion_estandar = obtener_float("Ingrese la desviación estándar (sigma): ")
            while desviacion_estandar <= 0:
                print("La desviación estándar debe ser un valor positivo.")
                desviacion_estandar = obtener_float("Ingrese la desviación estándar (sigma): ")
            cantidad = obtener_entero_entre("Ingrese la cantidad de números a generar (hasta 50000): ")
            generador = GeneradorNormal(media, desviacion_estandar)
            numeros = generador.generar_numeros(cantidad)

            print(f"\nSe generaron {len(numeros)} números con distribución Normal N({media:.2f}, {desviacion_estandar:.2f}).")

            distribution = Normal(media,desviacion_estandar)
            nombre_distribucion = f"normal N({media:.2f}, {desviacion_estandar:.2f})"

        elif opcion == '4':
            print("\n--- Distribución Poisson ---")
            media = obtener_float("Ingrese la media (lambda): ")
            while media <= 0:
                print("La media (lambda) debe ser un valor positivo.")
                media = obtener_float("Ingrese la media (lambda): ")
            cantidad = obtener_entero_entre("Ingrese la cantidad de números a generar (hasta 50000): ")
            generador = GeneradorPoisson(media)
            numeros = generador.generar_numeros(cantidad)
            print(f"\nSe generaron {len(numeros)} números con distribución Poisson con media {media:.2f}.")

            distribution = Poisson(media)
            nombre_distribucion = f"normal P({media:.2f})"

        if 1<= int(opcion) <=4:
            mostrar_numeros_interactivo(numeros, 100, 5)
            es_poisson = isinstance(distribution, Poisson)

            print('\n','*'*60)
            print(f"PRUEBA DE CHI CUADRADO")
            confianza = obtener_float_entre("Ingrese el nivel de confianza (1-99.95):", 1, 99.95)
            intervalo_prueba = None

            if not es_poisson:
                respuesta_intervalos = input(
                    f"¿Desea especificar la cantidad de intervalos para la prueba de Chi Cuadrado? (s/n): ").lower()
                if respuesta_intervalos == 's':
                    intervalo_prueba_usuario = obtener_entero_entre(
                        f"Ingrese la cantidad de intervalos de la prueba (1-{cantidad}):", 1, cantidad)
                    intervalo_prueba = intervalo_prueba_usuario

            intervalo_grafico = obtener_entero_entre(f"Ingrese la cantidad de intervalos del historigrama (1-{cantidad}):", 1, cantidad)

            prueba_chi = PruebaChiCuadrado(distribution, confianza)
            resultado_prueba = None

            if es_poisson:
                resultado_prueba = prueba_chi.realizar_prueba_discreta_poisson(numeros, cant_intervalos=intervalo_prueba)
            else:
                resultado_prueba = prueba_chi.realizar_prueba(numeros, cant_intervalos=intervalo_prueba)

            mostrar_tabla(resultado_prueba, nombre_distribucion)
            generar_histograma(numeros, intervalo_grafico)

        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, seleccione un número del 1 al 5.")

if __name__ == "__main__":
    programa_main()