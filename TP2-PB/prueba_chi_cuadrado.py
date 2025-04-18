import math
from scipy.stats import chi2

class PruebaChiCuadrado:
    def __init__(self, distribucion, nivel_confianza_porcentaje):
        self.distribucion = distribucion
        self.nivel_confianza = nivel_confianza_porcentaje / 100.0

    def _es_primo(self, n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _calcular_cant_intervalos(self, cantidad_total):
        if not isinstance(cantidad_total, int) or cantidad_total <= 0:
            return None
        raiz_cuadrada = int(math.sqrt(cantidad_total))
        while True:
            if self._es_primo(raiz_cuadrada):
                return raiz_cuadrada
            raiz_cuadrada += 1

    def _calcular_amplitud_intervalo(self, val_min, val_max, cant_intervalos):
        rango = val_max - val_min
        amplitud = rango / cant_intervalos
        return amplitud

    def _definir_intervalos(self, val_min, val_max, num_intervalos, amplitud_intervalos):
        lista_intervalos = []
        limite_inf = val_min

        for i in range(num_intervalos):
            limite_sup = limite_inf + amplitud_intervalos
            if i == num_intervalos - 1:
                limite_sup = val_max # Asegurar que el último intervalo llegue hasta el máximo
            intervalo = (limite_inf, limite_sup)
            lista_intervalos.append(intervalo)
            limite_inf = limite_sup
        return lista_intervalos

    def _calcular_frecuencia_observada(self, numeros, intervalos):
        frecuencias = {intervalo: 0 for intervalo in intervalos}

        for numero in numeros:
            asignado = False
            for i, intervalo in enumerate(intervalos):
                limite_inf, limite_sup = intervalo

                # Para todos los intervalos excepto el último, la condición es < limite_sup
                if i < len(intervalos) - 1:
                    if limite_inf <= numero < limite_sup:
                        frecuencias[intervalo] += 1
                        asignado = True
                        break  # Importante: salir del bucle de intervalos una vez asignado
                # Para el último intervalo, la condición es <= limite_sup (incluyendo el máximo)
                else:
                    if limite_inf <= numero <= limite_sup:
                        frecuencias[intervalo] += 1
                        asignado = True
                        break  # Importante: salir del bucle de intervalos una vez asignado
            if not asignado:
                print(f"¡Advertencia! Número {numero} no asignado a ningún intervalo.")

        return frecuencias

    def _calcular_estadistico(self, frecuencia_observada, frecuencia_esperada, frecuencia_esperada_minima=5):
        """
        Calcula el estadístico chi-cuadrado para la prueba de bondad de ajuste.

        Si la frecuencia esperada en algún intervalo es menor que la mínima requerida,
        se fusiona ese intervalo con el siguiente adyacente hasta alcanzar el mínimo.
        Si al llegar al final no se alcanza el mínimo, se fusiona con el último
        intervalo válido (con frecuencia esperada >= mínima) encontrado hacia atrás.

        Args:
            frecuencia_observada (dict): Diccionario con los intervalos como clave
                                          y la frecuencia observada como valor.
            frecuencia_esperada (dict): Diccionario con los intervalos como clave
                                         y la frecuencia esperada como valor.
            frecuencia_esperada_minima (int): Frecuencia esperada mínima requerida
                                               para cada intervalo (por defecto es 5).

        Returns:
            tuple: Una tupla conteniendo:
                   - estadisticos_por_intervalo (dict): Estadístico chi-cuadrado por intervalo.
                   - observada_fusionada (dict): Frecuencias observadas después de la fusión.
                   - esperada_fusionada (dict): Frecuencias esperadas después de la fusión.
        """
        estadisticos_por_intervalo = {}
        observada_fusionada = frecuencia_observada.copy()
        esperada_fusionada_original = frecuencia_esperada.copy()  # Guardar las frecuencias esperadas originales

        # Normalizar la frecuencia esperada para que sume igual a la observada
        suma_observada = sum(observada_fusionada.values())
        suma_esperada_original = sum(esperada_fusionada_original.values())

        if suma_esperada_original > 0:
            factor_normalizacion = suma_observada / suma_esperada_original
            esperada_fusionada = {k: v * factor_normalizacion for k, v in esperada_fusionada_original.items()}
        else:
            esperada_fusionada = esperada_fusionada_original.copy()  # Evitar división por cero

        # Convertir los diccionarios a listas de tuplas para facilitar el procesamiento
        intervalos = list(observada_fusionada.keys())
        n = len(intervalos)
        i = 0

        while i < n:
            intervalo_actual = intervalos[i]
            fe_actual = esperada_fusionada[intervalo_actual]

            # Si la frecuencia esperada es menor que el mínimo requerido
            if fe_actual < frecuencia_esperada_minima:
                # Caso 1: Fusionar con el siguiente intervalo (si existe)
                if i < n - 1:
                    intervalo_siguiente = intervalos[i + 1]

                    # Crear nuevo intervalo fusionado
                    nuevo_limite_inferior = intervalo_actual[0]
                    nuevo_limite_superior = intervalo_siguiente[1]
                    nuevo_intervalo = (nuevo_limite_inferior, nuevo_limite_superior)

                    # Sumar frecuencias
                    nueva_fo = observada_fusionada[intervalo_actual] + observada_fusionada[intervalo_siguiente]
                    nueva_fe = esperada_fusionada[intervalo_actual] + esperada_fusionada[intervalo_siguiente]

                    # Actualizar diccionarios
                    del observada_fusionada[intervalo_actual]
                    del observada_fusionada[intervalo_siguiente]
                    del esperada_fusionada[intervalo_actual]
                    del esperada_fusionada[intervalo_siguiente]

                    observada_fusionada[nuevo_intervalo] = nueva_fo
                    esperada_fusionada[nuevo_intervalo] = nueva_fe

                    # Actualizar lista de intervalos
                    intervalos[i:i + 2] = [nuevo_intervalo]
                    n -= 1

                    # No incrementar i para revisar el nuevo intervalo
                    continue

                # Caso 2: No hay siguiente intervalo, fusionar con el anterior
                elif i > 0:
                    intervalo_anterior = intervalos[i - 1]

                    # Crear nuevo intervalo fusionado
                    nuevo_limite_inferior = intervalo_anterior[0]
                    nuevo_limite_superior = intervalo_actual[1]
                    nuevo_intervalo = (nuevo_limite_inferior, nuevo_limite_superior)

                    # Sumar frecuencias
                    nueva_fo = observada_fusionada[intervalo_anterior] + observada_fusionada[intervalo_actual]
                    nueva_fe = esperada_fusionada[intervalo_anterior] + esperada_fusionada[intervalo_actual]

                    # Actualizar diccionarios
                    del observada_fusionada[intervalo_anterior]
                    del observada_fusionada[intervalo_actual]
                    del esperada_fusionada[intervalo_anterior]
                    del esperada_fusionada[intervalo_actual]

                    observada_fusionada[nuevo_intervalo] = nueva_fo
                    esperada_fusionada[nuevo_intervalo] = nueva_fe

                    # Actualizar lista de intervalos
                    intervalos[i - 1:i + 1] = [nuevo_intervalo]
                    n -= 1
                    i -= 1  # Revisar el nuevo intervalo en la siguiente iteración
                    continue

            i += 1

        # Calcular el estadístico chi-cuadrado para cada intervalo después de la fusión
        for intervalo in observada_fusionada:
            fo = observada_fusionada[intervalo]
            fe = esperada_fusionada[intervalo]
            estadistico = (fo - fe) ** 2 / fe
            estadisticos_por_intervalo[intervalo] = estadistico

        return estadisticos_por_intervalo, observada_fusionada, esperada_fusionada

    def _obtener_chi_cuadrado_tabulado(self, grados_libertad):
        try:
            return chi2.ppf(self.nivel_confianza, grados_libertad)
        except ValueError:
            print(f"Error: Grados de libertad ({grados_libertad}) no válidos.")
            return None

    def realizar_prueba(self, numeros,cant_intervalos=None):

        cantidad_total = len(numeros)

        val_min = min(numeros)
        val_max = max(numeros)

        if cant_intervalos is None:
            cant_calc_intervalos = self._calcular_cant_intervalos(cantidad_total)
            if cant_calc_intervalos is None:
                return {"error": "Cantidad total de números no válida."}
            else:
                cant_intervalos = cant_calc_intervalos

        amplitud_intervalos = self._calcular_amplitud_intervalo(val_min, val_max, cant_intervalos)
        intervalos = self._definir_intervalos(val_min, val_max, cant_intervalos, amplitud_intervalos)
        frecuencia_observada = self._calcular_frecuencia_observada(numeros, intervalos)
        frecuencia_esperada = self.distribucion.calcular_frecuencia_esperada(intervalos, numeros)
        estadisticos_por_intervalo, observada_fusionada, esperada_fusionada = self._calcular_estadistico(
            frecuencia_observada, frecuencia_esperada, frecuencia_esperada_minima=5
        )

        cant_intervalos = len(observada_fusionada)

        sumatoria_f0 = sum(observada_fusionada.values())
        sumatoria_fe = sum(esperada_fusionada.values())

        chi_cuadrado_calculado = sum(estadisticos_por_intervalo.values())
        grados_libertad = cant_intervalos - 1 # Grados de libertad = k - 1 (k = número de categorías)
        chi_cuadrado_tabulado = self._obtener_chi_cuadrado_tabulado(grados_libertad)

        aprueba_hipotesis_nula = chi_cuadrado_calculado < chi_cuadrado_tabulado if chi_cuadrado_tabulado is not None else None

        tabla_resultado = {
            "cantidad_de_intervalos": cant_intervalos,
            "intervalos": {},
            "sumatoria_frecuencia_observada": sumatoria_f0,
            "sumatoria_frecuencia_esperada": sumatoria_fe,
            "chi_calculado": chi_cuadrado_calculado,
            "chi_tabulado": chi_cuadrado_tabulado,
            "grados_de_libertad": grados_libertad,
            "nivel_confianza": self.nivel_confianza,
            "aprueba_hipotesis_nula": aprueba_hipotesis_nula
        }

        intervalos_ordenados = sorted(list(observada_fusionada.keys()))

        for intervalo  in intervalos_ordenados:
            fe = esperada_fusionada.get(intervalo)
            fo = observada_fusionada.get(intervalo)
            estadistico = estadisticos_por_intervalo.get(intervalo, float('nan'))
            tabla_resultado["intervalos"][intervalo] = {
                "frecuencia_observada": fo,
                "frecuencia_esperada": fe,
                "estadistico_chi_cuadrado": estadistico
            }

        return tabla_resultado

