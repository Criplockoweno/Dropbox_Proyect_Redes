import socket
import threading
from HTTPRequestHandler import HTTPRequestHandler

HEADER=4096
PORT=5053
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DISCONNECT"

def handle_client(conn, addr):
    
    print(f"[NEW CONNECTION]{addr} connected.")
    request = b''
    while True:
        # recibimos un mensaje de longitud maxima de 64 bytes
        # y lo decodificamos en formato UTF-8
        request = conn.recv(HEADER)
        if not request:
            break
        httpd = HTTPRequestHandler(request, conn)
        response = httpd.handle_request()
        # Enviamos la respuesta HTTP al cliente
        conn.sendall(response.encode(FORMAT))
       
    conn.close()

def start():
    
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # esperamos una conexion y cuando llegue la aceptamos
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]= {threading.active_count()-1}")


if __name__ == "__main__":
    # creamos la instancia Socket
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # asignamos la direccion IP y el puerto al socket
    server.bind(ADDR)
    print("Server is starting...")
    start()
