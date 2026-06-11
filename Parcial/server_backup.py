import socket

HOST = "0.0.0.0"
PORT = 9000
ARCHIVO_DESTINO = "repuestos_backup.json"


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(1)
    print(f"Servidor escuchando en {HOST}:{PORT}...")

    while True:
        conn, direccion = servidor.accept()
        print(f"Conexión recibida de {direccion[0]}:{direccion[1]}")

        datos = b""
        while True:
            fragmento = conn.recv(4096)
            if not fragmento:
                break
            datos += fragmento

        with open(ARCHIVO_DESTINO, "wb") as archivo:
            archivo.write(datos)

        print(f"Archivo recibido y guardado como '{ARCHIVO_DESTINO}'.")
        conn.close()
        print("Conexión cerrada. Esperando nueva conexión...\n")


iniciar_servidor()