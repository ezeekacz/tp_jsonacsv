#validador.py:
#Contiene las funciones de normalización (limpiar texto, convertir tipos)
#y la lógica de validación que decide si un producto se puede exportar o debe rechazarse, y por qué motivo.

from .constantes import CATEGORIA_POR_DEFECTO


def normalizar_texto(valor):
    if valor is None:
        return None
    return str(valor).strip()


def convertir_numero(valor, tipo):
    if valor is None:
        return None
    if isinstance(valor, str) and valor.strip() == "":
        return None
    try:
        return tipo(valor)
    except (ValueError, TypeError):
        return None


def procesar_producto(producto, ids_usuarios_validos, ids_vistos):
    id_producto = producto.get("id")
    nombre = normalizar_texto(producto.get("nombre"))

    if id_producto in ids_vistos:
        return None, "id duplicado"
    ids_vistos.add(id_producto)

    if id_producto is None:
        return None, "id faltante"

    if not nombre:
        return None, "nombre faltante"

    id_usuario = producto.get("id_usuario")
    if id_usuario not in ids_usuarios_validos:
        return None, "usuario inexistente"

    categoria = normalizar_texto(producto.get("categoria")) or CATEGORIA_POR_DEFECTO

    precio = convertir_numero(producto.get("precio"), float)
    if precio is None or precio < 0:
        return None, "precio faltante o inválido"

    stock = convertir_numero(producto.get("stock"), int)
    if stock is None or stock < 0:
        return None, "stock faltante o inválido"

    producto_normalizado = {
        "id": id_producto,
        "id_usuario": id_usuario,
        "nombre": nombre,
        "categoria": categoria,
        "precio": round(precio, 2),
        "stock": stock,
    }
    return producto_normalizado, None


def clasificar_productos(productos_planos, ids_usuarios_validos):
    productos_por_usuario = {uid: [] for uid in ids_usuarios_validos}
    rechazados = []
    ids_vistos = set()

    for producto in productos_planos:
        normalizado, motivo = procesar_producto(producto, ids_usuarios_validos, ids_vistos)
        if motivo:
            rechazados.append(
                {
                    "id": producto.get("id", ""),
                    "nombre": normalizar_texto(producto.get("nombre")) or "",
                    "motivo": motivo,
                }
            )
        else:
            productos_por_usuario[normalizado["id_usuario"]].append(normalizado)

    return productos_por_usuario, rechazados


def ordenar_productos(productos_por_usuario, campo_orden, descendente):
    for lista in productos_por_usuario.values():
        if campo_orden == "nombre":
            lista.sort(key=lambda p: p["nombre"].lower(), reverse=descendente)
        else:
            lista.sort(key=lambda p: p[campo_orden], reverse=descendente)
