# Chapitre 16 : Communication distribuée

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Utiliser le module socket pour TCP/UDP
- Créer des serveurs et clients TCP/UDP
- Comprendre la sérialisation (pickle, json, msgpack)
- Implémenter un système de messagerie distribué
- Gérer les erreurs réseau

---

## 1. Explication du principe

### 1.1 TCP vs UDP

**TCP (Transmission Control Protocol) :**
- Orienté connexion
- Fiable (garantit la livraison)
- Ordonné
- Plus lent

**UDP (User Datagram Protocol) :**
- Sans connexion
- Non fiable (pas de garantie)
- Plus rapide
- Utile pour le streaming, jeux

### 1.2 Sérialisation

**Pourquoi sérialiser ?**
Les données Python doivent être converties en bytes pour être envoyées sur le réseau.

**Formats :**
- **pickle** : Spécifique Python, peut exécuter du code (sécurité)
- **json** : Universel, texte, sûr
- **msgpack** : Binaire, efficace

**Points clés à retenir :**
- pickle : Rapide mais pas sûr pour données non fiables
- json : Sûr, universel, mais plus lent
- msgpack : Bon compromis

---

## 2. Exemple basique

### 2.1 Description

Communication TCP avec sérialisation JSON.

### 2.2 Code

```python
# serveur.py
import socket
import json

def serveur():
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket.bind(('localhost', 8888))
    serveur_socket.listen(5)
    
    print("Serveur démarré")
    
    while True:
        client_socket, adresse = serveur_socket.accept()
        print(f"Connexion de {adresse}")
        
        # Recevoir les données
        data = client_socket.recv(4096).decode()
        message = json.loads(data)
        
        print(f"Reçu: {message}")
        
        # Envoyer une réponse
        reponse = {"statut": "ok", "message": "Reçu"}
        client_socket.send(json.dumps(reponse).encode())
        
        client_socket.close()
```

```python
# client.py
import socket
import json

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))
    
    # Envoyer un message
    message = {"type": "hello", "data": "Bonjour serveur!"}
    client_socket.send(json.dumps(message).encode())
    
    # Recevoir la réponse
    reponse = client_socket.recv(4096).decode()
    data = json.loads(reponse)
    print(f"Réponse: {data}")
    
    client_socket.close()
```

---

## 3. Exemple avancé

### 3.1 Description

Système de messagerie distribué avec plusieurs clients.

### 3.2 Code

```python
import socket
import json
import threading
from datetime import datetime

class ServeurMessagerie:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.clients = []
        self.verrou = threading.Lock()
    
    def diffuser_message(self, message, expediteur):
        """Diffuse un message à tous les clients."""
        with self.verrou:
            for client_socket, _ in self.clients:
                if client_socket != expediteur:
                    try:
                        client_socket.send(json.dumps(message).encode())
                    except:
                        pass
    
    def gerer_client(self, client_socket, adresse):
        """Gère un client."""
        print(f"[{adresse}] Connexion")
        
        try:
            while True:
                data = client_socket.recv(4096).decode()
                if not data:
                    break
                
                message = json.loads(data)
                print(f"[{adresse}] {message['texte']}")
                
                # Diffuser à tous
                message['timestamp'] = datetime.now().isoformat()
                self.diffuser_message(message, client_socket)
        except Exception as e:
            print(f"[{adresse}] Erreur: {e}")
        finally:
            with self.verrou:
                self.clients = [(c, a) for c, a in self.clients if c != client_socket]
            client_socket.close()
            print(f"[{adresse}] Déconnexion")
    
    def demarrer(self):
        """Démarre le serveur."""
        serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur_socket.bind((self.host, self.port))
        serveur_socket.listen(5)
        
        print(f"Serveur démarré sur {self.host}:{self.port}")
        
        while True:
            client_socket, adresse = serveur_socket.accept()
            with self.verrou:
                self.clients.append((client_socket, adresse))
            
            thread = threading.Thread(
                target=self.gerer_client,
                args=(client_socket, adresse)
            )
            thread.start()

if __name__ == "__main__":
    serveur = ServeurMessagerie()
    serveur.demarrer()
```

---

## 4. Exercices

### Exercice 1 : Communication UDP

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Créer un client et serveur UDP

Créez un système de communication UDP simple.

### Exercice 2 : Sérialisation avec pickle

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Utiliser pickle pour la sérialisation

Créez un système qui envoie des objets Python complexes avec pickle.

### Exercice 3 : Système de fichiers distribué

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Créer un système de partage de fichiers

Créez un système où plusieurs clients peuvent partager des fichiers via un serveur.

---

## 5. Résumé

### Concepts clés
- ✅ **TCP** : Communication fiable, orientée connexion
- ✅ **UDP** : Communication rapide, sans connexion
- ✅ **Sérialisation** : Conversion données → bytes
- ✅ **JSON** : Format sûr et universel
- ✅ **pickle** : Format Python, rapide mais moins sûr

### Points importants à retenir
1. TCP est fiable mais plus lent
2. UDP est rapide mais non fiable
3. JSON est sûr pour données non fiables
4. pickle est rapide mais attention à la sécurité
5. Toujours gérer les erreurs réseau

---

## 6. Pour aller plus loin

- HTTP et REST APIs
- WebSockets
- gRPC
- Message queues (RabbitMQ, Kafka)

---

## 7. Questions de révision

1. Quelle est la différence entre TCP et UDP ?
2. Quand utiliseriez-vous UDP plutôt que TCP ?
3. Pourquoi sérialiser les données avant envoi ?
4. Quels sont les avantages/inconvénients de pickle vs JSON ?
5. Comment gérer les erreurs réseau dans un système distribué ?

---

*[Chapitre précédent : Chapitre 15 - Introduction à la programmation distribuée] | [Chapitre suivant : Chapitre 17 - Frameworks de distribution]*
