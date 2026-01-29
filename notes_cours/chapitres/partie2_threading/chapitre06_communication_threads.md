# Chapitre 6 : Communication entre Threads

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Utiliser les queues (Queue, LifoQueue, PriorityQueue) pour la communication thread-safe
- Comprendre les collections thread-safe
- Partager des données entre threads de manière sûre
- Utiliser le thread-local storage pour des variables locales aux threads

---

## 1. Explication du principe

### 1.1 Queue (File d'attente)

**Qu'est-ce qu'une Queue ?**
Une `Queue` est une structure de données thread-safe qui permet à plusieurs threads de mettre et retirer des éléments de manière sûre. C'est comme une file d'attente : premier arrivé, premier servi (FIFO).

**Types de queues :**
- `Queue` : FIFO (First In, First Out)
- `LifoQueue` : LIFO (Last In, First Out) - comme une pile
- `PriorityQueue` : Éléments triés par priorité

**Méthodes principales :**
- `put(item)` : Ajoute un élément
- `get()` : Retire un élément (bloque si la queue est vide)
- `empty()` : Vérifie si la queue est vide
- `qsize()` : Taille de la queue

**Points clés à retenir :**
- Thread-safe par défaut
- Bloque automatiquement si vide/pleine
- Parfait pour le pattern producteur-consommateur

### 1.2 Thread-safe collections

**Collections thread-safe :**
Certaines collections Python sont thread-safe pour certaines opérations, mais pas toutes. Pour une sécurité totale, utilisez des verrous ou des queues.

**Points clés à retenir :**
- Les queues sont thread-safe
- Les dictionnaires/listes standards ne le sont pas complètement
- Utilisez des verrous pour protéger les accès

### 1.3 Thread-local storage

**Qu'est-ce que le thread-local storage ?**
Le thread-local storage permet à chaque thread d'avoir sa propre copie d'une variable. Chaque thread voit sa propre valeur, même si la variable a le même nom.

**Utilisation :**
```python
local_data = threading.local()
local_data.valeur = 10  # Chaque thread a sa propre valeur
```

**Points clés à retenir :**
- Chaque thread a sa propre copie
- Utile pour éviter le partage de données
- Réduit le besoin de synchronisation

---

## 2. Exemple basique

### 2.1 Description

Exemple simple d'utilisation d'une Queue pour la communication entre threads.

### 2.2 Code

```python
import threading
import queue
import time

def producteur(queue_obj, nb_items):
    """Produit des items et les met dans la queue."""
    for i in range(nb_items):
        item = f"Item-{i}"
        queue_obj.put(item)
        print(f"[Producteur] Produit: {item}")
        time.sleep(0.1)

def consommateur(queue_obj, nom):
    """Consomme des items de la queue."""
    while True:
        try:
            item = queue_obj.get(timeout=2)
            print(f"[{nom}] Consommé: {item}")
            queue_obj.task_done()
        except queue.Empty:
            print(f"[{nom}] Timeout, fin")
            break

if __name__ == "__main__":
    q = queue.Queue()
    
    # Créer les threads
    p = threading.Thread(target=producteur, args=(q, 10))
    c1 = threading.Thread(target=consommateur, args=(q, "Consommateur-1"))
    c2 = threading.Thread(target=consommateur, args=(q, "Consommateur-2"))
    
    p.start()
    c1.start()
    c2.start()
    
    p.join()
    q.join()  # Attend que tous les items soient traités
    print("Terminé")
```

---

## 3. Exemple avancé

### 3.1 Description

Système de tâches avec file d'attente prioritaire.

### 3.2 Code

```python
import threading
import queue
import time

class Tache:
    """Représente une tâche avec priorité."""
    def __init__(self, nom, priorite, duree):
        self.nom = nom
        self.priorite = priorite  # Plus petit = plus prioritaire
        self.duree = duree
    
    def __lt__(self, other):
        return self.priorite < other.priorite

def worker(queue_obj, nom):
    """Worker qui traite les tâches."""
    while True:
        try:
            tache = queue_obj.get(timeout=1)
            print(f"[{nom}] Traitement: {tache.nom} (priorité: {tache.priorite})")
            time.sleep(tache.duree)
            print(f"[{nom}] Terminé: {tache.nom}")
            queue_obj.task_done()
        except queue.Empty:
            break

if __name__ == "__main__":
    q = queue.PriorityQueue()
    
    # Ajouter des tâches avec différentes priorités
    taches = [
        Tache("Tâche urgente", 1, 0.5),
        Tache("Tâche normale", 5, 1.0),
        Tache("Tâche importante", 2, 0.8),
        Tache("Tâche basse", 10, 1.5),
    ]
    
    for tache in taches:
        q.put(tache)
    
    # Créer des workers
    workers = []
    for i in range(2):
        w = threading.Thread(target=worker, args=(q, f"Worker-{i}"))
        workers.append(w)
        w.start()
    
    q.join()
    print("Toutes les tâches sont terminées")
```

---

## 4. Exercices

### Exercice 1 : Communication simple avec Queue

**Difficulté** : ⭐ Facile  
**Objectif** : Utiliser une Queue pour la communication

Créez un programme où un thread envoie des nombres et un autre les reçoit et les affiche.

### Exercice 2 : Thread-local storage

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Utiliser le thread-local storage

Créez un programme où chaque thread a son propre compteur local.

### Exercice 3 : Système de traitement avec LifoQueue

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Implémenter un système avec LifoQueue

Créez un système où les dernières tâches ajoutées sont traitées en premier.

---

## 5. Résumé

### Concepts clés
- ✅ **Queue** : Communication thread-safe FIFO
- ✅ **LifoQueue** : Communication LIFO (pile)
- ✅ **PriorityQueue** : Éléments triés par priorité
- ✅ **Thread-local storage** : Variables locales à chaque thread

### Points importants à retenir
1. Les queues sont thread-safe et bloquantes
2. Utilisez `task_done()` et `join()` pour suivre la progression
3. Le thread-local storage évite le partage de données
4. PriorityQueue trie automatiquement par priorité

---

## 6. Pour aller plus loin

- Documentation queue : https://docs.python.org/3/library/queue.html
- Pattern producteur-consommateur avancé
- Thread pools avec queues

---

## 7. Questions de révision

1. Quelle est la différence entre `Queue`, `LifoQueue` et `PriorityQueue` ?
2. Pourquoi `Queue.get()` bloque-t-il si la queue est vide ?
3. À quoi sert `task_done()` et `join()` sur une Queue ?
4. Quand utiliseriez-vous le thread-local storage ?
5. Comment fonctionne `PriorityQueue` avec des objets personnalisés ?

---

*[Chapitre précédent : Chapitre 5 - Synchronisation avec Threads] | [Chapitre suivant : Chapitre 7 - Multiprocessing - Les bases]*
