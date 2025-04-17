# TP2 - Generación y Prueba de Variables Aleatorias

Este proyecto se divide en dos módulos principales, implementando la generación y prueba de variables aleatorias de diferentes distribuciones.

## Estructura del Proyecto

El proyecto se organiza en las siguientes carpetas y archivos:

- **`data/`**: Contiene archivos CSV con valores de variables aleatorias generadas previamente para pruebas.
- **`generadores.py`**: Implementa una librería con clases para generar variables aleatorias de las distribuciones uniforme, exponencial, Poisson y normal.
- **`generar_archivo_numeros.py`**: Script para generar archivos CSV conteniendo números aleatorios de las distribuciones implementadas en `generadores.py`. Permite al usuario especificar los parámetros de la distribución y la cantidad de valores a generar.
- **`csv_utils.py`**: Contiene utilidades para trabajar con archivos CSV.
- **`prueba_chi_cuadrado.py`**: Implementa la prueba de Chi-Cuadrado para evaluar la bondad de ajuste de los generadores de variables aleatorias.
- **`main.py`**: Programa principal para interactuar con la librería de generación y realizar pruebas. (Se encuentra dentro de `TP2_PB`).
- **`README.md`**: Este archivo, que proporciona una descripción general del proyecto.
- **`requirements.txt`**: Lista de las dependencias necesarias para ejecutar el proyecto.
- **`TP2_PB/`**: Carpeta que contiene el archivo `main.py` para ejecutar el programa principal.

## Instalación de Dependencias

Para instalar las dependencias necesarias, ejecute el siguiente comando en la terminal:

```bash
pip install -r requirements.txt
```

## Manual de usuario

### Cómo ejecutar el programa

1.  **Navegue al directorio `TP2_PB`**: Abra su terminal o línea de comandos y diríjase a la carpeta `TP2_PB` dentro del directorio principal del proyecto.

    ``` bash
    cd TP2_PB 
    ```
    
2.  **Ejecute el script `main.py`**: Ejecute el programa principal utilizando el intérprete de Python.

    ``` bash
    python main.py
    ```
    
3.  **Siga las instrucciones en pantalla**: El programa le presentará un menú para seleccionar el tipo de distribución que desea generar y probar.
    
    -   **Seleccione la distribución**: Ingrese el número correspondiente a la distribución deseada (1 para Uniforme, 2 para Exponencial, 3 para Normal, 4 para Poisson).
    -   **Ingrese los parámetros**: El programa le solicitará los parámetros necesarios para la distribución seleccionada (por ejemplo, el valor mínimo y máximo para la uniforme, la media para la exponencial y Poisson, la media y desviación estándar para la normal).
    -   **Ingrese la cantidad de números**: Especifique la cantidad de números aleatorios que desea generar (hasta 50000).
    -   **Visualización interactiva (opcional)**: Se le preguntará la cantidad de columnas en las que desea ver los números generados, los cuales se mostrarán en bloques de 100. Puede navegar entre los bloques con las opciones 'a' (avanzar), 'v' (volver) y 's' (salir).
    -   **Prueba de Chi-Cuadrado**: Se le pedirá que ingrese el nivel de confianza para la prueba de Chi-Cuadrado y la cantidad de intervalos para el histograma.
    -   **Resultados**: El programa mostrará los resultados de la prueba de Chi-Cuadrado en una tabla y generará un histograma de los números generados.

### Importante sobre la visualización del histograma

Después de realizar la prueba de Chi-Cuadrado, se mostrará una ventana con el histograma generado. **Para continuar generando números y realizando más pruebas con diferentes distribuciones o parámetros, deberá cerrar la ventana del histograma.** El programa principal esperará a que cierre la ventana del gráfico para volver al menú principal.

## Modificaciones realizada 10/04

- Se cambió el mensaje de éxito de la prueba de chi cuadrado a "No se rechaza la hipótesis nula"
- Se cambió la validación del tipo rango de valores aceptados para el nivel de confianza a un valores flotantes entre 0 y 99.95
- Se añadió el método generar_numeros a algunas clases generadoras que lo omitían
- Se cambió la cantidad de tomada de decimales retornada por el método random de 2 a 16 decimales [0, 0.9999999999999999]
- Se agregó el método mostrar_numeros_interactivo(numeros, step, num_columnas) para que el usuario pueda visualizar los números generados de a bloques
- Se agregó un manual de usuario en el archivo README.md