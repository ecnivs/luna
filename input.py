import socket

def send_input(text):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 65432))
    client.sendall(text.encode())
    client.close()

if __name__ == "__main__":
    while True:
        user_input = input("Enter command: ")
        send_input(user_input)
