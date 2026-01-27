#!/usr/bin/env python3
"""
Serveur de chat multi-clients avec messagerie privée
Utilise socket et threading pour gérer plusieurs connexions simultanées
"""

import socket
import threading
import json
from datetime import datetime

class ChatServer:
    def __init__(self, host='192.168.1.104', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Dictionnaire des clients connectés: {nom: socket}
        self.clients = {}
        # Lock pour synchroniser l'accès au dictionnaire clients
        self.clients_lock = threading.Lock()
        
    def start(self):
        """Démarre le serveur et attend les connexions"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"[SERVEUR] Démarré sur {self.host}:{self.port}")
            print(f"[SERVEUR] En attente de connexions...")
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"[SERVEUR] Nouvelle connexion depuis {address}")
                
                # Créer un thread pour gérer ce client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n[SERVEUR] Arrêt du serveur...")
        finally:
            self.shutdown()
    
    def handle_client(self, client_socket, address):
        """Gère la communication avec un client spécifique"""
        client_name = None
        
        try:
            # Demander le nom du client
            client_socket.send("ENTER_NAME".encode('utf-8'))
            client_name = client_socket.recv(1024).decode('utf-8').strip()
            
            # Vérifier si le nom est déjà utilisé
            with self.clients_lock:
                if client_name in self.clients:
                    client_socket.send("NAME_TAKEN".encode('utf-8'))
                    client_socket.close()
                    return
                
                # Ajouter le client
                self.clients[client_name] = client_socket
                
            print(f"[SERVEUR] '{client_name}' a rejoint le chat")
            
            # Envoyer message de bienvenue
            welcome_msg = f"\n{'='*50}\n🎉 Bienvenue {client_name}! 🎉\n{'='*50}\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Envoyer la liste des clients connectés
            self.send_clients_list(client_socket, client_name)
            
            # Informer les autres clients de la nouvelle connexion
            self.broadcast(f"[SYSTÈME] {client_name} a rejoint le chat", exclude=client_name)
            
            # Envoyer les instructions
            instructions = """
📋 COMMANDES DISPONIBLES:
   /list          - Afficher la liste des clients connectés
   /to <nom>      - Envoyer un message privé à un client
   /all <message> - Envoyer un message à tous
   /quit          - Quitter le chat
   
💬 Tapez simplement votre message pour envoyer à tous
"""
            client_socket.send(instructions.encode('utf-8'))
            
            # Boucle de réception des messages
            while True:
                message = client_socket.recv(4096).decode('utf-8').strip()
                
                if not message:
                    break
                
                # Traiter les commandes
                if message.startswith('/'):
                    self.handle_command(client_name, message, client_socket)
                else:
                    # Message broadcast par défaut
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    formatted_msg = f"[{timestamp}] {client_name}: {message}"
                    self.broadcast(formatted_msg, exclude=client_name)
                    
        except Exception as e:
            print(f"[ERREUR] Client {client_name}: {e}")
        finally:
            # Nettoyer la connexion
            if client_name:
                with self.clients_lock:
                    if client_name in self.clients:
                        del self.clients[client_name]
                
                print(f"[SERVEUR] '{client_name}' s'est déconnecté")
                self.broadcast(f"[SYSTÈME] {client_name} a quitté le chat", exclude=client_name)
            
            client_socket.close()
    
    def handle_command(self, sender, message, sender_socket):
        """Traite les commandes du client"""
        parts = message.split(maxsplit=1)
        command = parts[0].lower()
        
        if command == '/list':
            self.send_clients_list(sender_socket, sender)
            
        elif command == '/to' and len(parts) > 1:
            # Format: /to nom:message
            try:
                recipient_and_msg = parts[1].split(maxsplit=1)
                if len(recipient_and_msg) < 2:
                    sender_socket.send("❌ Format incorrect. Utilisez: /to <nom> <message>\n".encode('utf-8'))
                    return
                
                recipient = recipient_and_msg[0]
                private_msg = recipient_and_msg[1]
                
                self.send_private_message(sender, recipient, private_msg, sender_socket)
            except Exception as e:
                sender_socket.send(f"❌ Erreur: {e}\n".encode('utf-8'))
                
        elif command == '/all' and len(parts) > 1:
            broadcast_msg = parts[1]
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_msg = f"[{timestamp}] {sender} (à tous): {broadcast_msg}"
            self.broadcast(formatted_msg, exclude=sender)
            sender_socket.send(f"✓ Message envoyé à tous\n".encode('utf-8'))
            
        elif command == '/quit':
            sender_socket.send("👋 Au revoir!\n".encode('utf-8'))
            sender_socket.close()
            
        else:
            sender_socket.send("❌ Commande inconnue. Tapez /list pour voir les commandes\n".encode('utf-8'))
    
    def send_private_message(self, sender, recipient, message, sender_socket):
        """Envoie un message privé d'un client à un autre"""
        with self.clients_lock:
            if recipient not in self.clients:
                sender_socket.send(f"❌ Client '{recipient}' non trouvé\n".encode('utf-8'))
                return
            
            recipient_socket = self.clients[recipient]
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        private_msg = f"[{timestamp}] 💌 Message privé de {sender}: {message}\n"
        
        try:
            recipient_socket.send(private_msg.encode('utf-8'))
            sender_socket.send(f"✓ Message privé envoyé à {recipient}\n".encode('utf-8'))
        except:
            sender_socket.send(f"❌ Impossible d'envoyer le message à {recipient}\n".encode('utf-8'))
    
    def send_clients_list(self, client_socket, current_client):
        """Envoie la liste des clients connectés"""
        with self.clients_lock:
            clients_list = list(self.clients.keys())
        
        if len(clients_list) <= 1:
            msg = "\n👥 CLIENTS CONNECTÉS:\n   Vous êtes seul pour le moment\n"
        else:
            msg = "\n👥 CLIENTS CONNECTÉS:\n"
            for name in clients_list:
                if name == current_client:
                    msg += f"   • {name} (vous)\n"
                else:
                    msg += f"   • {name}\n"
        
        client_socket.send(msg.encode('utf-8'))
    
    def broadcast(self, message, exclude=None):
        """Envoie un message à tous les clients sauf celui exclu"""
        message_with_newline = message + "\n"
        
        with self.clients_lock:
            disconnected = []
            for name, client_socket in self.clients.items():
                if name != exclude:
                    try:
                        client_socket.send(message_with_newline.encode('utf-8'))
                    except:
                        disconnected.append(name)
            
            # Nettoyer les clients déconnectés
            for name in disconnected:
                del self.clients[name]
    
    def shutdown(self):
        """Arrête proprement le serveur"""
        print("[SERVEUR] Fermeture des connexions...")
        
        with self.clients_lock:
            for client_socket in self.clients.values():
                try:
                    client_socket.send("SERVER_SHUTDOWN".encode('utf-8'))
                    client_socket.close()
                except:
                    pass
            self.clients.clear()
        
        self.server_socket.close()
        print("[SERVEUR] Arrêté")


if __name__ == "__main__":
    server = ChatServer(host='127.0.0.1', port=5555)
    server.start()
