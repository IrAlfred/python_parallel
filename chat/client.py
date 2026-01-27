#!/usr/bin/env python3
"""
Client de chat pour se connecter au serveur
Utilise threading pour recevoir et envoyer des messages simultanément
"""

import socket
import threading
import sys
from datetime import datetime

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
        self.name = None
        
    def connect(self):
        """Se connecte au serveur de chat"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            
            # Recevoir la demande de nom
            response = self.client_socket.recv(1024).decode('utf-8')
            
            if response == "ENTER_NAME":
                # Demander le nom à l'utilisateur
                self.name = input("Entrez votre nom: ").strip()
                
                while not self.name:
                    print("Le nom ne peut pas être vide!")
                    self.name = input("Entrez votre nom: ").strip()
                
                # Envoyer le nom au serveur
                self.client_socket.send(self.name.encode('utf-8'))
                
                # Vérifier si le nom est accepté
                response = self.client_socket.recv(1024).decode('utf-8')
                
                if response == "NAME_TAKEN":
                    print(f"❌ Le nom '{self.name}' est déjà utilisé!")
                    self.client_socket.close()
                    return False
                else:
                    # Le nom est accepté, afficher le message de bienvenue
                    print(response, end='')
                    self.connected = True
                    return True
            
        except ConnectionRefusedError:
            print("❌ Impossible de se connecter au serveur. Assurez-vous qu'il est démarré.")
            return False
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    
    def receive_messages(self):
        """Thread pour recevoir les messages du serveur"""
        while self.connected:
            try:
                message = self.client_socket.recv(4096).decode('utf-8')
                
                if not message:
                    break
                
                if message == "SERVER_SHUTDOWN":
                    print("\n[SYSTÈME] Le serveur a été arrêté")
                    self.connected = False
                    break
                
                # Afficher le message reçu
                print(message, end='')
                
            except Exception as e:
                if self.connected:
                    print(f"\n❌ Erreur de réception: {e}")
                break
        
        self.disconnect()
    
    def send_messages(self):
        """Thread pour envoyer les messages au serveur"""
        print("\n💬 Vous pouvez commencer à chatter!\n")
        
        while self.connected:
            try:
                message = input()
                
                if not self.connected:
                    break
                
                if message.strip():
                    if message.strip().lower() == '/quit':
                        self.connected = False
                        self.client_socket.send(message.encode('utf-8'))
                        break
                    
                    self.client_socket.send(message.encode('utf-8'))
                    
            except EOFError:
                break
            except Exception as e:
                if self.connected:
                    print(f"❌ Erreur d'envoi: {e}")
                break
        
        self.disconnect()
    
    def start(self):
        """Démarre le client de chat"""
        if not self.connect():
            return
        
        print(f"\n✅ Connecté au serveur {self.host}:{self.port}")
        
        # Créer deux threads: un pour recevoir, un pour envoyer
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Le thread principal gère l'envoi
        try:
            self.send_messages()
        except KeyboardInterrupt:
            print("\n\n👋 Déconnexion...")
            self.disconnect()
    
    def disconnect(self):
        """Déconnecte le client du serveur"""
        if self.connected:
            self.connected = False
            
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        
        print("\n[CLIENT] Déconnecté du serveur")


def print_banner():
    """Affiche la bannière du client"""
    banner = """
╔═══════════════════════════════════════════════════╗
║          💬 CLIENT DE CHAT PYTHON 💬              ║
╚═══════════════════════════════════════════════════╝
"""
    print(banner)


if __name__ == "__main__":
    print_banner()
    
    # Paramètres de connexion
    host = '127.0.0.1'
    port = 5555
    
    # Permettre de spécifier host et port en arguments
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("❌ Le port doit être un nombre")
            sys.exit(1)
    
    client = ChatClient(host, port)
    client.start()
