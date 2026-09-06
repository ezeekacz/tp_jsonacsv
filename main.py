from procesador.interfaz import construir_parser, resolver_opciones
from procesador.lector import cargar_datos, aplanar_productos, obtener_ids_usuarios_validos
from procesador.validador import clasificar_productos, ordenar_productos
from procesador.escritor import generar_archivos


def main():
    args = construir_parser().parse_args()
    separador, campo_orden, descendente = resolver_opciones(args)

    datos = cargar_datos(args.entrada)
    ids_usuarios_validos = obtener_ids_usuarios_validos(datos)
    productos_planos = aplanar_productos(datos.get("productos", []))

    productos_por_usuario, rechazados = clasificar_productos(
        productos_planos, ids_usuarios_validos
    )
    ordenar_productos(productos_por_usuario, campo_orden, descendente)

    archivos_generados = generar_archivos(
        productos_por_usuario, rechazados, separador, args.salida
    )

    for ruta, cantidad in archivos_generados:
        print(f"Generado {ruta} con {cantidad} fila(s).")

    print(f"\nProductos rechazados ({len(rechazados)}):")
    for r in rechazados:
        print(f"  - id={r['id']} nombre='{r['nombre']}' -> {r['motivo']}")


if __name__ == "__main__":
    main()
