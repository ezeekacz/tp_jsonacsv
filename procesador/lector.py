#lector.py:
#Responsable de leer el archivo JSON de entrada y de "aplanar" la lista
#de productos, que puede traer bloques anidados (listas dentro de la lista principal).

import json


def cargar_datos(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def aplanar_productos(lista_productos):
    planos = []
    for elemento in lista_productos:
        if isinstance(elemento, list):
            planos.extend(aplanar_productos(elemento))  # recursivo
        elif isinstance(elemento, dict):
            planos.append(elemento)
    return planos


def obtener_ids_usuarios_validos(datos):
    usuarios = datos.get("usuarios", [])
    return {u["id_usuario"] for u in usuarios}
