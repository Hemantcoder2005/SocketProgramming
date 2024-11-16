import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # Use "0.0.0.0" to listen on all interfaces
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    '''Handles individual client connections in a separate thread'''
    print(f"[NEW CONNECTION] {addr} connected.")
    is_connected = True
    while is_connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"{addr} --> {msg}")
                if msg == DISCONNECT:
                    is_connected = False
        except ConnectionResetError:
            print(f"[ERROR] Connection with {addr} reset unexpectedly.")
            break
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred with {addr}: {e}")
            break

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def start():
    '''Starts the server and spawns a new thread for each client'''
    server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("\n[SHUTTING DOWN] Server is shutting down.")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error in server: {e}")
            break

    server.close()

print("[STARTING] Server is starting...")
start()
