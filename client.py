import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(message):
    message = message.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

is_connected = True
while is_connected:
    try:
        message = input("Enter your message: ")
        if message == DISCONNECT_MESSAGE:
            send(DISCONNECT_MESSAGE)
            is_connected = False
        else:
            send(message)
    except KeyboardInterrupt:
        print("\nDisconnecting...")
        send(DISCONNECT_MESSAGE)
        is_connected = False
    except Exception as e:
        print(f"An error occurred: {e}")
        is_connected = False

client.close()
print("Connection Closed")
