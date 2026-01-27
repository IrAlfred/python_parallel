import socket

def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.104', 8000))
    client.send("Alfred".encode())
    #print("Connecté au serveur sur le port 8000.")
    msg_serveur = client.recv(1024).decode()
    print(f"Message du serveur: {msg_serveur}")

if __name__ == "__main__":
    client()