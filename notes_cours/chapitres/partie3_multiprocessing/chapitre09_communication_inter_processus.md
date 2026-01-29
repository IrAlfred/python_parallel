# Chapitre 9 : Communication inter-processus

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Utiliser les Pipes pour la communication entre processus
- Utiliser les Queues pour partager des données
- Utiliser la mémoire partagée (Value, Array, Manager)
- Synchroniser les processus avec Lock, Event, Condition

---

## 1. Explication du principe

### 1.1 Pipes

**Qu'est-ce qu'un Pipe ?**
Un `Pipe` crée une connexion bidirectionnelle entre deux processus. C'est comme un tube où chaque processus peut envoyer et recevoir des données.

**Utilisation :**
```python
from multiprocessing import Process, Pipe
import os

# Créer un pipe avec deux connexions
parent_conn, child_conn = Pipe()

# Processus parent : envoyer et recevoir
def processus_parent(conn):
    conn.send(f"message du parent PID {os.getpid()}")  # Envoyer un message
    reponse = conn.recv()  # Recevoir la réponse
    print(reponse)

# Processus enfant : recevoir et envoyer
def processus_enfant(conn):
    message = conn.recv()  # Recevoir le message
    print(message)
    conn.send(f"réponse de l'enfant, PID {os.getpid()}")  # Envoyer une réponse

# Utilisation
p = Process(target=processus_enfant, args=(child_conn,))
p.start()
p_parent = Process(target=processus_parent, args=(parent_conn,))
p_parent.start()
p.join()
p_parent.join()
```

**Points clés à retenir :**
- Communication bidirectionnelle (les deux sens)
- Deux connexions : une pour chaque processus
- Plus simple que Queue pour deux processus
- Les messages sont reçus dans l'ordre

#### Exemple basique : Communication bidirectionnelle avec Pipe

**Description :**
Cet exemple montre comment utiliser un Pipe pour la communication bidirectionnelle entre deux processus. Un Pipe permet à chaque processus d'envoyer et de recevoir des données.

**Code :**

```python
from multiprocessing import Process, Pipe
import time
import os

def processus_enfant(conn_enfant):
    """Processus enfant qui communique via le pipe."""
    pid = os.getpid()
    print(f"[Enfant PID:{pid}] Démarrage")
    
    # Recevoir un message du parent
    message_parent = conn_enfant.recv()
    print(f"[Enfant PID:{pid}] Message reçu du parent: {message_parent}")
    
    # Envoyer une réponse
    reponse = f"Bonjour parent! Je suis le processus {pid}"
    conn_enfant.send(reponse)
    print(f"[Enfant PID:{pid}] Réponse envoyée au parent")
    
    # Fermer la connexion
    conn_enfant.close()
    print(f"[Enfant PID:{pid}] Connexion fermée")

def processus_parent(conn_parent):
    """Processus parent qui communique via le pipe."""
    pid = os.getpid()
    print(f"[Parent PID:{pid}] Démarrage")
    
    # Envoyer un message à l'enfant
    message = "Bonjour enfant!"
    conn_parent.send(message)
    print(f"[Parent PID:{pid}] Message envoyé à l'enfant: {message}")
    
    # Recevoir la réponse
    reponse = conn_parent.recv()
    print(f"[Parent PID:{pid}] Réponse reçue de l'enfant: {reponse}")
    
    # Fermer la connexion
    conn_parent.close()
    print(f"[Parent PID:{pid}] Connexion fermée")

if __name__ == "__main__":
    print("=== Communication bidirectionnelle avec Pipe ===\n")
    
    # Créer le pipe (deux connexions)
    conn_parent, conn_child = Pipe()
    
    # Créer et démarrer le processus enfant
    p_enfant = Process(target=processus_enfant, args=(conn_child,))
    p_enfant.start()
    
    # Le parent communique via conn_parent
    processus_parent(conn_parent)
    
    # Attendre que l'enfant se termine
    p_enfant.join()
    
    print("\n✓ Communication terminée")
```

**Explication :**
- `Pipe()` crée deux connexions : `conn_parent` et `conn_child`
- Le parent utilise `conn_parent.send()` et `conn_parent.recv()`
- L'enfant utilise `conn_child.send()` et `conn_child.recv()`
- La communication est bidirectionnelle : chaque processus peut envoyer et recevoir
- Il faut fermer les connexions avec `close()`

**Résultat attendu :**
```
=== Communication bidirectionnelle avec Pipe ===

[Enfant PID:12348] Démarrage
[Parent PID:12345] Démarrage
[Parent PID:12345] Message envoyé à l'enfant: Bonjour enfant!
[Enfant PID:12348] Message reçu du parent: Bonjour enfant!
[Enfant PID:12348] Réponse envoyée au parent
[Parent PID:12345] Réponse reçue de l'enfant: Bonjour parent! Je suis le processus 12348
[Parent PID:12345] Connexion fermée
[Enfant PID:12348] Connexion fermée

✓ Communication terminée
```

---

### 1.2 Queues

**Queue inter-processus :**
Similaire aux queues de threading mais pour les processus. Thread-safe et process-safe.

**Utilisation :**
```python
from multiprocessing import Process, Queue

# Créer une queue partagée
q = Queue()

# Processus producteur : envoyer des données
def producteur(queue_obj):
    queue_obj.put("donnee 1")
    queue_obj.put("donnee 2")
    queue_obj.put(None)  # Signal de fin

# Processus consommateur : recevoir des données
def consommateur(queue_obj):
    while True:
        item = queue_obj.get()  # Recevoir (bloque si vide)
        if item is None:  # Signal de fin
            break
        print(f"Reçu: {item}")

# Utilisation
p1 = Process(target=producteur, args=(q,))
p2 = Process(target=consommateur, args=(q,))
p1.start()
p2.start()
p1.join()
p2.join()
```

**Points clés à retenir :**
- Thread-safe et process-safe
- Communication unidirectionnelle (FIFO)
- Bloque automatiquement si vide/pleine
- Idéal pour le pattern producteur-consommateur

#### Exemple basique : Communication avec Queue

**Description :**
Cet exemple montre comment utiliser une Queue pour la communication entre processus. Une Queue est thread-safe et process-safe, ce qui en fait un mécanisme idéal pour partager des données entre processus.

**Code :**

```python
from multiprocessing import Process, Queue
import time
import os

def producteur(queue_obj, nb_items):
    """Produit des données et les envoie dans la queue."""
    pid = os.getpid()
    print(f"[Producteur PID:{pid}] Démarrage")
    
    for i in range(nb_items):
        item = f"Item-{i}"
        queue_obj.put(item)
        print(f"[Producteur PID:{pid}] Envoyé: {item}")
        time.sleep(0.3)
    
    # Signal de fin
    queue_obj.put(None)
    print(f"[Producteur PID:{pid}] Production terminée")

def consommateur(queue_obj, nom):
    """Consomme des données de la queue."""
    pid = os.getpid()
    print(f"[{nom} PID:{pid}] Démarrage")
    
    while True:
        try:
            item = queue_obj.get(timeout=5)
            if item is None:  # Signal de fin
                print(f"[{nom} PID:{pid}] Signal de fin reçu")
                break
            print(f"[{nom} PID:{pid}] Reçu: {item}")
            time.sleep(0.2)
        except:
            break
    
    print(f"[{nom} PID:{pid}] Consommation terminée")

if __name__ == "__main__":
    print("=== Communication inter-processus avec Queue ===\n")
    
    q = Queue()
    
    p = Process(target=producteur, args=(q, 5))
    c = Process(target=consommateur, args=(q, "Consommateur"))
    
    p.start()
    c.start()
    
    p.join()
    c.join()
    
    print("\n✓ Tous les processus sont terminés")
```

**Explication :**
- `Queue()` crée une queue partagée entre processus
- `queue_obj.put(item)` envoie un item dans la queue
- `queue_obj.get(timeout=5)` récupère un item (bloque avec timeout)
- On utilise `None` comme signal de fin
- La queue est automatiquement thread-safe et process-safe

**Résultat attendu :**
```
=== Communication inter-processus avec Queue ===

[Producteur PID:12346] Démarrage
[Consommateur PID:12347] Démarrage
[Producteur PID:12346] Envoyé: Item-0
[Consommateur PID:12347] Reçu: Item-0
[Producteur PID:12346] Envoyé: Item-1
[Consommateur PID:12347] Reçu: Item-1
[Producteur PID:12346] Envoyé: Item-2
[Consommateur PID:12347] Reçu: Item-2
[Producteur PID:12346] Envoyé: Item-3
[Consommateur PID:12347] Reçu: Item-3
[Producteur PID:12346] Envoyé: Item-4
[Consommateur PID:12347] Reçu: Item-4
[Producteur PID:12346] Production terminée
[Consommateur PID:12347] Signal de fin reçu
[Consommateur PID:12347] Consommation terminée

✓ Tous les processus sont terminés
```

#### Exemple basique 2 : Queue avec interaction utilisateur (stdin)

**Description :**
Cet exemple montre un cas d'usage important : l'interaction avec l'utilisateur via `input()` (stdin) depuis le processus principal, car stdin n'est pas disponible dans les processus enfants. La Queue permet de transmettre les données saisies par l'utilisateur au processus consommateur.

**Code :**

```python
from multiprocessing import Process, Queue
import os

def processus_consommateur(q):
    """
    Processus consommateur qui reçoit des messages de la queue.
    
    Args:
        q (Queue): Queue pour recevoir les messages
    """
    pid = os.getpid()
    print(f"[Consommateur PID:{pid}] Démarrage - En attente de messages...\n")
    
    while True:
        message = q.get()  # Bloque jusqu'à recevoir un message
        if message.lower() == 'exit':
            print(f"[Consommateur PID:{pid}] Signal de fin reçu")
            break
        print(f"[Consommateur PID:{pid}] Message reçu: {message}")

if __name__ == "__main__":
    print("=== Queue avec interaction utilisateur ===\n")
    print(f"Processus principal PID: {os.getpid()}\n")
    
    # Créer la queue
    q = Queue()
    
    # Créer et démarrer le processus consommateur
    p_cons = Process(target=processus_consommateur, args=(q,))
    p_cons.start()
    
    # Le processus principal gère l'input
    # Note: stdin n'est pas disponible dans les processus enfants,
    # donc on doit lire depuis le processus principal
    print("Tapez des messages (ou 'exit' pour quitter):\n")
    while True:
        message = input("Entrez un message à produire: ")
        q.put(message)  # Envoyer le message dans la queue
        print(f"[Principal] Produit: {message}\n")
        
        if message.lower() == 'exit':
            break
    
    # Attendre que le consommateur se termine
    p_cons.join()
    
    print("\n✓ Communication terminée")
```

**Explication :**
- Le processus principal lit depuis `stdin` avec `input()` (non disponible dans les processus enfants)
- Les messages saisis sont envoyés dans la queue avec `q.put(message)`
- Le processus consommateur récupère les messages avec `q.get()` (bloque jusqu'à recevoir)
- Le mot "exit" sert de signal de fin
- C'est un pattern utile pour les applications interactives avec multiprocessing

**Résultat attendu :**
```
=== Queue avec interaction utilisateur ===

Processus principal PID: 12345

Tapez des messages (ou 'exit' pour quitter):

[Consommateur PID:12346] Démarrage - En attente de messages...

Entrez un message à produire: Bonjour
[Principal] Produit: Bonjour

[Consommateur PID:12346] Message reçu: Bonjour
Entrez un message à produire: Comment allez-vous?
[Principal] Produit: Comment allez-vous?

[Consommateur PID:12346] Message reçu: Comment allez-vous?
Entrez un message à produire: exit
[Principal] Produit: exit

[Consommateur PID:12346] Signal de fin reçu

✓ Communication terminée
```

**Points importants :**
- `stdin` (input) n'est disponible que dans le processus principal
- La Queue permet de transmettre les données saisies aux processus enfants
- Pattern utile pour les applications interactives
- Le processus consommateur peut traiter les messages en arrière-plan

---

### 1.3 Mémoire partagée

**Value et Array :**
Permettent de partager des valeurs simples ou des tableaux entre processus.

**Utilisation :**
```python
from multiprocessing import Process, Value, Array, Lock

# Créer une valeur partagée (type 'i' = entier)
compteur = Value('i', 0)

# Créer un array partagé (type 'i' = entier, taille 5)
array_shared = Array('i', [0, 0, 0, 0, 0])

# Créer un verrou pour synchroniser
verrou = Lock()

# Processus qui modifie la valeur partagée
def worker(compteur, array_shared, verrou):
    # Lire la valeur
    valeur = compteur.value
    
    # Modifier avec protection
    with verrou:
        compteur.value += 1  # Modifier la valeur
        array_shared[0] = 10  # Modifier l'array
    
    # Lire après modification
    nouvelle_valeur = compteur.value
    element = array_shared[0]

# Utilisation
p = Process(target=worker, args=(compteur, array_shared, verrou))
p.start()
p.join()

# Accéder aux valeurs depuis le processus principal
print(f"Compteur: {compteur.value}")
print(f"Array: {list(array_shared)}")
```

**Manager :**
Permet de partager des structures plus complexes (listes, dictionnaires).

**Utilisation Manager :**
```python
from multiprocessing import Process, Manager, Lock

# Créer un manager
manager = Manager()

# Créer des structures partagées
liste_partagee = manager.list([1, 2, 3])
dict_partage = manager.dict({'cle': 'valeur'})

# Processus qui modifie
def worker(liste, dico, verrou):
    with verrou:
        liste.append(4)  # Ajouter un élément
        dico['nouvelle_cle'] = 'nouvelle_valeur'  # Modifier le dictionnaire

# Utilisation
verrou = Lock()
p = Process(target=worker, args=(liste_partagee, dict_partage, verrou))
p.start()
p.join()
```

**Points clés à retenir :**
- Value/Array : Pour des données simples, plus performant
- Manager : Pour des structures complexes, moins performant
- Toujours synchroniser avec un Lock
- Moins performant que la mémoire isolée mais nécessaire pour le partage

#### Exemple basique : Mémoire partagée avec Value et Array

**Description :**
Cet exemple montre comment utiliser `Value` et `Array` pour partager des données simples entre processus. Contrairement à Manager, Value et Array sont plus performants car ils utilisent la mémoire partagée directement.

**Code :**

```python
from multiprocessing import Process, Value, Array, Lock
import time
import os

def incrementer_compteur(compteur, verrou, nom):
    """Incrémente un compteur partagé."""
    pid = os.getpid()
    print(f"[{nom} PID:{pid}] Démarrage")
    
    for i in range(5):
        with verrou:  # Protéger l'accès
            compteur.value += 1
            valeur_actuelle = compteur.value
        print(f"[{nom} PID:{pid}] Compteur: {valeur_actuelle}")
        time.sleep(0.1)

def modifier_array(array_shared, verrou, nom, index):
    """Modifie un élément de l'array partagé."""
    pid = os.getpid()
    print(f"[{nom} PID:{pid}] Démarrage")
    
    for i in range(3):
        with verrou:
            ancienne_valeur = array_shared[index]
            array_shared[index] = ancienne_valeur + 10
            nouvelle_valeur = array_shared[index]
        print(f"[{nom} PID:{pid}] Array[{index}]: {ancienne_valeur} -> {nouvelle_valeur}")
        time.sleep(0.2)

if __name__ == "__main__":
    print("=== Mémoire partagée avec Value et Array ===\n")
    
    # Créer un compteur partagé (type 'i' = entier)
    compteur = Value('i', 0)
    
    # Créer un array partagé de 5 entiers
    array_shared = Array('i', [0, 0, 0, 0, 0])
    
    # Créer un verrou pour synchroniser
    verrou = Lock()
    
    print(f"Compteur initial: {compteur.value}")
    print(f"Array initial: {list(array_shared)}\n")
    
    # Créer des processus pour le compteur
    processus_compteur = []
    for i in range(3):
        p = Process(target=incrementer_compteur, 
                   args=(compteur, verrou, f"P-C{i}"))
        processus_compteur.append(p)
        p.start()
    
    # Créer des processus pour l'array
    processus_array = []
    for i in range(3):
        p = Process(target=modifier_array, 
                   args=(array_shared, verrou, f"P-A{i}", i))
        processus_array.append(p)
        p.start()
    
    # Attendre tous les processus
    for p in processus_compteur + processus_array:
        p.join()
    
    print(f"\nCompteur final: {compteur.value}")
    print(f"Array final: {list(array_shared)}")
    print("\n✓ Tous les processus sont terminés")
```

**Explication :**
- `Value('i', 0)` crée un entier partagé (type 'i' = int)
- `Array('i', [0, 0, 0, 0, 0])` crée un array de 5 entiers partagés
- `compteur.value` accède à la valeur partagée
- `array_shared[index]` accède à un élément de l'array
- Le verrou (`Lock()`) protège les accès concurrents
- Tous les processus voient les modifications des autres

**Résultat attendu :**
```
=== Mémoire partagée avec Value et Array ===

Compteur initial: 0
Array initial: [0, 0, 0, 0, 0]

[P-C0 PID:12349] Démarrage
[P-C1 PID:12350] Démarrage
[P-C2 PID:12351] Démarrage
[P-A0 PID:12352] Démarrage
[P-A1 PID:12353] Démarrage
[P-A2 PID:12354] Démarrage
[P-C0 PID:12349] Compteur: 1
[P-C1 PID:12350] Compteur: 2
[P-C2 PID:12351] Compteur: 3
[P-A0 PID:12352] Array[0]: 0 -> 10
[P-C0 PID:12349] Compteur: 4
[P-A1 PID:12353] Array[1]: 0 -> 10
...
[P-C2 PID:12351] Compteur: 15
[P-A2 PID:12354] Array[2]: 20 -> 30

Compteur final: 15
Array final: [30, 30, 30, 0, 0]

✓ Tous les processus sont terminés
```

**Points importants :**
- `Value` et `Array` utilisent la mémoire partagée (plus rapide que Manager)
- Le verrou est essentiel pour éviter les race conditions
- Chaque processus voit les modifications des autres
- Les types doivent être spécifiés ('i' pour int, 'd' pour double, etc.)

---


## 3. Exemple avancé

### 3.1 Description

Mémoire partagée avec Manager pour un compteur partagé.

### 3.2 Code

```python
from multiprocessing import Process, Manager, Lock
import time

def incrementer(compteur, verrou, nom):
    """Incrémente un compteur partagé."""
    for _ in range(5):
        with verrou:
            compteur['valeur'] += 1
            print(f"[{nom}] Compteur: {compteur['valeur']}")
        time.sleep(0.1)

if __name__ == "__main__":
    manager = Manager()
    compteur = manager.dict({'valeur': 0})
    verrou = Lock()
    
    processus = []
    for i in range(3):
        p = Process(target=incrementer, args=(compteur, verrou, f"P{i}"))
        processus.append(p)
        p.start()
    
    for p in processus:
        p.join()
    
    print(f"\nValeur finale: {compteur['valeur']}")
```

---

## 4. Exercices

### Exercice 1 : Communication avec Pipe

**Difficulté** : ⭐ Facile  
**Objectif** : Utiliser Pipe pour la communication

Créez deux processus qui communiquent via un Pipe.

### Exercice 2 : Mémoire partagée avec Value

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Partager une valeur simple

Créez plusieurs processus qui partagent un compteur avec Value.

### Exercice 3 : Système distribué avec Manager

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Utiliser Manager pour des structures complexes

Créez un système où plusieurs processus partagent un dictionnaire via Manager.

---

## 5. Résumé

### Concepts clés
- ✅ **Pipe** : Communication bidirectionnelle
- ✅ **Queue** : Communication thread-safe et process-safe
- ✅ **Value/Array** : Mémoire partagée pour données simples
- ✅ **Manager** : Mémoire partagée pour structures complexes

### Points importants à retenir
1. Les processus ont une mémoire isolée
2. La communication nécessite des mécanismes spéciaux
3. Manager est pratique mais moins performant
4. Toujours synchroniser les accès à la mémoire partagée

---

## 6. Pour aller plus loin

- Communication réseau entre processus
- Sérialisation avec pickle
- Performance de la mémoire partagée

---

## 7. Questions de révision

1. Quelle est la différence entre Pipe et Queue ?
2. Quand utiliseriez-vous Value plutôt que Manager ?
3. Pourquoi faut-il synchroniser l'accès à la mémoire partagée ?
4. Quels sont les avantages et inconvénients de Manager ?
5. Comment choisir entre Pipe, Queue et mémoire partagée ?

---

*[Chapitre précédent : Chapitre 8 - Pool de processus] | [Chapitre suivant : Chapitre 10 - Introduction à l'asynchrone]*
