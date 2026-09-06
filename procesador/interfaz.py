#interfaz.py:
#Maneja la interacción con quien ejecuta el programa: argumentos de línea
#de comandos y las preguntas por consola (separador y criterio de orden).


import argparse

from .constantes import ENTRADA_POR_DEFECTO


def construir_parser():
    parser = argparse.ArgumentParser(
        description="Procesa productos.json y genera un CSV por usuario."
    )
    parser.add_argument("--separador", choices=[",", ";"], help="Separador de los CSV")
    parser.add_argument(
        "--orden", choices=["nombre", "precio", "stock"], help="Campo de ordenamiento"
    )
    parser.add_argument(
        "--direccion", choices=["asc", "desc"], help="Dirección del ordenamiento"
    )
    parser.add_argument(
        "--entrada", default=ENTRADA_POR_DEFECTO, help="Ruta del archivo JSON de entrada"
    )
    parser.add_argument("--salida", default=".", help="Carpeta de salida para los CSV")
    return parser


def preguntar_separador():
    print("¿Qué separador querés usar en los CSV?")
    print("  1) Coma (,)")
    print("  2) Punto y coma (;)")
    opcion = input("Elegí 1 o 2: ").strip()
    return ";" if opcion == "2" else ","


def preguntar_orden():
    print("¿Cómo querés ordenar los productos?")
    print("  1) Por nombre")
    print("  2) Por precio")
    print("  3) Por stock")
    opcion = input("Elegí 1, 2 o 3: ").strip()
    campo = {"1": "nombre", "2": "precio", "3": "stock"}.get(opcion, "nombre")

    print("¿Orden ascendente o descendente?")
    print("  1) Ascendente")
    print("  2) Descendente")
    direccion = input("Elegí 1 o 2: ").strip()
    descendente = direccion == "2"
    return campo, descendente


def resolver_opciones(args):
    separador = args.separador if args.separador else preguntar_separador()

    if args.orden and args.direccion:
        campo_orden = args.orden
        descendente = args.direccion == "desc"
    else:
        campo_orden, descendente = preguntar_orden()

    return separador, campo_orden, descendente
