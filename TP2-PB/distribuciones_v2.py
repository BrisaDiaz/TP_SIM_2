import math
from abc import ABC, abstractmethod
from scipy import stats

class Distribucion(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def calcular_frecuencia_esperada(self, intervalos, cantidad_total):
        pass


class Uniforme(Distribucion):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def calcular_frecuencia_esperada(self, intervalos, cantidad_total):
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
        self.lambda_param = 1 / media  # λ = 1/media

    def _cdf(self, x):
        """Función de distribución acumulada para exponencial"""
        return 1 - math.exp(-self.lambda_param * x)

    def calcular_frecuencia_esperada(self, intervalos, cantidad_total):
        frecuencias_esperadas = {}

        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            # Calcular probabilidad usando la CDF manual
            prob = self._cdf(limite_sup) - self._cdf(limite_inf)
            frecuencia_esperada = cantidad_total * prob
            frecuencias_esperadas[intervalo] = frecuencia_esperada

        return frecuencias_esperadas


class Normal(Distribucion):
    def __init__(self, mu, sigma):
        super().__init__()
        self.mu = mu
        self.sigma = sigma

    def _cdf(self, x):
         """Función de distribución acumulada para normal"""
         return stats.norm.cdf(x, loc=self.mu, scale=self.sigma)

    def calcular_frecuencia_esperada(self, intervalos, cantidad_total):
        frecuencias_esperadas = {}

        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            # Calcular probabilidad usando la CDF
            prob = self._cdf(limite_sup) - self._cdf(limite_inf)
            frecuencia_esperada = cantidad_total * prob
            frecuencias_esperadas[intervalo] = frecuencia_esperada

        return frecuencias_esperadas


class Poisson(Distribucion):
    def __init__(self, media):
        self.media = media

    def _pmf(self, k):
        if k < 0:
            return 0
        return (math.exp(-self.media) * (self.media ** k)) / math.factorial(k)

    def calcular_frecuencia_esperada(self, valores_unicos, cantidad_total):
        frecuencias_esperadas = {}
        for valor in valores_unicos:
            prob = self._pmf(valor)
            frecuencia_esperada = cantidad_total * prob
            frecuencias_esperadas[valor] = frecuencia_esperada
        return frecuencias_esperadas