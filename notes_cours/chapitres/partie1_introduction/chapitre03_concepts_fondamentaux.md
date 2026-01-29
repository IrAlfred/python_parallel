# Chapitre 3 : Concepts fondamentaux

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Distinguer la concurrence du parallélisme
- Comprendre la différence entre threads et processus
- Maîtriser les concepts de synchronisation et de verrous
- Identifier et résoudre les conditions de course (race conditions)
- Comprendre et éviter les deadlocks et livelocks
- Comprendre les différences entre mémoire partagée et mémoire distribuée

---

## 1. Explication du principe

### 1.1 Concurrence vs Parallélisme

**Concurrence (Concurrency) :**
La concurrence signifie que plusieurs tâches peuvent être en cours d'exécution en même temps, mais pas nécessairement simultanément. C'est comme un serveur de restaurant qui gère plusieurs tables : il passe d'une table à l'autre, donnant l'impression qu'il s'occupe de toutes en même temps, mais il ne peut être qu'à une seule table à la fois.

**Parallélisme (Parallelism) :**
Le parallélisme signifie que plusieurs tâches s'exécutent vraiment en même temps, sur plusieurs cœurs de processeur. C'est comme avoir plusieurs serveurs dans le restaurant, chacun s'occupant de tables différentes simultanément.

**Différences clés :**

| Aspect | Concurrence | Parallélisme |
|--------|-------------|--------------|
| **Exécution** | Apparente simultanéité | Vraie simultanéité |
| **Cœurs** | Peut fonctionner sur 1 cœur | Nécessite plusieurs cœurs |
| **Utilisation** | I/O, interface utilisateur | Calculs CPU intensifs |
| **Exemple Python** | `threading`, `asyncio` | `multiprocessing` |

**Points clés à retenir :**
- La **concurrence** gère plusieurs tâches en alternance (time-slicing)
- Le **parallélisme** exécute plusieurs tâches vraiment en même temps
- En Python, à cause du GIL, le threading est plutôt de la concurrence que du parallélisme
- Le multiprocessing permet le vrai parallélisme

### 1.2 Threads vs Processus

**Threads :**
Un thread (fil d'exécution) est une unité d'exécution plus légère qu'un processus. Plusieurs threads partagent la même mémoire et les mêmes ressources du processus parent.

**Caractéristiques des threads :**
- Partage de la mémoire (variables globales accessibles par tous)
- Création rapide (moins de ressources)
- Communication facile (mémoire partagée)
- Moins isolés (une erreur peut affecter les autres threads)

**Processus :**
Un processus est une instance d'un programme en cours d'exécution. Chaque processus a sa propre mémoire isolée.

**Caractéristiques des processus :**
- Mémoire isolée (pas de partage direct)
- Création plus lourde (plus de ressources)
- Communication plus complexe (pipes, queues, mémoire partagée explicite)
- Très isolés (une erreur n'affecte pas les autres processus)

**Comparaison :**

| Aspect | Threads | Processus |
|--------|---------|------------|
| **Mémoire** | Partagée | Isolée |
| **Création** | Rapide (~1ms) | Plus lente (~10-100ms) |
| **Communication** | Directe (mémoire) | Via IPC (Inter-Process Communication) |
| **Isolation** | Faible | Forte |
| **GIL** | Affecté | Non affecté (chaque processus a son GIL) |

**Quand utiliser quoi ?**
- **Threads** : Opérations I/O (fichiers, réseau), interface utilisateur
- **Processus** : Calculs CPU intensifs, quand on veut vraiment utiliser plusieurs cœurs

**Points clés à retenir :**
- Les threads sont plus légers mais partagent la mémoire
- Les processus sont plus lourds mais sont isolés
- En Python, pour le calcul CPU, utilisez des processus à cause du GIL

### 1.3 Synchronisation et verrous

**Pourquoi la synchronisation ?**
Quand plusieurs threads/processus accèdent à la même ressource (variable, fichier, etc.), il faut coordonner leurs accès pour éviter les conflits.

**Verrous (Locks) :**
Un verrou est un mécanisme qui permet à un seul thread/processus d'accéder à une ressource à la fois. C'est comme une clé de salle de bain : une seule personne peut l'utiliser à la fois.

**Comment fonctionne un verrou :**
1. Un thread demande le verrou (`acquire()`)
2. Si disponible, il l'obtient et accède à la ressource
3. Si occupé, il attend que le verrou soit libéré
4. Après utilisation, il libère le verrou (`release()`)

**Types de verrous :**
- **Lock simple** : Un thread à la fois
- **RLock (Reentrant Lock)** : Permet au même thread de verrouiller plusieurs fois
- **Semaphore** : Permet à N threads d'accéder simultanément

**Points clés à retenir :**
- Les verrous protègent les ressources partagées
- Un verrou mal utilisé peut causer des deadlocks
- Il faut toujours libérer un verrou après utilisation

### 1.4 Conditions de course (Race Conditions)

**Qu'est-ce qu'une race condition ?**
Une race condition se produit quand le résultat d'un programme dépend de l'ordre d'exécution des threads/processus, qui est non déterministe. C'est comme deux personnes qui essaient de modifier le même document en même temps sans coordination.

**Exemple classique :**
```python
# Variable partagée
compteur = 0

# Thread 1
compteur = compteur + 1  # Lit 0, calcule 1, écrit 1

# Thread 2 (en même temps)
compteur = compteur + 1  # Lit 0 (avant que Thread 1 n'écrive), calcule 1, écrit 1

# Résultat attendu : 2
# Résultat obtenu : 1 (ou parfois 2, selon le timing)
```

**Pourquoi c'est dangereux ?**
- Les résultats sont imprévisibles
- Les bugs sont difficiles à reproduire
- Les erreurs peuvent être subtiles et passer inaperçues

**Comment éviter les race conditions ?**
- Utiliser des verrous pour protéger les accès
- Utiliser des structures thread-safe (Queue, etc.)
- Éviter le partage d'état quand possible
- Utiliser des opérations atomiques

**Points clés à retenir :**
- Les race conditions sont causées par des accès non synchronisés
- Elles sont difficiles à détecter et à déboguer
- Toujours protéger les accès aux ressources partagées

### 1.5 Deadlocks et livelocks

**Deadlock (Interblocage) :**
Un deadlock se produit quand deux ou plusieurs threads/processus s'attendent mutuellement, créant une situation où aucun ne peut progresser. C'est comme deux personnes qui se tiennent la main et attendent que l'autre lâche en premier.

**Exemple de deadlock :**
```python
# Thread 1
verrou1.acquire()  # Obtient verrou1
verrou2.acquire()  # Attend verrou2 (détenu par Thread 2)

# Thread 2
verrou2.acquire()  # Obtient verrou2
verrou1.acquire()  # Attend verrou1 (détenu par Thread 1)

# Résultat : Les deux threads sont bloqués indéfiniment
```

**Conditions nécessaires pour un deadlock (Conditions de Coffman) :**
1. **Exclusion mutuelle** : Une ressource ne peut être utilisée que par un processus à la fois
2. **Rétention et attente** : Un processus détient une ressource et attend une autre
3. **Pas de préemption** : Les ressources ne peuvent pas être retirées de force
4. **Attente circulaire** : Il existe un cycle de processus qui s'attendent mutuellement

**Livelock :**
Un livelock est similaire à un deadlock, mais les processus continuent d'essayer de progresser sans succès. C'est comme deux personnes qui se croisent dans un couloir et continuent de bouger sans jamais se débloquer.

**Comment éviter les deadlocks :**
1. **Ordre constant des verrous** : Toujours acquérir les verrous dans le même ordre
2. **Timeout sur les verrous** : Ne pas attendre indéfiniment
3. **Détection de deadlock** : Surveiller et détecter les cycles
4. **Éviter les verrous multiples** : Utiliser un seul verrou quand possible

**Points clés à retenir :**
- Les deadlocks bloquent complètement l'exécution
- Les livelocks font tourner les processus sans progresser
- Prévenir est mieux que guérir : concevez votre code pour éviter ces situations

### 1.6 Partage de mémoire vs mémoire distribuée

**Mémoire partagée (Shared Memory) :**
Dans un système à mémoire partagée, tous les threads/processus accèdent à la même mémoire physique. C'est comme plusieurs personnes qui travaillent sur le même tableau blanc.

**Avantages :**
- Communication rapide (pas de copie de données)
- Accès direct aux données
- Simple à utiliser

**Inconvénients :**
- Risque de race conditions
- Besoin de synchronisation
- Difficile à scaler sur plusieurs machines

**Mémoire distribuée (Distributed Memory) :**
Dans un système à mémoire distribuée, chaque processus a sa propre mémoire. La communication se fait via messages. C'est comme plusieurs personnes qui travaillent sur des tableaux séparés et s'envoient des messages.

**Avantages :**
- Pas de race conditions (mémoire isolée)
- Scalable sur plusieurs machines
- Plus robuste (une erreur n'affecte pas les autres)

**Inconvénients :**
- Communication plus lente (sérialisation, réseau)
- Plus complexe à programmer
- Overhead de communication

**Points clés à retenir :**
- **Threads** : Mémoire partagée (rapide mais nécessite synchronisation)
- **Processus** : Mémoire isolée (sécurisé mais communication nécessaire)
- **Distribué** : Mémoire séparée sur différentes machines (scalable mais complexe)

---

## 2. Exemples basiques

### 2.1 Exemple basique 1 : Race condition sur un compteur

#### 2.1.1 Description

Nous allons créer un exemple qui illustre une race condition classique : l'incrémentation d'un compteur partagé par plusieurs threads. Cet exemple montrera le problème et comment le résoudre avec un verrou.

**Ce que nous allons faire :**
- Créer un compteur partagé
- Lancer plusieurs threads qui l'incrémentent
- Observer le problème de race condition
- Résoudre le problème avec un verrou

#### 2.1.2 Code

```python
import threading
import time

# Compteur partagé (sans protection)
compteur_sans_verrou = 0

# Compteur partagé (avec protection)
compteur_avec_verrou = 0
verrou = threading.Lock()

def incrementer_sans_verrou(nb_iterations):
    """
    Incrémente le compteur sans protection (race condition).
    
    Args:
        nb_iterations (int): Nombre de fois à incrémenter
    """
    global compteur_sans_verrou
    
    for _ in range(nb_iterations):
        # Opération non atomique : lecture, calcul, écriture
        valeur_actuelle = compteur_sans_verrou
        time.sleep(0.0001)  # Simule un petit délai
        compteur_sans_verrou = valeur_actuelle + 1

def incrementer_avec_verrou(nb_iterations):
    """
    Incrémente le compteur avec protection (pas de race condition).
    
    Args:
        nb_iterations (int): Nombre de fois à incrémenter
    """
    global compteur_avec_verrou
    
    for _ in range(nb_iterations):
        # Protéger l'accès avec un verrou
        verrou.acquire()
        try:
            valeur_actuelle = compteur_avec_verrou
            time.sleep(0.0001)  # Simule un petit délai
            compteur_avec_verrou = valeur_actuelle + 1
        finally:
            verrou.release()  # Toujours libérer le verrou

def test_race_condition():
    """Test qui montre la race condition."""
    global compteur_sans_verrou
    
    compteur_sans_verrou = 0
    nb_threads = 5
    nb_iterations_par_thread = 100
    
    print("=== Test sans verrou (Race Condition) ===\n")
    print(f"Lancement de {nb_threads} threads, chacun incrémente {nb_iterations_par_thread} fois")
    print(f"Valeur attendue : {nb_threads * nb_iterations_par_thread}\n")
    
    threads = []
    for i in range(nb_threads):
        t = threading.Thread(target=incrementer_sans_verrou, args=(nb_iterations_par_thread,))
        threads.append(t)
        t.start()
    
    # Attendre que tous les threads se terminent
    for t in threads:
        t.join()
    
    print(f"Valeur obtenue : {compteur_sans_verrou}")
    print(f"Différence : {nb_threads * nb_iterations_par_thread - compteur_sans_verrou}")
    
    if compteur_sans_verrou != nb_threads * nb_iterations_par_thread:
        print("⚠️  RACE CONDITION DÉTECTÉE ! La valeur est incorrecte.\n")
    else:
        print("✓ Valeur correcte (par chance, mais ce n'est pas garanti)\n")

def test_avec_verrou():
    """Test avec verrou (pas de race condition)."""
    global compteur_avec_verrou
    
    compteur_avec_verrou = 0
    nb_threads = 5
    nb_iterations_par_thread = 100
    
    print("=== Test avec verrou (Protection) ===\n")
    print(f"Lancement de {nb_threads} threads, chacun incrémente {nb_iterations_par_thread} fois")
    print(f"Valeur attendue : {nb_threads * nb_iterations_par_thread}\n")
    
    threads = []
    for i in range(nb_threads):
        t = threading.Thread(target=incrementer_avec_verrou, args=(nb_iterations_par_thread,))
        threads.append(t)
        t.start()
    
    # Attendre que tous les threads se terminent
    for t in threads:
        t.join()
    
    print(f"Valeur obtenue : {compteur_avec_verrou}")
    print(f"Différence : {nb_threads * nb_iterations_par_thread - compteur_avec_verrou}")
    
    if compteur_avec_verrou == nb_threads * nb_iterations_par_thread:
        print("✓ Valeur correcte ! Le verrou protège contre les race conditions.\n")
    else:
        print("⚠️  Erreur inattendue\n")

if __name__ == "__main__":
    # Test 1 : Sans protection (race condition)
    test_race_condition()
    
    # Test 2 : Avec protection (verrou)
    test_avec_verrou()
    
    print("=== Conclusion ===")
    print("Le verrou garantit que les opérations sur le compteur")
    print("sont atomiques et évitent les race conditions.")
```

#### 2.1.3 Explication ligne par ligne

**Lignes 1-2 : Importations**
- `threading` : Pour créer des threads et des verrous
- `time` : Pour simuler des délais

**Lignes 4-9 : Variables globales**
- `compteur_sans_verrou` : Compteur non protégé (va avoir des race conditions)
- `compteur_avec_verrou` : Compteur protégé
- `verrou` : Verrou pour protéger le compteur

**Lignes 11-22 : Fonction `incrementer_sans_verrou`**
- Lit la valeur actuelle
- Attend un peu (simule un calcul)
- Écrit la nouvelle valeur
- **Problème** : Entre la lecture et l'écriture, un autre thread peut modifier la valeur

**Lignes 24-38 : Fonction `incrementer_avec_verrou`**
- Acquiert le verrou avant d'accéder au compteur
- Effectue l'incrémentation
- Libère le verrou dans un bloc `finally` (garantit la libération même en cas d'erreur)
- **Solution** : Le verrou garantit qu'un seul thread modifie le compteur à la fois

**Lignes 40-68 : Fonction `test_race_condition`**
- Crée plusieurs threads qui incrémentent le compteur sans protection
- Montre que le résultat est incorrect

**Lignes 70-96 : Fonction `test_avec_verrou`**
- Même test mais avec protection
- Montre que le résultat est correct

#### 2.1.4 Résultat attendu

```
=== Test sans verrou (Race Condition) ===

Lancement de 5 threads, chacun incrémente 100 fois
Valeur attendue : 500

Valeur obtenue : 487
Différence : 13
⚠️  RACE CONDITION DÉTECTÉE ! La valeur est incorrecte.

=== Test avec verrou (Protection) ===

Lancement de 5 threads, chacun incrémente 100 fois
Valeur attendue : 500

Valeur obtenue : 500
Différence : 0
✓ Valeur correcte ! Le verrou protège contre les race conditions.

=== Conclusion ===
Le verrou garantit que les opérations sur le compteur
sont atomiques et évitent les race conditions.
```

*Note : La valeur exacte sans verrou variera à chaque exécution à cause de la race condition.*

#### 2.1.5 Analyse du résultat

Le résultat montre clairement :
- **Sans verrou** : La valeur est incorrecte (race condition)
- **Avec verrou** : La valeur est toujours correcte (protection)

Cela illustre l'importance de la synchronisation pour protéger les ressources partagées.

---

### 2.2 Exemple basique 2 : Partage de liste sans protection

#### 2.2.1 Description

Cet exemple montre une race condition sur une liste partagée. Plusieurs threads ajoutent des éléments à une liste sans synchronisation.

#### 2.2.2 Code

```python
import threading

liste_sans_verrou = []
liste_avec_verrou = []
verrou = threading.Lock()

def ajouter_sans_verrou(nb_elements):
    """Ajoute des éléments sans protection."""
    global liste_sans_verrou
    for i in range(nb_elements):
        liste_sans_verrou.append(i)

def ajouter_avec_verrou(nb_elements):
    """Ajoute des éléments avec protection."""
    global liste_avec_verrou
    for i in range(nb_elements):
        with verrou:
            liste_avec_verrou.append(i)

if __name__ == "__main__":
    threads = []
    
    # Test sans verrou
    for _ in range(3):
        t = threading.Thread(target=ajouter_sans_verrou, args=(100,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Sans verrou: {len(liste_sans_verrou)} éléments (attendu: 300)")
    
    # Test avec verrou
    threads = []
    for _ in range(3):
        t = threading.Thread(target=ajouter_avec_verrou, args=(100,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Avec verrou: {len(liste_avec_verrou)} éléments (attendu: 300)")
```

#### 2.2.3 Explication

Même si `list.append()` semble atomique, dans un contexte multi-thread, il peut y avoir des problèmes. Le verrou garantit que l'opération est vraiment atomique.

---

### 2.3 Exemple basique 3 : Comprendre la concurrence vs parallélisme

#### 2.3.1 Description

Cet exemple illustre la différence entre concurrence (threading) et parallélisme (multiprocessing) en Python.

#### 2.3.2 Code

```python
import threading
import multiprocessing
import time

def calcul_cpu(n):
    """Calcul CPU intensif."""
    resultat = 0
    for i in range(n):
        resultat += i * i
    return resultat

def test_threading():
    """Test avec threading (concurrence)."""
    debut = time.time()
    threads = []
    for _ in range(4):
        t = threading.Thread(target=calcul_cpu, args=(1000000,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    return time.time() - debut

def test_multiprocessing():
    """Test avec multiprocessing (parallélisme)."""
    debut = time.time()
    processus = []
    for _ in range(4):
        p = multiprocessing.Process(target=calcul_cpu, args=(1000000,))
        processus.append(p)
        p.start()
    
    for p in processus:
        p.join()
    return time.time() - debut

if __name__ == "__main__":
    print("Threading (concurrence):")
    temps_thread = test_threading()
    print(f"  Temps: {temps_thread:.4f}s\n")
    
    print("Multiprocessing (parallélisme):")
    temps_proc = test_multiprocessing()
    print(f"  Temps: {temps_proc:.4f}s\n")
    
    print(f"Multiprocessing est {temps_thread/temps_proc:.2f}x plus rapide")
```

#### 2.3.3 Explication

Pour le calcul CPU, multiprocessing est plus efficace car il utilise vraiment plusieurs cœurs, contrairement à threading qui est limité par le GIL.

---

## 3. Exemple avancé

### 3.1 Description

Nous allons créer un exemple qui illustre un deadlock classique : deux threads qui ont besoin de deux verrous différents mais les acquièrent dans un ordre différent. Nous montrerons comment détecter et résoudre ce problème.

**Contexte :**
Imaginez un système bancaire où deux comptes doivent transférer de l'argent l'un à l'autre. Chaque compte a un verrou. Si les deux transferts se font en même temps et acquièrent les verrous dans un ordre différent, on obtient un deadlock.

**Objectifs :**
- Créer un scénario de deadlock
- Détecter le deadlock
- Résoudre le problème avec un ordre constant des verrous
- Utiliser un timeout pour éviter les blocages infinis

### 3.2 Code

```python
import threading
import time
import random

# Verrous pour deux comptes bancaires
verrou_compte_a = threading.Lock()
verrou_compte_b = threading.Lock()

# Comptes bancaires
compte_a = 1000
compte_b = 1000

def transfert_vers_b(montant, avec_deadlock=True):
    """
    Transfère de l'argent du compte A vers le compte B.
    
    Args:
        montant (float): Montant à transférer
        avec_deadlock (bool): Si True, crée un deadlock potentiel
    """
    global compte_a, compte_b
    
    if avec_deadlock:
        # MAUVAISE APPROCHE : Ordre différent selon le thread
        print(f"Thread {threading.current_thread().name}: Acquiert verrou A")
        verrou_compte_a.acquire()
        time.sleep(0.1)  # Simule un délai (augmente la chance de deadlock)
        
        print(f"Thread {threading.current_thread().name}: Acquiert verrou B")
        verrou_compte_b.acquire()
    else:
        # BONNE APPROCHE : Ordre constant (toujours A puis B)
        print(f"Thread {threading.current_thread().name}: Acquiert verrou A")
        verrou_compte_a.acquire()
        time.sleep(0.1)
        
        print(f"Thread {threading.current_thread().name}: Acquiert verrou B")
        verrou_compte_b.acquire()
    
    try:
        # Effectuer le transfert
        if compte_a >= montant:
            compte_a -= montant
            compte_b += montant
            print(f"Thread {threading.current_thread().name}: Transfert de {montant} de A vers B")
        else:
            print(f"Thread {threading.current_thread().name}: Fonds insuffisants")
    finally:
        # Libérer dans l'ordre inverse
        verrou_compte_b.release()
        verrou_compte_a.release()
        print(f"Thread {threading.current_thread().name}: Verrous libérés")

def transfert_vers_a(montant, avec_deadlock=True):
    """
    Transfère de l'argent du compte B vers le compte A.
    
    Args:
        montant (float): Montant à transférer
        avec_deadlock (bool): Si True, crée un deadlock potentiel
    """
    global compte_a, compte_b
    
    if avec_deadlock:
        # MAUVAISE APPROCHE : Ordre différent (B puis A)
        print(f"Thread {threading.current_thread().name}: Acquiert verrou B")
        verrou_compte_b.acquire()
        time.sleep(0.1)  # Simule un délai
        
        print(f"Thread {threading.current_thread().name}: Acquiert verrou A")
        verrou_compte_a.acquire()
    else:
        # BONNE APPROCHE : Ordre constant (toujours A puis B)
        print(f"Thread {threading.current_thread().name}: Acquiert verrou A")
        verrou_compte_a.acquire()
        time.sleep(0.1)
        
        print(f"Thread {threading.current_thread().name}: Acquiert verrou B")
        verrou_compte_b.acquire()
    
    try:
        # Effectuer le transfert
        if compte_b >= montant:
            compte_b -= montant
            compte_a += montant
            print(f"Thread {threading.current_thread().name}: Transfert de {montant} de B vers A")
        else:
            print(f"Thread {threading.current_thread().name}: Fonds insuffisants")
    finally:
        # Libérer dans l'ordre inverse
        verrou_compte_b.release()
        verrou_compte_a.release()
        print(f"Thread {threading.current_thread().name}: Verrous libérés")

def test_deadlock():
    """Test qui peut créer un deadlock."""
    global compte_a, compte_b
    
    compte_a = 1000
    compte_b = 1000
    
    print("=== Test avec Deadlock Potentiel ===\n")
    print("Situation :")
    print("- Thread 1 : A -> B (acquiert A puis B)")
    print("- Thread 2 : B -> A (acquiert B puis A)")
    print("Risque : Deadlock si les deux threads s'exécutent en même temps\n")
    
    thread1 = threading.Thread(target=transfert_vers_b, args=(100, True), name="Thread-1")
    thread2 = threading.Thread(target=transfert_vers_a, args=(50, True), name="Thread-2")
    
    thread1.start()
    thread2.start()
    
    # Attendre avec timeout pour détecter le deadlock
    thread1.join(timeout=2)
    thread2.join(timeout=2)
    
    if thread1.is_alive() or thread2.is_alive():
        print("\n⚠️  DEADLOCK DÉTECTÉ ! Les threads sont bloqués.")
        print("Solution : Utiliser un ordre constant pour les verrous.\n")
    else:
        print("\n✓ Transferts terminés (par chance, pas de deadlock cette fois)\n")
    
    print(f"État final - Compte A: {compte_a}, Compte B: {compte_b}")

def test_sans_deadlock():
    """Test sans deadlock (ordre constant des verrous)."""
    global compte_a, compte_b
    
    compte_a = 1000
    compte_b = 1000
    
    print("=== Test sans Deadlock (Ordre Constant) ===\n")
    print("Solution : Toujours acquérir les verrous dans le même ordre (A puis B)\n")
    
    thread1 = threading.Thread(target=transfert_vers_b, args=(100, False), name="Thread-1")
    thread2 = threading.Thread(target=transfert_vers_a, args=(50, False), name="Thread-2")
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    print("\n✓ Transferts terminés sans deadlock\n")
    print(f"État final - Compte A: {compte_a}, Compte B: {compte_b}")

def transfert_avec_timeout(montant, timeout=1):
    """
    Version avec timeout pour éviter les blocages infinis.
    
    Args:
        montant (float): Montant à transférer
        timeout (float): Timeout en secondes
    """
    global compte_a, compte_b
    
    # Essayer d'acquérir les verrous avec timeout
    if not verrou_compte_a.acquire(timeout=timeout):
        print(f"Thread {threading.current_thread().name}: Timeout sur verrou A")
        return False
    
    try:
        if not verrou_compte_b.acquire(timeout=timeout):
            print(f"Thread {threading.current_thread().name}: Timeout sur verrou B")
            return False
        
        try:
            # Effectuer le transfert
            if compte_a >= montant:
                compte_a -= montant
                compte_b += montant
                print(f"Thread {threading.current_thread().name}: Transfert réussi")
                return True
            else:
                print(f"Thread {threading.current_thread().name}: Fonds insuffisants")
                return False
        finally:
            verrou_compte_b.release()
    finally:
        verrou_compte_a.release()
    
    return False

if __name__ == "__main__":
    # Test 1 : Avec deadlock potentiel
    test_deadlock()
    
    print("\n" + "="*50 + "\n")
    
    # Test 2 : Sans deadlock (solution)
    test_sans_deadlock()
    
    print("\n" + "="*50 + "\n")
    
    # Test 3 : Avec timeout
    print("=== Test avec Timeout ===\n")
    compte_a = 1000
    compte_b = 1000
    
    thread1 = threading.Thread(target=transfert_avec_timeout, args=(100, 0.5), name="Thread-1")
    thread2 = threading.Thread(target=transfert_avec_timeout, args=(50, 0.5), name="Thread-2")
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    print(f"\nÉtat final - Compte A: {compte_a}, Compte B: {compte_b}")
```

### 3.3 Explication détaillée

**Architecture :**
L'exemple simule un système bancaire avec deux comptes. Les transferts nécessitent d'acquérir les verrous des deux comptes, créant un risque de deadlock.

**Fonctionnalités :**

1. **Transferts avec deadlock potentiel** :
   - Thread 1 acquiert A puis B
   - Thread 2 acquiert B puis A
   - Si les deux s'exécutent en même temps → deadlock

2. **Transferts sans deadlock** :
   - Toujours acquérir A puis B (ordre constant)
   - Même si les transferts vont dans des directions différentes

3. **Transferts avec timeout** :
   - Utilise `acquire(timeout=...)` pour éviter les blocages infinis
   - Retourne False si le timeout est atteint

**Points techniques importants :**

- **Ordre constant des verrous** : Toujours acquérir les verrous dans le même ordre (par exemple, toujours par ordre alphabétique ou par ID)
- **Timeout** : Utiliser `acquire(timeout=...)` pour éviter les blocages infinis
- **Bloc try/finally** : Garantit que les verrous sont toujours libérés

### 3.4 Résultat attendu

```
=== Test avec Deadlock Potentiel ===

Situation :
- Thread 1 : A -> B (acquiert A puis B)
- Thread 2 : B -> A (acquiert B puis A)
Risque : Deadlock si les deux threads s'exécutent en même temps

Thread Thread-1: Acquiert verrou A
Thread Thread-2: Acquiert verrou B
Thread Thread-1: Acquiert verrou B
Thread Thread-2: Acquiert verrou A

⚠️  DEADLOCK DÉTECTÉ ! Les threads sont bloqués.
Solution : Utiliser un ordre constant pour les verrous.

État final - Compte A: 1000, Compte B: 1000

==================================================

=== Test sans Deadlock (Ordre Constant) ===

Solution : Toujours acquérir les verrous dans le même ordre (A puis B)

Thread Thread-1: Acquiert verrou A
Thread Thread-2: Acquiert verrou A
Thread Thread-1: Acquiert verrou B
Thread Thread-1: Transfert de 100 de A vers B
Thread Thread-1: Verrous libérés
Thread Thread-2: Acquiert verrou B
Thread Thread-2: Transfert de 50 de B vers A
Thread Thread-2: Verrous libérés

✓ Transferts terminés sans deadlock

État final - Compte A: 950, Compte B: 1050
```

### 3.5 Analyse et améliorations possibles

**Analyse :**
- Le premier test montre le deadlock (threads bloqués)
- Le deuxième test montre la solution (ordre constant)
- Le timeout permet de détecter et gérer les deadlocks

**Améliorations possibles :**
- Utiliser un contexte manager (`with verrou:`) pour une gestion automatique
- Implémenter un détecteur de deadlock automatique
- Utiliser des transactions pour garantir la cohérence

---

## 4. Exercices

### Exercice 1 : Détecter une race condition

**Difficulté** : ⭐ Facile  
**Temps estimé** : 20-25 minutes  
**Objectif** : Identifier et corriger une race condition

**Énoncé :**
Créez un programme qui :
1. A une liste partagée `ma_liste = []`
2. Lance 3 threads qui ajoutent chacun 100 éléments à la liste
3. Affiche la longueur finale de la liste
4. Identifie pourquoi la longueur n'est pas 300
5. Corrige le problème avec un verrou

**Consignes :**
- Utilisez `threading.Thread` et `threading.Lock`
- Affichez clairement la différence entre avec et sans verrou

**Solution :**

```python
import threading

ma_liste = []
verrou = threading.Lock()

def ajouter_sans_verrou(nb_elements):
    """Ajoute des éléments sans protection."""
    global ma_liste
    for i in range(nb_elements):
        ma_liste.append(i)

def ajouter_avec_verrou(nb_elements):
    """Ajoute des éléments avec protection."""
    global ma_liste
    for i in range(nb_elements):
        verrou.acquire()
        try:
            ma_liste.append(i)
        finally:
            verrou.release()

# Test sans verrou
ma_liste = []
threads = []
for _ in range(3):
    t = threading.Thread(target=ajouter_sans_verrou, args=(100,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Sans verrou : {len(ma_liste)} éléments (attendu: 300)")

# Test avec verrou
ma_liste = []
threads = []
for _ in range(3):
    t = threading.Thread(target=ajouter_avec_verrou, args=(100,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Avec verrou : {len(ma_liste)} éléments (attendu: 300)")
```

**Explication de la solution :**
Même si `list.append()` semble atomique, dans un contexte multi-thread, il peut y avoir des problèmes. Le verrou garantit que l'opération est vraiment atomique.

---

### Exercice 2 : Éviter un deadlock

**Difficulté** : ⭐⭐ Moyen  
**Temps estimé** : 30-40 minutes  
**Objectif** : Implémenter une solution qui évite les deadlocks

**Énoncé :**
Créez un programme qui :
1. A 3 ressources avec 3 verrous (R1, R2, R3)
2. Crée 3 threads qui ont besoin de 2 ressources chacun :
   - Thread 1 : R1 et R2
   - Thread 2 : R2 et R3
   - Thread 3 : R3 et R1
3. Implémentez une fonction qui acquiert les verrous dans un ordre constant pour éviter les deadlocks
4. Testez avec et sans l'ordre constant

**Consignes :**
- Utilisez un ordre basé sur l'ID de la ressource
- Affichez l'ordre d'acquisition des verrous
- Utilisez un timeout pour détecter les deadlocks

**Solution :**

```python
import threading
import time

verrou_r1 = threading.Lock()
verrou_r2 = threading.Lock()
verrou_r3 = threading.Lock()

verrous = {
    'R1': verrou_r1,
    'R2': verrou_r2,
    'R3': verrou_r3
}

def utiliser_ressources(ressources, nom_thread, avec_ordre=True):
    """
    Utilise des ressources avec ou sans ordre constant.
    
    Args:
        ressources (list): Liste des noms de ressources
        nom_thread (str): Nom du thread
        avec_ordre (bool): Si True, trie les ressources par ordre
    """
    if avec_ordre:
        # SOLUTION : Trier les ressources pour avoir un ordre constant
        ressources = sorted(ressources)
        print(f"{nom_thread}: Ordre trié des ressources: {ressources}")
    
    verrous_acquises = []
    try:
        for ressource in ressources:
            verrou = verrous[ressource]
            print(f"{nom_thread}: Tentative d'acquisition de {ressource}")
            if verrou.acquire(timeout=2):
                verrous_acquises.append((ressource, verrou))
                print(f"{nom_thread}: {ressource} acquise")
                time.sleep(0.1)  # Simule un travail
            else:
                print(f"{nom_thread}: Timeout sur {ressource}")
                # Libérer les verrous déjà acquises
                for r, v in reversed(verrous_acquises):
                    v.release()
                    print(f"{nom_thread}: {r} libérée")
                return False
        
        # Utiliser les ressources
        print(f"{nom_thread}: Utilisation des ressources {ressources}")
        time.sleep(0.5)
        print(f"{nom_thread}: Travail terminé")
        return True
    finally:
        # Libérer dans l'ordre inverse
        for ressource, verrou in reversed(verrous_acquises):
            verrou.release()
            print(f"{nom_thread}: {ressource} libérée")

# Test avec ordre constant
print("=== Test avec ordre constant (pas de deadlock) ===\n")
thread1 = threading.Thread(target=utiliser_ressources, 
                           args=(['R1', 'R2'], 'Thread-1', True))
thread2 = threading.Thread(target=utiliser_ressources, 
                           args=(['R2', 'R3'], 'Thread-2', True))
thread3 = threading.Thread(target=utiliser_ressources, 
                           args=(['R3', 'R1'], 'Thread-3', True))

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()

print("\n✓ Tous les threads ont terminé")
```

**Explication de la solution :**
En triant les ressources par nom, on garantit un ordre constant d'acquisition, évitant ainsi les deadlocks circulaires.

---

### Exercice 3 : Système de cache thread-safe

**Difficulté** : ⭐⭐⭐ Avancé  
**Temps estimé** : 45-60 minutes  
**Objectif** : Créer un système de cache thread-safe avec gestion des race conditions

**Énoncé :**
Créez une classe `CacheThreadSafe` qui :
1. Stocke des paires clé-valeur
2. Permet d'ajouter, récupérer et supprimer des éléments
3. Est thread-safe (plusieurs threads peuvent l'utiliser simultanément)
4. Utilise un verrou pour protéger les accès
5. Teste avec plusieurs threads qui ajoutent/récupèrent des éléments

**Consignes :**
- Utilisez un dictionnaire pour stocker les données
- Protégez toutes les opérations avec un verrou
- Testez avec des threads qui font des opérations concurrentes

**Solution :**

```python
import threading
import time
import random

class CacheThreadSafe:
    """Cache thread-safe pour stocker des paires clé-valeur."""
    
    def __init__(self):
        self._donnees = {}
        self._verrou = threading.RLock()  # RLock pour permettre les appels imbriqués
        self._stats = {
            'lectures': 0,
            'ecritures': 0,
            'suppressions': 0
        }
    
    def ajouter(self, cle, valeur):
        """Ajoute ou met à jour une entrée."""
        with self._verrou:
            self._donnees[cle] = valeur
            self._stats['ecritures'] += 1
            return True
    
    def recuperer(self, cle, valeur_par_defaut=None):
        """Récupère une valeur ou retourne la valeur par défaut."""
        with self._verrou:
            self._stats['lectures'] += 1
            return self._donnees.get(cle, valeur_par_defaut)
    
    def supprimer(self, cle):
        """Supprime une entrée."""
        with self._verrou:
            if cle in self._donnees:
                del self._donnees[cle]
                self._stats['suppressions'] += 1
                return True
            return False
    
    def taille(self):
        """Retourne le nombre d'éléments."""
        with self._verrou:
            return len(self._donnees)
    
    def obtenir_stats(self):
        """Retourne les statistiques d'utilisation."""
        with self._verrou:
            return self._stats.copy()
    
    def vider(self):
        """Vide le cache."""
        with self._verrou:
            self._donnees.clear()

def worker_ecriture(cache, nb_operations, nom):
    """Worker qui écrit dans le cache."""
    for i in range(nb_operations):
        cle = f"cle_{nom}_{i}"
        valeur = f"valeur_{nom}_{i}"
        cache.ajouter(cle, valeur)
        time.sleep(random.uniform(0.001, 0.01))

def worker_lecture(cache, nb_operations, nom):
    """Worker qui lit dans le cache."""
    for i in range(nb_operations):
        cle = f"cle_thread_{i % 5}"  # Lit des clés qui peuvent exister ou non
        cache.recuperer(cle)
        time.sleep(random.uniform(0.001, 0.01))

if __name__ == "__main__":
    cache = CacheThreadSafe()
    
    # Créer des threads qui écrivent
    threads_ecriture = []
    for i in range(3):
        t = threading.Thread(target=worker_ecriture, args=(cache, 10, i))
        threads_ecriture.append(t)
        t.start()
    
    # Créer des threads qui lisent
    threads_lecture = []
    for i in range(2):
        t = threading.Thread(target=worker_lecture, args=(cache, 15, i))
        threads_lecture.append(t)
        t.start()
    
    # Attendre que tous se terminent
    for t in threads_ecriture + threads_lecture:
        t.join()
    
    print(f"Taille du cache : {cache.taille()}")
    print(f"Statistiques : {cache.obtenir_stats()}")
```

**Explication de la solution :**
Cette solution utilise un `RLock` (Reentrant Lock) qui permet au même thread d'acquérir le verrou plusieurs fois (utile si une méthode appelle une autre méthode de la même classe). Le contexte manager `with` garantit la libération automatique du verrou.

---

## 5. Résumé

### Concepts clés
- ✅ **Concurrence** : Gestion de plusieurs tâches en alternance (apparente simultanéité)
- ✅ **Parallélisme** : Exécution simultanée réelle sur plusieurs cœurs
- ✅ **Threads** : Légers, mémoire partagée, affectés par le GIL
- ✅ **Processus** : Isolés, mémoire séparée, vrai parallélisme en Python
- ✅ **Verrous** : Mécanisme de synchronisation pour protéger les ressources
- ✅ **Race condition** : Résultat dépendant de l'ordre d'exécution non déterministe
- ✅ **Deadlock** : Situation où des threads/processus s'attendent mutuellement

### Points importants à retenir
1. La concurrence et le parallélisme sont différents : la concurrence est pour l'I/O, le parallélisme pour le CPU
2. Les threads partagent la mémoire, les processus ont une mémoire isolée
3. Toujours protéger les ressources partagées avec des verrous
4. Utiliser un ordre constant pour acquérir les verrous (évite les deadlocks)
5. Les race conditions sont difficiles à détecter mais faciles à prévenir avec la synchronisation

### Pièges à éviter
- ⚠️ **Oublier de libérer un verrou** : Utilisez `with verrou:` ou `try/finally`
- ⚠️ **Acquérir des verrous dans un ordre différent** : Toujours le même ordre
- ⚠️ **Penser que les opérations simples sont atomiques** : Elles ne le sont pas toujours
- ⚠️ **Trop de verrous** : Peut réduire la parallélisation, utilisez-les seulement quand nécessaire

---

## 6. Pour aller plus loin

### Ressources supplémentaires
- 📚 "Operating System Concepts" - Chapitre sur la synchronisation
- 📚 "The Art of Multiprocessor Programming" - Concepts avancés
- 📚 Documentation Python threading : https://docs.python.org/3/library/threading.html

### Concepts liés à explorer
- **Lock-free programming** : Structures de données sans verrous
- **Atomic operations** : Opérations garanties atomiques par le processeur
- **Memory models** : Modèles de mémoire pour comprendre la cohérence

### Projets suggérés
- Implémenter un système de files d'attente thread-safe
- Créer une bibliothèque de structures de données thread-safe
- Développer un système de logging thread-safe

---

## 7. Questions de révision

1. Quelle est la différence fondamentale entre concurrence et parallélisme ?
2. Pourquoi les threads en Python ne permettent-ils pas le vrai parallélisme pour le calcul CPU ?
3. Qu'est-ce qu'une race condition et comment l'éviter ?
4. Quelles sont les 4 conditions nécessaires pour qu'un deadlock se produise ?
5. Pourquoi est-il important d'acquérir les verrous dans un ordre constant ?

---

*[Chapitre précédent : Chapitre 2 - Environnement] | [Chapitre suivant : Chapitre 4 - Threading en Python - Les bases]*
