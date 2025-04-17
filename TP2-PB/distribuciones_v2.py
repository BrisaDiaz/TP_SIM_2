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
        self.lambda_param = 1 / media  # λ = 1/media

    def _cdf(self, x):
        """Función de distribución acumulada para exponencial"""
        return 1 - math.exp(-self.lambda_param * x)

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)
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

    def _pdf(self, x):
        """Función de densidad de probabilidad"""
        return (1 / (self.sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - self.mu) / self.sigma) ** 2)

    def _cdf(self, x):
         """Función de distribución acumulada para normal"""
         return stats.norm.cdf(x, loc=self.mu, scale=self.sigma)

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)
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
        super().__init__()
        self.lambda_param = media  # λ = media

    def _pmf(self, k):
        """Función de masa de probabilidad para Poisson"""
        return (math.exp(-self.lambda_param) * (self.lambda_param ** k)) / math.factorial(k)

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)
        frecuencias_esperadas = {}

        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            prob = 0.0

            # Sumar las probabilidades para todos los enteros en el intervalo
            k_start = math.ceil(limite_inf)
            k_end = math.ceil(limite_sup)

            for k in range(k_start, k_end):
                prob += self._pmf(k)

            frecuencia_esperada = cantidad_total * prob
            frecuencias_esperadas[intervalo] = frecuencia_esperada

        return frecuencias_esperadas