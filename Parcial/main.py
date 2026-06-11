import json
import csv
import uuid
from datetime import datetime

ARCHIVO_JSON = "repuestos.json"
ARCHIVO_CSV = "repuestos.csv"

CATEGORIAS = [
    "motor", "frenos", "pastilla de freno", "filtro de agua",
    "filtro de aceite", "aceite", "bateria", "escobillas",
    "suspension", "transmision", "escape", "carroceria", "otros"
]


def fecha_actual():
    return datetime.now().isoformat(timespec="seconds")


def cargar_repuestos():
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


def guardar_repuestos(repuestos):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(repuestos, archivo, indent=4, ensure_ascii=False)


def pedir_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor != "":
            return valor
        print("Este campo es requerido.")


def pedir_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor > 0:
                return valor
            print("El precio debe ser mayor a 0.")
        except ValueError:
            print("Ingrese un número válido.")


def pedir_int(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= 0:
                return valor
            print("El stock no puede ser negativo.")
        except ValueError:
            print("Ingrese un número entero válido.")


def pedir_categoria():
    print("Categorías disponibles:")

    numero = 1
    for cat in CATEGORIAS:
        print(str(numero) + ". " + cat)
        numero += 1

    while True:
        categoria = input("Categoría: ").lower().strip()
        if categoria in CATEGORIAS:
            return categoria
        print("Categoría inválida. Elegí una de la lista.")


def agregar_repuesto(repuestos):
    nombre = pedir_texto("Nombre: ")
    marca = pedir_texto("Marca: ")
    modelo_auto = pedir_texto("Modelo de auto: ")
    categoria = pedir_categoria()
    precio = pedir_float("Precio: ")
    stock = pedir_int("Stock: ")

    ahora = fecha_actual()

    repuesto = {
        "id": str(uuid.uuid4()),
        "nombre": nombre,
        "marca": marca,
        "modelo_auto": modelo_auto,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "fecha_ingreso": ahora,
        "fecha_modificado": ahora
    }

    repuestos.append(repuesto)
    guardar_repuestos(repuestos)
    print("Repuesto agregado correctamente.")


def listar_repuestos(repuestos):
    if len(repuestos) == 0:
        print("El inventario está vacío.")
        return

    for r in repuestos:
        print("-------------------------")
        print(f"ID: {r['id']}")
        print(f"Nombre: {r['nombre']}")
        print(f"Marca: {r['marca']}")
        print(f"Modelo auto: {r['modelo_auto']}")
        print(f"Categoría: {r['categoria']}")
        print(f"Precio: ${r['precio']}")
        print(f"Stock: {r['stock']}")
        print(f"Fecha ingreso: {r['fecha_ingreso']}")
        print(f"Fecha modificado: {r['fecha_modificado']}")


def buscar_repuesto(repuestos):
    texto = input("Buscar por nombre o marca: ").lower().strip()
    encontrados = []

    for r in repuestos:
        if texto in r["nombre"].lower() or texto in r["marca"].lower():
            encontrados.append(r)

    if len(encontrados) == 0:
        print("No se encontraron repuestos.")
    else:
        listar_repuestos(encontrados)


def actualizar_repuesto(repuestos):
    id_buscar = input("Ingrese el ID del repuesto: ").strip()

    for r in repuestos:
        if r["id"] == id_buscar:
            print("Dejar vacío si no desea modificar.")

            nuevo_precio = input("Nuevo precio: ").strip()
            if nuevo_precio != "":
                try:
                    nuevo_precio = float(nuevo_precio)
                    if nuevo_precio > 0:
                        r["precio"] = nuevo_precio
                    else:
                        print("El precio debe ser mayor a 0.")
                        return
                except ValueError:
                    print("Precio inválido.")
                    return

            nuevo_stock = input("Nuevo stock: ").strip()
            if nuevo_stock != "":
                try:
                    nuevo_stock = int(nuevo_stock)
                    if nuevo_stock >= 0:
                        r["stock"] = nuevo_stock
                    else:
                        print("El stock no puede ser negativo.")
                        return
                except ValueError:
                    print("Stock inválido.")
                    return

            r["fecha_modificado"] = fecha_actual()
            guardar_repuestos(repuestos)
            print("Repuesto actualizado correctamente.")
            return

    print("No se encontró un repuesto con ese ID.")


def eliminar_repuesto(repuestos):
    id_buscar = input("Ingrese el ID del repuesto a eliminar: ").strip()

    for r in repuestos:
        if r["id"] == id_buscar:
            confirmar = input("¿Seguro que desea eliminarlo? s/n: ").lower().strip()

            if confirmar == "s":
                repuestos.remove(r)
                guardar_repuestos(repuestos)
                print("Repuesto eliminado correctamente.")
            else:
                print("Operación cancelada.")
            return

    print("No se encontró un repuesto con ese ID.")


def exportar_csv(repuestos):
    if len(repuestos) == 0:
        print("No hay repuestos para exportar.")
        return

    campos = [
        "id", "nombre", "marca", "modelo_auto", "categoria",
        "precio", "stock", "fecha_ingreso", "fecha_modificado"
    ]

    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(repuestos)

    print("Archivo CSV exportado correctamente.")


def mostrar_menu():
    print("\n--- Sistema de Gestión de Repuestos ---")
    print("1. Agregar repuesto")
    print("2. Listar repuestos")
    print("3. Buscar repuesto")
    print("4. Actualizar repuesto")
    print("5. Eliminar repuesto")
    print("6. Exportar a CSV")
    print("7. Salir")


def main():
    repuestos = cargar_repuestos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_repuesto(repuestos)
        elif opcion == "2":
            listar_repuestos(repuestos)
        elif opcion == "3":
            buscar_repuesto(repuestos)
        elif opcion == "4":
            actualizar_repuesto(repuestos)
        elif opcion == "5":
            eliminar_repuesto(repuestos)
        elif opcion == "6":
            exportar_csv(repuestos)
        elif opcion == "7":
            guardar_repuestos(repuestos)
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


main()