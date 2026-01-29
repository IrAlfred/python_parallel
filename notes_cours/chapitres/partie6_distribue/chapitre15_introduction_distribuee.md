# Chapitre 15 : Introduction à la programmation distribuée

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Comprendre les concepts de systèmes distribués
- Comprendre la communication réseau (TCP/IP, HTTP)
- Utiliser les sockets en Python
- Créer un client-serveur simple
- Comprendre les défis de la programmation distribuée

---

## 1. Explication du principe

### 1.1 Systèmes distribués

**Définition :**
Un système distribué est un ensemble de machines indépendantes qui travaillent ensemble pour accomplir une tâche.

**Caractéristiques :**
- Machines indépendantes
- Communication via réseau
- Pas de mémoire partagée
- Tolérance aux pannes

**Avantages :**
- Scalabilité horizontale
- Résilience (une machine peut tomber)
- Distribution géographique

**Défis :**
- Latence réseau
- Gestion des erreurs réseau
- Cohérence des données
- Synchronisation

### 1.2 Communication réseau

**TCP/IP :**
Protocole de communication fiable, orienté connexion.

**HTTP :**
Protocole applicatif basé sur TCP, utilisé pour le web.

**Sockets :**
Interface de programmation pour la communication réseau.

### 1.3 Sockets en Python

**Module socket :**
Le module `socket` permet de créer des connexions réseau.

**Types :**
- `socket.AF_INET` : IPv4
- `socket.SOCK_STREAM` : TCP
- `socket.SOCK_DGRAM` : UDP

---

## 2. Exemples basiques : aller en douceur

Dans cette section, nous allons progresser **étape par étape** :
- d’abord un serveur minimal qui accepte une connexion,
- puis un client minimal qui s’y connecte,
- ensuite seulement nous ajouterons l’envoi/réception de données.

### 2.1 Exemple basique 1 : serveur minimal

#### 2.1.1 Description

Nous commençons par le **serveur le plus simple possible** :
- il crée une socket TCP,
- il s’attache à l’adresse `('localhost', 8000)`,
- il se met en écoute,
- il accepte **une seule connexion**, puis s’arrête.

Pas encore de réception ou d’envoi de message : l’objectif est de comprendre le **cycle de vie de base** d’un serveur.

#### 2.1.2 Code

```python
import socket

def serveur():
    # Créer une socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associer la socket à une adresse (hôte, port)
    server.bind(('localhost', 8000))

    # Mettre le serveur en écoute (1 connexion en file d'attente max)
    server.listen(1)
    print("Serveur en écoute sur le port 8000...")

    # Attendre une connexion (appel bloquant)
    conn, addr = server.accept()
    print(f"Connexion de {addr}")

    # Fermer la connexion et la socket serveur
    conn.close()
    server.close()

if __name__ == "__main__":
    serveur()
```

#### 2.1.3 Explication

- `socket.socket(AF_INET, SOCK_STREAM)` : crée une socket TCP IPv4.
- `bind(('localhost', 8000))` : attache la socket à l’interface locale sur le port 8000.
- `listen(1)` : met la socket en mode écoute (prête à accepter des connexions).
- `accept()` : bloque jusqu’à ce qu’un client se connecte, retourne `(conn, addr)`.
- `conn.close()` et `server.close()` ferment proprement la connexion et le serveur.

À ce stade, lancer ce script **tout seul** ne sert à rien : il attend un client. Nous allons donc créer le client minimal.

---

### 2.2 Exemple basique 2 : client minimal

#### 2.2.1 Description

Le client minimal :
- crée une socket TCP,
- se connecte au serveur sur `('localhost', 8000)`,
- affiche un message indiquant la réussite de la connexion,
- ferme la socket.

Il ne fait encore **aucun échange de données**.

#### 2.2.2 Code

```python
import socket

def client():
    # Créer une socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Se connecter au serveur (doit déjà être lancé)
    client.connect(('localhost', 8000))
    print("Connecté au serveur sur le port 8000.")

    # Fermer la connexion
    client.close()

if __name__ == "__main__":
    client()
```

#### 2.2.3 Plan de test

1. Ouvrir un premier terminal et lancer le serveur :
   ```bash
   python serveur.py
   ```
2. Ouvrir un deuxième terminal et lancer le client :
   ```bash
   python client.py
   ```
3. Observer dans le terminal du serveur l’affichage de l’adresse du client.

---

### 2.3 Exemple basique 3 : ajout d’un message (echo simple)

#### 2.3.1 Description

Maintenant que la **connexion** est claire, nous ajoutons un tout petit peu de complexité :
- le client envoie un message texte au serveur,
- le serveur lit ce message et le ré-affiche (echo) au client,
- le serveur renvoie le même message au client,
- le client affiche la réponse.

#### 2.3.2 Code du serveur (echo une seule fois)

```python
# serveur_echo.py
import socket

def serveur_echo():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))
    server.listen(1)
    print("Serveur (echo) en écoute sur le port 8000...")

    conn, addr = server.accept()
    print(f"Connexion de {addr}")

    # Recevoir un message (jusqu'à 1024 octets)
    message = conn.recv(1024).decode()
    print(f"Message reçu du client : {message}")

    # Répondre (echo)
    reponse = f"Echo: {message}"
    conn.send(reponse.encode())

    conn.close()
    server.close()

if __name__ == "__main__":
    serveur_echo()
```

#### 2.3.3 Code du client

```python
# client_echo.py
import socket

def client_echo():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8000))
    print("Connecté au serveur (echo).")

    message = "Hello, serveur!"
    print(f"Envoi : {message}")
    client.send(message.encode())

    reponse = client.recv(1024).decode()
    print(f"Réponse du serveur : {reponse}")

    client.close()

if __name__ == "__main__":
    client_echo()
```

#### 2.3.4 Explication

- `recv(1024)` : lit jusqu’à 1024 octets sur la connexion TCP.
- `decode()` / `encode()` : conversion entre `bytes` (niveau réseau) et `str` (niveau Python).
- On gère **un seul client** et **un seul message**, pour garder les choses simples.

---

## 3. Exemple intermédiaire : plusieurs clients, sans threads

### 3.1 Description

Dans cet exemple, nous faisons un **pas de plus** :
- le serveur reste en écoute dans une boucle,
- il accepte **plusieurs connexions successives**,
- il traite chaque client l’un après l’autre (pas encore de parallélisme).

Cela permet de comprendre le passage de **un client** à **plusieurs clients** sans introduire encore les threads.

### 3.2 Code

```python
import socket

def serveur_multi_clients_sequentiel():
    """Serveur simple qui gère plusieurs clients, un par un (séquentiel)."""
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveur_socket.bind(('localhost', 8000))
    serveur_socket.listen(5)
    
    print("Serveur séquentiel démarré sur le port 8000")
    
    while True:
        print("En attente d'un nouveau client...")
        client_socket, adresse = serveur_socket.accept()
        print(f"[{adresse}] Connexion établie")
        
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print(f"[{adresse}] Aucun message reçu")
            else:
                print(f"[{adresse}] Reçu: {message}")
                reponse = f"Echo: {message}"
                client_socket.send(reponse.encode())
        except Exception as e:
            print(f"[{adresse}] Erreur: {e}")
        finally:
            client_socket.close()
            print(f"[{adresse}] Connexion fermée\n")

if __name__ == "__main__":
    serveur_multi_clients_sequentiel()
```

### 3.3 Analyse

- Les clients sont gérés **les uns après les autres** : si un client est lent, les autres attendent.
- C’est une étape importante avant d’introduire les threads, car la logique est encore simple.

---

## 4. Exemple avancé : serveur multi-clients avec threads

### 4.1 Description

Nous allons maintenant améliorer le serveur précédent en :
- créant un **thread par client**,
- permettant de gérer **plusieurs clients en parallèle**,
- gardant la même logique d’echo.

### 4.2 Code

```python
import socket
import threading

def gerer_client(client_socket, adresse):
    """Gère un client dans un thread dédié."""
    print(f"[{adresse}] Connexion établie")
    
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            
            print(f"[{adresse}] Reçu: {message}")
            reponse = f"Echo: {message}"
            client_socket.send(reponse.encode())
    except Exception as e:
        print(f"[{adresse}] Erreur: {e}")
    finally:
        client_socket.close()
        print(f"[{adresse}] Déconnexion")

def serveur_multi_clients():
    """Serveur qui gère plusieurs clients en parallèle grâce aux threads."""
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveur_socket.bind(('localhost', 8888))
    serveur_socket.listen(5)
    
    print("Serveur multi-clients (threads) démarré sur le port 8888")
    
    while True:
        client_socket, adresse = serveur_socket.accept()
        thread = threading.Thread(
            target=gerer_client,
            args=(client_socket, adresse),
            daemon=True  # Le thread se termine avec le processus principal
        )
        thread.start()

if __name__ == "__main__":
    serveur_multi_clients()
```

---

## 5. Exercices

### Exercice 1 : Client-serveur simple

**Difficulté** : ⭐ Facile  
**Objectif** : Créer un client et un serveur basiques

Créez un client et un serveur qui échangent des messages.

### Exercice 2 : Serveur multi-clients

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Gérer plusieurs clients simultanément

Créez un serveur qui peut gérer plusieurs clients en parallèle.

### Exercice 3 : Système de calcul distribué

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Distribuer des calculs sur plusieurs machines

Créez un système où un serveur distribue des calculs à des clients workers.

---

## 6. Résumé

### Concepts clés
- ✅ **Systèmes distribués** : Machines indépendantes qui coopèrent
- ✅ **Sockets** : Interface de communication réseau
- ✅ **TCP/IP** : Protocole de communication fiable
- ✅ **Client-Serveur** : Architecture de base

### Points importants à retenir
1. Les systèmes distribués utilisent le réseau
2. Les sockets permettent la communication bas niveau
3. TCP est fiable, UDP est plus rapide mais non fiable
4. La gestion des erreurs réseau est cruciale

---

## 7. Pour aller plus loin

- Documentation socket : https://docs.python.org/3/library/socket.html
- HTTP et REST APIs
- Frameworks de distribution (chapitre suivant)

---

## 8. Questions de révision

1. Qu'est-ce qu'un système distribué ?
2. Quelle est la différence entre TCP et UDP ?
3. Comment fonctionne un socket en Python ?
4. Pourquoi utiliser threading pour un serveur multi-clients ?
5. Quels sont les défis de la programmation distribuée ?

---

*[Chapitre précédent : Chapitre 14 - Gestion des erreurs et debugging] | [Chapitre suivant : Chapitre 16 - Communication distribuée]*
