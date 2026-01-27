import socket

def serveur():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.1.104', 8000))
    server.listen(10)
    print("Serveur en attente de connexion...")
    while True:
        conn, addr = server.accept()
        data = conn.recv(1024).decode()
        print(f"{addr} Connecté")
        print(f"Nom client: {data}")
        conn.send(f"Bienvenue, {data}!".encode())


if __name__ == "__main__":
    serveur()