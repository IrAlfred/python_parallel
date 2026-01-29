# Chapitre 5 : Synchronisation avec Threads

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Utiliser les verrous (Lock, RLock) pour protéger les ressources partagées
- Comprendre et utiliser les sémaphores
- Utiliser les événements (Events) pour la coordination entre threads
- Maîtriser les conditions (Conditions) pour des synchronisations complexes
- Utiliser les barrières (Barriers) pour synchroniser plusieurs threads

---

## 1. Explication du principe

### 1.1 Verrous (Locks)

**Lock (Verrou simple) :**
Un `Lock` permet à un seul thread d'accéder à une ressource à la fois. C'est le mécanisme de synchronisation le plus basique.

**RLock (Reentrant Lock) :**
Un `RLock` permet au même thread d'acquérir le verrou plusieurs fois. Utile quand une fonction protégée appelle une autre fonction protégée.

**Utilisation avec contexte manager :**
```python
with verrou:
    # Code protégé
    pass
```

**Points clés à retenir :**
- `Lock` : Un thread à la fois
- `RLock` : Permet les acquisitions multiples par le même thread
- Toujours utiliser `with` ou `try/finally` pour garantir la libération

### 1.2 Sémaphores

**Qu'est-ce qu'un sémaphore ?**
Un sémaphore permet à N threads d'accéder simultanément à une ressource. C'est comme un parking avec N places : N voitures peuvent entrer en même temps.

**Utilisation :**
```python
semaphore = threading.Semaphore(3)  # 3 threads maximum
with semaphore:
    # Code exécuté par max 3 threads
    pass
```

**Points clés à retenir :**
- Contrôle le nombre de threads simultanés
- Utile pour limiter l'accès à une ressource
- Plus flexible qu'un simple Lock

### 1.3 Événements (Events)

**Qu'est-ce qu'un Event ?**
Un `Event` permet à un thread de signaler un événement à d'autres threads. Les threads peuvent attendre qu'un événement se produise.

**Méthodes principales :**
- `set()` : Signale l'événement
- `wait()` : Attend que l'événement soit signalé
- `clear()` : Réinitialise l'événement
- `is_set()` : Vérifie si l'événement est signalé

**Points clés à retenir :**
- Permet la coordination entre threads
- Un thread peut signaler, d'autres peuvent attendre
- Utile pour démarrer/arrêter des threads

### 1.4 Conditions (Conditions)

**Qu'est-ce qu'une Condition ?**
Une `Condition` combine un verrou avec une condition logique. Les threads attendent qu'une condition soit vraie avant de continuer.

**Utilisation typique :**
```python
condition = threading.Condition(verrou)
with condition:
    while not condition_est_vraie:
        condition.wait()
    # Faire quelque chose
    condition.notify_all()
```

**Points clés à retenir :**
- Combine verrou et condition logique
- `wait()` libère le verrou et attend
- `notify()` ou `notify_all()` réveille les threads en attente
- Parfait pour le pattern producteur-consommateur

### 1.5 Barrières (Barriers)

**Qu'est-ce qu'une Barrière ?**
Une `Barrier` synchronise un nombre fixe de threads. Tous les threads doivent atteindre la barrière avant que n'importe lequel puisse continuer.

**Utilisation :**
```python
barriere = threading.Barrier(3)  # 3 threads
barriere.wait()  # Attend que les 3 threads arrivent
```

**Points clés à retenir :**
- Synchronise un nombre fixe de threads
- Tous doivent arriver avant de continuer
- Utile pour des phases de traitement

---

## 2. Exemple basique

### 2.1 Description

Nous allons créer un exemple qui montre l'utilisation d'un Lock pour protéger une ressource partagée (un compteur).

### 2.2 Code

```python
import threading
import time

# Compteur partagé
compteur = 0
verrou = threading.Lock()

def incrementer(nb_fois):
    """Incrémente le compteur plusieurs fois."""
    global compteur
    
    for _ in range(nb_fois):
        with verrou:  # Acquiert le verrou
            valeur = compteur
            time.sleep(0.0001)  # Simule un travail
            compteur = valeur + 1
        # Le verrou est libéré automatiquement

if __name__ == "__main__":
    threads = []
    for i in range(5):
        t = threading.Thread(target=incrementer, args=(100,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Valeur finale : {compteur} (attendu: 500)")
```

### 2.3 Explication

Le verrou protège l'accès au compteur. Sans verrou, il y aurait une race condition. Avec le verrou, chaque incrémentation est atomique.

### 2.4 Résultat attendu

```
Valeur finale : 500 (attendu: 500)
```

---

## 3. Exemple avancé

### 3.1 Description

Implémentation d'un pattern producteur-consommateur avec Conditions.

### 3.2 Code

```python
import threading
import time
import random

class Buffer:
    """Buffer thread-safe pour le pattern producteur-consommateur."""
    
    def __init__(self, capacite_max=5):
        self.capacite_max = capacite_max
        self.buffer = []
        self.verrou = threading.Lock()
        self.condition = threading.Condition(self.verrou)
    
    def produire(self, item):
        """Ajoute un item au buffer."""
        with self.condition:
            # Attendre qu'il y ait de la place
            while len(self.buffer) >= self.capacite_max:
                print(f"[Producteur] Buffer plein, attente...")
                self.condition.wait()
            
            self.buffer.append(item)
            print(f"[Producteur] Produit: {item}, Buffer: {len(self.buffer)}/{self.capacite_max}")
            self.condition.notify_all()  # Réveille les consommateurs
    
    def consommer(self):
        """Retire un item du buffer."""
        with self.condition:
            # Attendre qu'il y ait un item
            while len(self.buffer) == 0:
                print(f"[Consommateur] Buffer vide, attente...")
                self.condition.wait()
            
            item = self.buffer.pop(0)
            print(f"[Consommateur] Consommé: {item}, Buffer: {len(self.buffer)}/{self.capacite_max}")
            self.condition.notify_all()  # Réveille les producteurs
            return item

def producteur(buffer, nb_items):
    """Thread producteur."""
    for i in range(nb_items):
        time.sleep(random.uniform(0.1, 0.5))
        buffer.produire(f"Item-{i}")

def consommateur(buffer, nom, nb_items):
    """Thread consommateur."""
    for _ in range(nb_items):
        time.sleep(random.uniform(0.2, 0.6))
        item = buffer.consommer()

if __name__ == "__main__":
    buffer = Buffer(capacite_max=3)
    
    # Créer les threads
    p = threading.Thread(target=producteur, args=(buffer, 10))
    c1 = threading.Thread(target=consommateur, args=(buffer, "C1", 5))
    c2 = threading.Thread(target=consommateur, args=(buffer, "C2", 5))
    
    p.start()
    c1.start()
    c2.start()
    
    p.join()
    c1.join()
    c2.join()
```

### 3.3 Explication

Les Conditions permettent une synchronisation fine : les producteurs attendent quand le buffer est plein, les consommateurs attendent quand il est vide. `notify_all()` réveille tous les threads en attente.

---

## 4. Exercices

### Exercice 1 : Utiliser un Semaphore

**Difficulté** : ⭐ Facile  
**Objectif** : Limiter l'accès à une ressource avec un sémaphore

**Énoncé :**
Créez un programme avec un sémaphore qui limite à 3 threads simultanés l'accès à une fonction qui simule un travail.

**Solution :**

```python
import threading
import time

semaphore = threading.Semaphore(3)

def travail(identifiant):
    with semaphore:
        print(f"Thread {identifiant} commence")
        time.sleep(2)
        print(f"Thread {identifiant} termine")

threads = []
for i in range(10):
    t = threading.Thread(target=travail, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

---

### Exercice 2 : Utiliser un Event

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Coordonner des threads avec un Event

**Énoncé :**
Créez un programme où un thread "chef" donne le signal de départ à plusieurs threads "travailleurs".

**Solution :**

```python
import threading
import time

event_depart = threading.Event()

def travailleur(nom):
    print(f"[{nom}] En attente du signal...")
    event_depart.wait()
    print(f"[{nom}] Démarrage du travail!")

# Créer les travailleurs
travailleurs = []
for i in range(5):
    t = threading.Thread(target=travailleur, args=(f"Worker-{i}",))
    travailleurs.append(t)
    t.start()

time.sleep(2)
print("\n[Chef] Signal de départ!")
event_depart.set()

for t in travailleurs:
    t.join()
```

---

### Exercice 3 : Utiliser une Barrière

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Synchroniser plusieurs threads avec une barrière

**Énoncé :**
Créez un programme où 4 threads doivent tous terminer une phase avant de passer à la phase suivante.

**Solution :**

```python
import threading
import time
import random

barriere = threading.Barrier(4)

def phase_travail(nom_thread, phase_num):
    print(f"[{nom_thread}] Phase {phase_num} - Début")
    time.sleep(random.uniform(0.5, 2.0))
    print(f"[{nom_thread}] Phase {phase_num} - Terminée")
    barriere.wait()  # Attend que tous arrivent
    print(f"[{nom_thread}] Tous les threads ont terminé la phase {phase_num}")

def thread_complet(nom):
    for phase in range(1, 4):
        phase_travail(nom, phase)

threads = []
for i in range(4):
    t = threading.Thread(target=thread_complet, args=(f"Thread-{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

---

## 5. Résumé

### Concepts clés
- ✅ **Lock/RLock** : Verrous pour protéger les ressources
- ✅ **Semaphore** : Limite le nombre de threads simultanés
- ✅ **Event** : Signalisation entre threads
- ✅ **Condition** : Synchronisation basée sur des conditions
- ✅ **Barrier** : Synchronisation d'un nombre fixe de threads

### Points importants à retenir
1. Utilisez `Lock` pour protéger les ressources partagées
2. `Semaphore` pour limiter l'accès concurrent
3. `Event` pour la coordination simple
4. `Condition` pour des synchronisations complexes (producteur-consommateur)
5. `Barrier` pour synchroniser des phases de traitement

---

## 6. Pour aller plus loin

- Documentation threading : https://docs.python.org/3/library/threading.html
- Pattern producteur-consommateur
- Reader-Writer locks

---

## 7. Questions de révision

1. Quelle est la différence entre `Lock` et `RLock` ?
2. Quand utiliseriez-vous un `Semaphore` plutôt qu'un `Lock` ?
3. Comment fonctionne `Condition.wait()` et `Condition.notify()` ?
4. À quoi sert une `Barrier` ?
5. Pourquoi utiliser `with condition:` plutôt que `condition.acquire()` ?

---

*[Chapitre précédent : Chapitre 4 - Threading en Python - Les bases] | [Chapitre suivant : Chapitre 6 - Communication entre Threads]*
