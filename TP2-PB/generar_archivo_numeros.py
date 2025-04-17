from csv_utils import  grabar_en_archivo
from TP2_PA.generadores import GeneradorExponencial, GeneradorUniforme, GeneradorPoisson, GeneradorNormal

cant_n=600

generador_un = GeneradorUniforme(0,10 )
numeros_norm = generador_un.generar_numeros(cant_n)
grabar_en_archivo(numeros_norm, f"data/uniforme-{cant_n}.csv")

generador_norm = GeneradorNormal(38, 0.5)
numeros_norm = generador_norm.generar_numeros(cant_n)
grabar_en_archivo(numeros_norm, f"data/normal-{cant_n}.csv")


generador_exp = GeneradorExponencial(5)
numeros_exp = generador_exp.generar_numeros(cant_n)
grabar_en_archivo(numeros_exp, f"data/exponencial-{cant_n}.csv")

generador_poi = GeneradorPoisson(3)
numeros_poi = generador_poi.generar_numeros(cant_n)
grabar_en_archivo(numeros_poi, f"data/poisson-{cant_n}.csv")
