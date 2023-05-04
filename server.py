import socket
import threading
from HTTPRequestHandler import HTTPRequestHandler
import re

HEADER = 4096
PORT = 5053
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


def handle_client(conn, addr):

    print(f"[NEW CONNECTION]{addr} connected.")
    while True:
        # recibimos un mensaje de longitud maxima de 64 bytes
        # y lo decodificamos en formato UTF-8
        request = conn.recv(HEADER)  # .decode(FORMAT)
        print('Cabeceras')
        headers = request.decode(FORMAT)
        lines = headers.split('\n')
        headers = {}
        for line in lines[1:]:
            if line.strip() != '':
                key, value = line.split(': ')
                headers[key] = value.strip()
        if ('Content-Length' in headers):
            print(headers['Content-Length'])
        if not request:
            break
        httpd = HTTPRequestHandler(request.decode(FORMAT))
        response = httpd.handle_request()
        # Enviamos la respuesta HTTP al cliente
        # conn.sendall(response.encode(FORMAT))
        if (type(response) is str):
            response = response.encode(FORMAT)
        conn.sendall(response)

    conn.close()


def start():

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # esperamos una conexion y cuando llegue la aceptamos
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]= {threading.active_count()-1}")


if __name__ == "__main__":
    # creamos la instancia Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # asignamos la direccion IP y el puerto al socket
    server.bind(ADDR)
    print("Server is starting...")
    start()
