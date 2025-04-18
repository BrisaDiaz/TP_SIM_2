from abc import ABC, abstractmethod
from scipy import stats
import math

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
        frecuencias_esperadas = {}
        num_intervalos = len(intervalos)
        if num_intervalos > 0:
            frecuencia_esperada_por_intervalo = cantidad_total / num_intervalos
            for intervalo in intervalos:
                frecuencias_esperadas[intervalo] = frecuencia_esperada_por_intervalo
        return frecuencias_esperadas

class Exponencial(Distribucion):
    def __init__(self, media):
        super().__init__()
        self.media = media

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)
        frecuencias_esperadas = {}
        dist_esperada = stats.expon(scale=self.media)
        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            probabilidad = dist_esperada.cdf(limite_sup) - dist_esperada.cdf(limite_inf)
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
        frecuencias_esperadas = {}
        dist_esperada = stats.norm(loc=self.mu, scale=self.sigma)
        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            probabilidad = dist_esperada.cdf(limite_sup) - dist_esperada.cdf(limite_inf)
            frecuencia_esperada = cantidad_total * probabilidad
            frecuencias_esperadas[intervalo] = frecuencia_esperada
        return frecuencias_esperadas

class Poisson(Distribucion):
    def __init__(self, media):
        super().__init__()
        self.media = media

    def calcular_frecuencia_esperada(self, intervalos, numeros):
        cantidad_total = len(numeros)
        frecuencias_esperadas = {}
        dist_esperada = stats.poisson(mu=self.media)
        for intervalo in intervalos:
            limite_inf, limite_sup = intervalo
            probabilidad = 0

            # Sumar las probabilidades para todos los enteros en el intervalo
            k_start = math.ceil(limite_inf)
            k_end = math.ceil(limite_sup)
            for k in range(k_start, k_end + 1):
                probabilidad += dist_esperada.pmf(k)

            frecuencia_esperada = cantidad_total * probabilidad
            frecuencias_esperadas[intervalo] = frecuencia_esperada
        return frecuencias_esperadas