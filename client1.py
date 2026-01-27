import socket

def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8000))
    print("Connecté au serveur sur le port 8000.")

if __name__ == "__main__":
    client()