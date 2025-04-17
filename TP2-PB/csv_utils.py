import csv

def grabar_en_archivo(numeros, nombre_archivo="numeros.csv", encabezado='Numeros'):
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([encabezado])

        filas = [[numero] for numero in numeros]
        escritor_csv.writerows(filas)
        archivo_csv.flush()

        archivo_csv.close()

def cargar_de_archivo(nombre_archivo):
    numeros_cargados = []
    try:
        with open(nombre_archivo, 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            next(lector_csv, None)  # Saltar la primera fila (encabezado)

            for fila in lector_csv:
                if fila:  # Asegurarse de que la fila no esté vacía
                    try:
                        numero_str = fila[0]
                        if isinstance(numero_str, float) :
                            numeros_cargados.append(int(numero_str))
                        else:
                            numeros_cargados.append(float(numero_str))
                    except ValueError:
                        print(f"Advertencia: No se pudo convertir a número el valor '{fila[0]}' en el archivo.")
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
    return numeros_cargados

