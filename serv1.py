import socket

def serveur():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))

    server.listen(1)
    print("Serveur en écoute sur le port 8000...")
    conn, addr = server.accept()
    print(f"Connexion de {addr}")

if __name__ == "__main__":
    serveur()