import math
from abc import ABC, abstractmethod
from scipy import stats

class Distribucion(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def calcular_frecuencia_esperada(self, intervalos, numeros):
        pass

class Uniforme(Distribucion):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)
        num_intervalos = len(intervalos)
        if num_intervalos > 0:
            frecuencia_esperada_por_intervalo = cantidad_total / num_intervalos
            frecuencias_esperadas = {intervalo: frecuencia_esperada_por_intervalo for intervalo in intervalos}
            return frecuencias_esperadas
        else:
            return {}

class Exponencial(Distribucion):
    def __init__(self, media):
        super().__init__()
        self.media = media

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)
        if not numeros:
            return {intervalo: 0 for intervalo in intervalos}

        media = self.media

        frecuencias_esperadas = {}
        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            probabilidad = stats.expon.cdf(limite_sup, scale=media) - stats.expon.cdf(limite_inf, scale=media)
            frecuencia_esperada = cantidad_total * probabilidad
            frecuencias_esperadas[intervalo] = frecuencia_esperada
        return frecuencias_esperadas

class Normal(Distribucion):
    def __init__(self, mu, sigma):
        super().__init__()
        self.mu = mu
        self.sigma = sigma

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)
        if not numeros:
            return {intervalo: 0 for intervalo in intervalos}

        media_muestra = self.mu
        desviacion_estandar_muestra = self.sigma

        frecuencias_esperadas = {}
        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            probabilidad = stats.norm.cdf(limite_sup, loc=media_muestra, scale=desviacion_estandar_muestra) - stats.norm.cdf(limite_inf, loc=media_muestra, scale=desviacion_estandar_muestra)
            frecuencia_esperada = cantidad_total * probabilidad
            frecuencias_esperadas[intervalo] = frecuencia_esperada
        return frecuencias_esperadas

class Poisson(Distribucion):
    def __init__(self, media):
        super().__init__()
        self.media = media

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)

        if not numeros:
            return {intervalo: 0 for intervalo in intervalos}

        media = self.media

        frecuencias_esperadas = {}
        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            probabilidad = 0

            for k in range(math.ceil(limite_inf), math.ceil(limite_sup)):
                probabilidad += stats.poisson.pmf(k, mu=media)
            frecuencia_esperada = cantidad_total * probabilidad
            frecuencias_esperadas[intervalo] = frecuencia_esperada
        return frecuencias_esperadas