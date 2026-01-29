# Plan du Cours : Programmation Parallèle et Distribuée en Python

## Vue d'ensemble
- **Durée totale** : 60 heures
- **Public cible** : Débutants avec bases superficielles de Python
- **Objectifs** : Comprendre et maîtriser les concepts de programmation parallèle et distribuée en Python

---

## Structure du cours

### Partie 1 : Introduction et Fondamentaux (8h)

#### Chapitre 1 : Introduction à la programmation parallèle et distribuée (2h)
- Concepts de base : séquentiel vs parallèle vs distribué
- Pourquoi la programmation parallèle ?
- Limitations de la programmation séquentielle
- Architecture des processeurs modernes (cœurs, threads)
- GIL (Global Interpreter Lock) en Python
- Exemple basique : comparaison séquentiel vs parallèle
- Exemple avancé : benchmark de performance
- Exercices

#### Chapitre 2 : Environnement de développement et outils (2h)
- Configuration de l'environnement Python
- Outils de profiling et de mesure de performance
- time, timeit, cProfile
- Visualisation des performances
- Exemple basique : mesurer le temps d'exécution
- Exemple avancé : profiler une application
- Exercices

#### Chapitre 3 : Concepts fondamentaux (4h)
- Concurrence vs Parallélisme
- Threads vs Processus
- Synchronisation et verrous
- Conditions de course (race conditions)
- Deadlocks et livelocks
- Partage de mémoire vs mémoire distribuée
- Exemple basique : comprendre les race conditions
- Exemple avancé : détecter et résoudre un deadlock
- Exercices

---

### Partie 2 : Programmation Parallèle avec Threads (12h)

#### Chapitre 4 : Threading en Python - Les bases (4h)
- Module `threading`
- Création de threads
- Thread principal vs threads secondaires
- Méthodes start(), join(), is_alive()
- Threads daemon
- Exemple basique : créer et lancer des threads simples
- Exemple avancé : gestion de plusieurs threads avec monitoring
- Exercices

#### Chapitre 5 : Synchronisation avec Threads (4h)
- Verrous (Locks) : Lock, RLock
- Sémaphores
- Événements (Events)
- Conditions (Conditions)
- Barrières (Barriers)
- Exemple basique : utiliser un Lock pour protéger une ressource partagée
- Exemple avancé : implémenter un producteur-consommateur avec Conditions
- Exercices

#### Chapitre 6 : Communication entre Threads (4h)
- Queue : Queue, LifoQueue, PriorityQueue
- Thread-safe collections
- Partage de données entre threads
- Variables locales aux threads (thread-local storage)
- Exemple basique : communication via Queue
- Exemple avancé : système de tâches avec file d'attente prioritaire
- Exercices

---

### Partie 3 : Programmation Parallèle avec Processus (14h)

#### Chapitre 7 : Multiprocessing - Les bases (4h)
- Module `multiprocessing`
- Pourquoi multiprocessing plutôt que threading ?
- Création de processus
- Process vs Pool
- Communication entre processus
- Exemple basique : créer et lancer des processus
- Exemple avancé : paralléliser un calcul intensif
- Exercices

#### Chapitre 8 : Pool de processus (4h)
- ProcessPoolExecutor
- Pool.map(), Pool.apply(), Pool.apply_async()
- Gestion des résultats
- Gestion des erreurs
- Exemple basique : utiliser Pool pour paralléliser une fonction
- Exemple avancé : traitement parallèle de fichiers avec gestion d'erreurs
- Exercices

#### Chapitre 9 : Communication inter-processus (6h)
- Pipes (Pipe)
- Files d'attente (Queue, JoinableQueue)
- Mémoire partagée (Value, Array, Manager)
- Synchronisation entre processus (Lock, Event, Condition)
- Exemple basique : communication via Pipe
- Exemple avancé : système distribué avec mémoire partagée et synchronisation
- Exercices

---

### Partie 4 : Programmation Asynchrone (10h)

#### Chapitre 10 : Introduction à l'asynchrone (3h)
- Concepts : async/await
- Pourquoi l'asynchrone ?
- Différence avec threading et multiprocessing
- Module `asyncio`
- Exemple basique : première fonction async
- Exemple avancé : comparaison async vs threading pour I/O
- Exercices

#### Chapitre 11 : asyncio - Les fondamentaux (4h)
- Coroutines et tasks
- Event loop
- await, async def
- asyncio.run(), asyncio.create_task()
- Exécution concurrente avec gather()
- Exemple basique : exécuter plusieurs coroutines
- Exemple avancé : scraper web asynchrone
- Exercices

#### Chapitre 12 : Synchronisation asynchrone (3h)
- Locks asynchrones (asyncio.Lock)
- Sémaphores asynchrones (asyncio.Semaphore)
- Events asynchrones (asyncio.Event)
- Queues asynchrones (asyncio.Queue)
- Exemple basique : protéger une ressource avec Lock
- Exemple avancé : rate limiting avec Semaphore
- Exercices

---

### Partie 5 : Patterns et Architectures (8h)

#### Chapitre 13 : Patterns de conception parallèle (4h)
- Pattern Producteur-Consommateur
- Pattern Map-Reduce
- Pattern Worker Pool
- Pattern Pipeline
- Pattern Master-Worker
- Exemple basique : implémenter un pattern Producteur-Consommateur
- Exemple avancé : système de traitement d'images avec Pipeline
- Exercices

#### Chapitre 14 : Gestion des erreurs et debugging (4h)
- Gestion d'exceptions dans les threads
- Gestion d'exceptions dans les processus
- Gestion d'exceptions asynchrones
- Outils de debugging
- Logging dans un contexte parallèle
- Exemple basique : capturer les exceptions dans un thread
- Exemple avancé : système de logging thread-safe
- Exercices

---

### Partie 6 : Programmation Distribuée (8h)

#### Chapitre 15 : Introduction à la programmation distribuée (2h)
- Concepts : systèmes distribués
- Communication réseau
- Protocoles : TCP/IP, HTTP
- Sockets en Python
- Exemple basique : client-serveur simple
- Exemple avancé : serveur multi-clients avec threading
- Exercices

#### Chapitre 16 : Communication distribuée (3h)
- Module `socket`
- Serveurs TCP/UDP
- Clients TCP/UDP
- Sérialisation : pickle, json, msgpack
- Exemple basique : échanger des données via socket
- Exemple avancé : système de messagerie distribué
- Exercices

#### Chapitre 17 : Frameworks de distribution (3h)
- Introduction à Celery
- Introduction à RPyC (Remote Python Call)
- Introduction à Pyro4
- Comparaison des approches
- Exemple basique : tâche distribuée avec Celery
- Exemple avancé : système de calcul distribué
- Exercices

---

## Projet final suggéré

Créer une application qui combine plusieurs concepts :
- Traitement parallèle de données
- Communication distribuée
- Interface utilisateur (optionnel avec Tkinter)
- Gestion d'erreurs robuste
- Documentation complète

---

## Ressources complémentaires

- Documentation officielle Python
- Livres de référence
- Outils de développement
- Communautés et forums
