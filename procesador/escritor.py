#escritor.py:
#Responsable de escribir los archivos CSV finales: uno por usuario y uno con los productos rechazados.

import csv
import os
from .constantes import COLUMNAS_PRODUCTO, COLUMNAS_RECHAZADOS


def escribir_csv_usuario(path, productos, separador):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=COLUMNAS_PRODUCTO,
            delimiter=separador,
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for p in productos:
            fila = {col: p[col] for col in COLUMNAS_PRODUCTO}
            writer.writerow(fila)


def escribir_csv_rechazados(path, rechazados, separador):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=COLUMNAS_RECHAZADOS,
            delimiter=separador,
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for r in rechazados:
            writer.writerow(r)


def generar_archivos(productos_por_usuario, rechazados, separador, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    archivos_generados = []

    for uid, lista in productos_por_usuario.items():
        nombre_archivo = os.path.join(carpeta_salida, f"productos_{uid}.csv")
        escribir_csv_usuario(nombre_archivo, lista, separador)
        archivos_generados.append((nombre_archivo, len(lista)))

    ruta_rechazados = os.path.join(carpeta_salida, "productos_rechazados.csv")
    escribir_csv_rechazados(ruta_rechazados, rechazados, separador)
    archivos_generados.append((ruta_rechazados, len(rechazados)))

    return archivos_generados
