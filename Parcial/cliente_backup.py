import socket
import os

HOST = "127.0.0.1"
PORT = 9000
ARCHIVO_ORIGEN = "repuestos.json"


def enviar_archivo():
    if not os.path.exists(ARCHIVO_ORIGEN):
        print(f"No se encontró el archivo '{ARCHIVO_ORIGEN}'.")
        return

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))
        print(f"Conectado al servidor {HOST}:{PORT}")

        with open(ARCHIVO_ORIGEN, "rb") as archivo:
            while True:
                fragmento = archivo.read(4096)
                if not fragmento:
                    break
                cliente.sendall(fragmento)

        print(f"Archivo '{ARCHIVO_ORIGEN}' enviado correctamente.")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Verificá que server_backup.py esté en ejecución.")

    finally:
        cliente.close()


enviar_archivo()