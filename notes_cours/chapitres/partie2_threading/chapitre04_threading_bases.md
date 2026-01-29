# Chapitre 4 : Threading en Python - Les bases

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Comprendre le module `threading` de Python
- Créer et lancer des threads
- Utiliser les méthodes essentielles : `start()`, `join()`, `is_alive()`
- Comprendre la différence entre thread principal et threads secondaires
- Utiliser les threads daemon
- Gérer plusieurs threads simultanément

---

## 1. Explication du principe

### 1.1 Le module threading

**Qu'est-ce que threading ?**
Le module `threading` de Python fournit une interface de haut niveau pour créer et gérer des threads. C'est l'outil principal pour la programmation concurrente en Python.

**Pourquoi utiliser threading ?**
- **Opérations I/O** : Pendant qu'un thread attend une réponse réseau, un autre peut continuer à travailler
- **Interface utilisateur** : Garder l'interface réactive pendant qu'un calcul s'exécute
- **Tâches parallèles** : Traiter plusieurs fichiers, requêtes, etc. en même temps

**Limitations du threading en Python :**
À cause du GIL (Global Interpreter Lock), les threads Python ne peuvent pas vraiment exécuter du code Python en parallèle sur plusieurs cœurs. Cependant, ils sont excellents pour :
- Les opérations I/O (fichiers, réseau)
- Les tâches qui attendent beaucoup
- Maintenir une interface utilisateur réactive

**Points clés à retenir :**
- `threading` est idéal pour les opérations I/O
- Le GIL limite le parallélisme réel pour le calcul CPU
- Les threads sont légers et rapides à créer

### 1.2 Création de threads

**Deux façons de créer un thread :**

1. **Créer une classe qui hérite de `Thread`** :
```python
class MonThread(threading.Thread):
    def run(self):
        # Code à exécuter
        pass
```

2. **Passer une fonction au constructeur `Thread`** :
```python
def ma_fonction():
    # Code à exécuter
    pass

thread = threading.Thread(target=ma_fonction)
```

**Méthode recommandée :**
Pour la plupart des cas, passer une fonction est plus simple et plus Pythonique.

**Points clés à retenir :**
- Deux méthodes : classe héritée ou fonction cible
- La méthode avec fonction est généralement préférée
- Le thread ne commence pas automatiquement, il faut appeler `start()`

### 1.3 Méthodes essentielles

**`start()`** :
Démarre l'exécution du thread. Le thread commence à exécuter la fonction cible dans un nouveau fil d'exécution.

**`join(timeout=None)`** :
Attend que le thread se termine. Si `timeout` est spécifié, attend au maximum ce nombre de secondes.

**`is_alive()`** :
Retourne `True` si le thread est en cours d'exécution, `False` sinon.

**`name`** :
Nom du thread (utile pour le débogage).

**Points clés à retenir :**
- `start()` démarre le thread
- `join()` attend la fin du thread
- `is_alive()` vérifie si le thread est actif
- Toujours utiliser `join()` pour attendre la fin des threads

### 1.4 Thread principal vs threads secondaires

**Thread principal :**
Le thread principal est celui qui exécute le script Python initial. C'est le thread qui exécute le code dans `if __name__ == "__main__":`.

**Threads secondaires :**
Les threads créés explicitement avec `threading.Thread()` sont des threads secondaires.

**Pourquoi cette distinction est importante :**
- Le programme Python se termine quand le thread principal se termine
- Si des threads secondaires sont encore actifs, ils peuvent être interrompus brutalement
- Il faut attendre que les threads secondaires se terminent avec `join()`

**Points clés à retenir :**
- Le thread principal est celui du script initial
- Les threads secondaires doivent être attendus avec `join()`
- Le programme se termine quand le thread principal se termine

### 1.5 Threads daemon

**Qu'est-ce qu'un thread daemon ?**
Un thread daemon est un thread qui se termine automatiquement quand tous les threads non-daemon se terminent. C'est utile pour des tâches de fond qui peuvent être interrompues.

**Caractéristiques :**
- Se termine automatiquement quand le programme principal se termine
- Utile pour des tâches de surveillance, logging, etc.
- Ne doit pas être utilisé pour des tâches critiques (peut être interrompu)

**Comment créer un thread daemon :**
```python
thread = threading.Thread(target=ma_fonction, daemon=True)
# ou
thread.daemon = True
```

**Points clés à retenir :**
- Les threads daemon se terminent automatiquement
- Utiles pour des tâches de fond non critiques
- Ne pas utiliser pour des tâches importantes

---

## 2. Exemple basique

### 2.1 Description

Nous allons créer un exemple simple qui montre comment créer et lancer des threads. Cet exemple illustrera les concepts de base du threading.

**Ce que nous allons faire :**
- Créer une fonction simple qui fait un travail
- Créer plusieurs threads qui exécutent cette fonction
- Démarrer les threads et attendre qu'ils se terminent
- Afficher des informations sur les threads

### 2.2 Code

```python
import threading
import time

def travail_simple(nom_thread, duree):
    """
    Simule un travail qui prend du temps.
    
    Args:
        nom_thread (str): Nom du thread
        duree (float): Durée du travail en secondes
    """
    print(f"[{nom_thread}] Début du travail")
    
    for i in range(5):
        time.sleep(duree / 5)
        print(f"[{nom_thread}] Progression : {i+1}/5")
    
    print(f"[{nom_thread}] Travail terminé")

def exemple_basique():
    """Exemple basique de création et utilisation de threads."""
    
    print("=== Exemple basique de threading ===\n")
    
    # Créer des threads
    thread1 = threading.Thread(
        target=travail_simple,
        args=("Thread-1", 2.0),
        name="Thread-1"
    )
    
    thread2 = threading.Thread(
        target=travail_simple,
        args=("Thread-2", 1.5),
        name="Thread-2"
    )
    
    thread3 = threading.Thread(
        target=travail_simple,
        args=("Thread-3", 1.0),
        name="Thread-3"
    )
    
    # Afficher les informations des threads avant démarrage
    print("Threads créés :")
    print(f"  {thread1.name}: is_alive={thread1.is_alive()}")
    print(f"  {thread2.name}: is_alive={thread2.is_alive()}")
    print(f"  {thread3.name}: is_alive={thread3.is_alive()}\n")
    
    # Démarrer les threads
    print("Démarrage des threads...\n")
    thread1.start()
    thread2.start()
    thread3.start()
    
    # Vérifier qu'ils sont actifs
    print("Après start() :")
    print(f"  {thread1.name}: is_alive={thread1.is_alive()}")
    print(f"  {thread2.name}: is_alive={thread2.is_alive()}")
    print(f"  {thread3.name}: is_alive={thread3.is_alive()}\n")
    
    # Attendre que tous les threads se terminent
    print("Attente de la fin des threads...\n")
    thread1.join()
    thread2.join()
    thread3.join()
    
    # Vérifier qu'ils sont terminés
    print("\nAprès join() :")
    print(f"  {thread1.name}: is_alive={thread1.is_alive()}")
    print(f"  {thread2.name}: is_alive={thread2.is_alive()}")
    print(f"  {thread3.name}: is_alive={thread3.is_alive()}")
    
    print("\n✓ Tous les threads sont terminés")

if __name__ == "__main__":
    exemple_basique()
```

### 2.3 Explication ligne par ligne

**Lignes 1-2 : Importations**
- `threading` : Module pour créer et gérer des threads
- `time` : Pour `sleep()` afin de simuler un travail

**Lignes 4-18 : Fonction `travail_simple`**
- Fonction qui sera exécutée par chaque thread
- Prend un nom et une durée
- Simule un travail en se mettant en pause plusieurs fois
- Affiche la progression

**Lignes 20-70 : Fonction `exemple_basique`**
- **Lignes 25-40** : Crée 3 threads avec `threading.Thread()`
  - `target` : Fonction à exécuter
  - `args` : Arguments à passer à la fonction
  - `name` : Nom du thread (pour le débogage)
  
- **Lignes 42-46** : Affiche l'état des threads avant `start()`
  - `is_alive()` retourne `False` car les threads ne sont pas encore démarrés
  
- **Lignes 48-52** : Démarre les threads avec `start()`
  - Les threads commencent à s'exécuter en parallèle
  
- **Lignes 54-58** : Vérifie que les threads sont actifs
  - `is_alive()` retourne maintenant `True`
  
- **Lignes 60-64** : Attend la fin des threads avec `join()`
  - Le thread principal attend que chaque thread se termine
  
- **Lignes 66-70** : Vérifie que les threads sont terminés
  - `is_alive()` retourne `False`

### 2.4 Résultat attendu

```
=== Exemple basique de threading ===

Threads créés :
  Thread-1: is_alive=False
  Thread-2: is_alive=False
  Thread-3: is_alive=False

Démarrage des threads...

Après start() :
  Thread-1: is_alive=True
  Thread-2: is_alive=True
  Thread-3: is_alive=True

Attente de la fin des threads...

[Thread-1] Début du travail
[Thread-2] Début du travail
[Thread-3] Début du travail
[Thread-3] Progression : 1/5
[Thread-2] Progression : 1/5
[Thread-1] Progression : 1/5
[Thread-3] Progression : 2/5
[Thread-2] Progression : 2/5
[Thread-1] Progression : 2/5
[Thread-3] Progression : 3/5
[Thread-3] Progression : 4/5
[Thread-2] Progression : 3/5
[Thread-1] Progression : 3/5
[Thread-3] Travail terminé
[Thread-2] Progression : 4/5
[Thread-1] Progression : 4/5
[Thread-2] Travail terminé
[Thread-1] Progression : 5/5
[Thread-1] Travail terminé

Après join() :
  Thread-1: is_alive=False
  Thread-2: is_alive=False
  Thread-3: is_alive=False

✓ Tous les threads sont terminés
```

*Note : L'ordre d'affichage peut varier car les threads s'exécutent en parallèle.*

### 2.5 Analyse du résultat

Le résultat montre que :
- Les threads s'exécutent en parallèle (les messages se mélangent)
- `is_alive()` change de `False` à `True` après `start()`
- `join()` attend que chaque thread se termine
- Les threads se terminent dans un ordre non déterministe (selon leur durée)

---

## 3. Exemple avancé

### 3.1 Description

Nous allons créer un exemple plus réaliste : un système de téléchargement de fichiers qui utilise plusieurs threads pour télécharger plusieurs fichiers en parallèle. Cet exemple montre l'utilité pratique du threading pour les opérations I/O.

**Contexte :**
Imaginez que vous devez télécharger 10 fichiers depuis Internet. Au lieu de les télécharger un par un (séquentiel), nous allons les télécharger en parallèle avec plusieurs threads.

**Objectifs :**
- Simuler le téléchargement de plusieurs fichiers
- Utiliser des threads pour télécharger en parallèle
- Afficher la progression de chaque téléchargement
- Comparer les temps d'exécution séquentiel vs parallèle
- Gérer les threads avec monitoring

### 3.2 Code

```python
import threading
import time
import random
from datetime import datetime

class TelechargeurFichier:
    """Classe pour gérer le téléchargement de fichiers avec threads."""
    
    def __init__(self):
        self.verrou_affichage = threading.Lock()
        self.fichiers_termines = 0
        self.verrou_compteur = threading.Lock()
    
    def simuler_telechargement(self, nom_fichier, taille_mb):
        """
        Simule le téléchargement d'un fichier.
        
        Args:
            nom_fichier (str): Nom du fichier
            taille_mb (float): Taille du fichier en MB
        """
        thread_name = threading.current_thread().name
        
        # Simuler le temps de téléchargement (1 MB par seconde)
        temps_telechargement = taille_mb
        
        with self.verrou_affichage:
            print(f"[{thread_name}] Début du téléchargement de {nom_fichier} ({taille_mb} MB)")
        
        # Simuler la progression
        for pourcentage in range(0, 101, 25):
            time.sleep(temps_telechargement / 4)
            with self.verrou_affichage:
                print(f"[{thread_name}] {nom_fichier}: {pourcentage}%")
        
        with self.verrou_affichage:
            print(f"[{thread_name}] ✓ {nom_fichier} téléchargé avec succès")
        
        # Incrémenter le compteur de fichiers terminés
        with self.verrou_compteur:
            self.fichiers_termines += 1
    
    def telecharger_sequentiel(self, fichiers):
        """
        Télécharge les fichiers de manière séquentielle.
        
        Args:
            fichiers (list): Liste de tuples (nom, taille_mb)
        
        Returns:
            float: Temps d'exécution en secondes
        """
        debut = time.time()
        
        print("=== Téléchargement séquentiel ===\n")
        
        for nom, taille in fichiers:
            self.simuler_telechargement(nom, taille)
        
        fin = time.time()
        return fin - debut
    
    def telecharger_parallele(self, fichiers, nb_threads=3):
        """
        Télécharge les fichiers en parallèle avec des threads.
        
        Args:
            fichiers (list): Liste de tuples (nom, taille_mb)
            nb_threads (int): Nombre de threads à utiliser
        
        Returns:
            float: Temps d'exécution en secondes
        """
        self.fichiers_termines = 0
        debut = time.time()
        
        print(f"=== Téléchargement parallèle ({nb_threads} threads) ===\n")
        
        threads = []
        index = 0
        
        # Créer et démarrer les threads
        while index < len(fichiers):
            threads_actifs = [t for t in threads if t.is_alive()]
            
            # Si on a de la place, créer un nouveau thread
            if len(threads_actifs) < nb_threads and index < len(fichiers):
                nom, taille = fichiers[index]
                thread = threading.Thread(
                    target=self.simuler_telechargement,
                    args=(nom, taille),
                    name=f"Downloader-{len(threads)+1}"
                )
                threads.append(thread)
                thread.start()
                index += 1
            
            # Attendre un peu avant de vérifier à nouveau
            time.sleep(0.1)
        
        # Attendre que tous les threads se terminent
        for thread in threads:
            thread.join()
        
        fin = time.time()
        return fin - debut
    
    def afficher_statistiques(self, temps_seq, temps_par, fichiers):
        """Affiche les statistiques de performance."""
        total_mb = sum(taille for _, taille in fichiers)
        acceleration = temps_seq / temps_par if temps_par > 0 else 0
        
        print("\n" + "="*50)
        print("=== Statistiques ===")
        print(f"Nombre de fichiers : {len(fichiers)}")
        print(f"Taille totale : {total_mb:.1f} MB")
        print(f"Temps séquentiel : {temps_seq:.2f} secondes")
        print(f"Temps parallèle : {temps_par:.2f} secondes")
        print(f"Accélération : {acceleration:.2f}x")
        print(f"Gain de temps : {temps_seq - temps_par:.2f} secondes")
        print("="*50)

def exemple_avance():
    """Exemple avancé de gestion de threads."""
    
    # Liste de fichiers à télécharger
    fichiers = [
        ("document1.pdf", 5.0),
        ("image1.jpg", 2.5),
        ("video1.mp4", 10.0),
        ("archive.zip", 3.0),
        ("presentation.pptx", 4.0),
        ("spreadsheet.xlsx", 1.5),
    ]
    
    telechargeur = TelechargeurFichier()
    
    # Téléchargement séquentiel
    temps_seq = telechargeur.telecharger_sequentiel(fichiers)
    
    print("\n" + "="*50 + "\n")
    
    # Téléchargement parallèle
    temps_par = telechargeur.telecharger_parallele(fichiers, nb_threads=3)
    
    # Statistiques
    telechargeur.afficher_statistiques(temps_seq, temps_par, fichiers)

if __name__ == "__main__":
    exemple_avance()
```

### 3.3 Explication détaillée

**Architecture :**
L'exemple utilise une classe `TelechargeurFichier` qui encapsule la logique de téléchargement et la gestion des threads.

**Fonctionnalités :**

1. **Simulation de téléchargement** (`simuler_telechargement`) :
   - Simule le téléchargement d'un fichier avec une progression
   - Utilise un verrou pour protéger l'affichage (évite que les messages se mélangent)
   - Incrémente un compteur de fichiers terminés

2. **Téléchargement séquentiel** (`telecharger_sequentiel`) :
   - Télécharge les fichiers un par un
   - Simple mais lent

3. **Téléchargement parallèle** (`telecharger_parallele`) :
   - Crée plusieurs threads pour télécharger en parallèle
   - Limite le nombre de threads simultanés (pour ne pas surcharger)
   - Attend que tous les threads se terminent

**Points techniques importants :**

- **Verrous pour l'affichage** : Protège `print()` pour éviter que les messages se mélangent
- **Gestion du nombre de threads** : Limite le nombre de threads actifs simultanément
- **Monitoring** : Suit la progression de chaque téléchargement

### 3.4 Résultat attendu

```
=== Téléchargement séquentiel ===

[MainThread] Début du téléchargement de document1.pdf (5.0 MB)
[MainThread] document1.pdf: 0%
[MainThread] document1.pdf: 25%
[MainThread] document1.pdf: 50%
[MainThread] document1.pdf: 75%
[MainThread] document1.pdf: 100%
[MainThread] ✓ document1.pdf téléchargé avec succès
...

=== Téléchargement parallèle (3 threads) ===

[Downloader-1] Début du téléchargement de document1.pdf (5.0 MB)
[Downloader-2] Début du téléchargement de image1.jpg (2.5 MB)
[Downloader-3] Début du téléchargement de video1.mp4 (10.0 MB)
[Downloader-2] image1.jpg: 0%
[Downloader-1] document1.pdf: 0%
[Downloader-3] video1.mp4: 0%
[Downloader-2] image1.jpg: 25%
...

==================================================
=== Statistiques ===
Nombre de fichiers : 6
Taille totale : 26.0 MB
Temps séquentiel : 26.00 secondes
Temps parallèle : 10.50 secondes
Accélération : 2.48x
Gain de temps : 15.50 secondes
==================================================
```

### 3.5 Analyse et améliorations possibles

**Analyse :**
- Le téléchargement parallèle est significativement plus rapide
- L'accélération n'est pas parfaite (3x) car il y a un overhead de gestion des threads
- Pour les opérations I/O, le threading est très efficace

**Améliorations possibles :**
- Utiliser `ThreadPoolExecutor` pour une gestion plus simple
- Ajouter une barre de progression globale
- Gérer les erreurs de téléchargement
- Implémenter un vrai téléchargement HTTP

---

## 4. Exercices

### Exercice 1 : Créer des threads simples

**Difficulté** : ⭐ Facile  
**Temps estimé** : 15-20 minutes  
**Objectif** : Maîtriser la création et le démarrage de threads

**Énoncé :**
Créez un programme qui :
1. Définit une fonction `afficher_nombres(nom, debut, fin)` qui affiche les nombres de `debut` à `fin`
2. Crée 3 threads qui affichent des séquences différentes :
   - Thread 1 : nombres de 1 à 10
   - Thread 2 : nombres de 11 à 20
   - Thread 3 : nombres de 21 à 30
3. Démarre tous les threads et attendez qu'ils se terminent
4. Affiche un message de fin

**Consignes :**
- Utilisez `threading.Thread` avec `target` et `args`
- Utilisez `start()` et `join()`
- Ajoutez un petit délai dans la fonction pour voir le parallélisme

**Solution :**

```python
import threading
import time

def afficher_nombres(nom, debut, fin):
    """Affiche une séquence de nombres."""
    for i in range(debut, fin + 1):
        print(f"[{nom}] {i}")
        time.sleep(0.1)  # Petit délai pour voir le parallélisme

if __name__ == "__main__":
    print("Démarrage des threads...\n")
    
    # Créer les threads
    thread1 = threading.Thread(
        target=afficher_nombres,
        args=("Thread-1", 1, 10),
        name="Thread-1"
    )
    
    thread2 = threading.Thread(
        target=afficher_nombres,
        args=("Thread-2", 11, 20),
        name="Thread-2"
    )
    
    thread3 = threading.Thread(
        target=afficher_nombres,
        args=("Thread-3", 21, 30),
        name="Thread-3"
    )
    
    # Démarrer les threads
    thread1.start()
    thread2.start()
    thread3.start()
    
    # Attendre qu'ils se terminent
    thread1.join()
    thread2.join()
    thread3.join()
    
    print("\n✓ Tous les threads sont terminés")
```

**Explication de la solution :**
Cet exercice pratique les bases : création, démarrage et attente de threads. Le délai permet de voir que les threads s'exécutent en parallèle (les nombres se mélangent).

---

### Exercice 2 : Threads daemon

**Difficulté** : ⭐⭐ Moyen  
**Temps estimé** : 25-30 minutes  
**Objectif** : Comprendre et utiliser les threads daemon

**Énoncé :**
Créez un programme qui :
1. Crée un thread daemon qui affiche la date/heure toutes les 2 secondes
2. Crée un thread normal qui fait un travail (affiche des messages pendant 5 secondes)
3. Observez la différence de comportement :
   - Avec le thread daemon : le programme se termine quand le thread normal se termine
   - Sans le thread daemon : le programme continue indéfiniment

**Consignes :**
- Utilisez `daemon=True` pour créer un thread daemon
- Utilisez `time.sleep()` pour simuler le travail
- Affichez clairement quand chaque thread se termine

**Solution :**

```python
import threading
import time
from datetime import datetime

def afficher_heure():
    """Affiche l'heure toutes les 2 secondes (thread daemon)."""
    while True:
        print(f"[Daemon] Heure actuelle : {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(2)

def travail_principal():
    """Fait un travail pendant 5 secondes."""
    print("[Main] Début du travail")
    for i in range(5):
        print(f"[Main] Travail en cours... {i+1}/5")
        time.sleep(1)
    print("[Main] Travail terminé")

if __name__ == "__main__":
    print("=== Test avec thread daemon ===\n")
    
    # Créer un thread daemon
    thread_daemon = threading.Thread(
        target=afficher_heure,
        daemon=True,
        name="Daemon-Thread"
    )
    
    # Créer un thread normal pour le travail
    thread_travail = threading.Thread(
        target=travail_principal,
        name="Work-Thread"
    )
    
    # Démarrer les threads
    thread_daemon.start()
    thread_travail.start()
    
    # Attendre que le thread de travail se termine
    thread_travail.join()
    
    print("\nLe thread principal se termine.")
    print("Le thread daemon devrait s'arrêter automatiquement.")
    time.sleep(1)  # Donner un peu de temps pour voir
```

**Explication de la solution :**
Cet exercice montre que les threads daemon se terminent automatiquement quand le programme principal se termine, même s'ils sont encore en cours d'exécution.

---

### Exercice 3 : Gestionnaire de threads

**Difficulté** : ⭐⭐⭐ Avancé  
**Temps estimé** : 40-50 minutes  
**Objectif** : Créer un système de gestion de threads

**Énoncé :**
Créez une classe `GestionnaireThreads` qui :
1. Peut ajouter des tâches à exécuter
2. Exécute les tâches avec un nombre limité de threads simultanés
3. Suit l'état de chaque thread (en attente, en cours, terminé)
4. Affiche un rapport final avec les statistiques

**Consignes :**
- Utilisez une liste pour stocker les tâches
- Limitez le nombre de threads actifs
- Utilisez des verrous pour protéger les structures de données partagées
- Affichez un rapport avec le temps d'exécution de chaque tâche

**Solution :**

```python
import threading
import time
from datetime import datetime

class GestionnaireThreads:
    """Gère l'exécution de tâches avec un pool de threads."""
    
    def __init__(self, nb_threads_max=3):
        self.nb_threads_max = nb_threads_max
        self.taches = []
        self.threads_actifs = []
        self.resultats = []
        self.verrou = threading.Lock()
    
    def ajouter_tache(self, fonction, *args, **kwargs):
        """Ajoute une tâche à exécuter."""
        tache = {
            'fonction': fonction,
            'args': args,
            'kwargs': kwargs,
            'statut': 'en_attente',
            'debut': None,
            'fin': None
        }
        self.taches.append(tache)
    
    def executer_tache(self, tache):
        """Exécute une tâche et enregistre les statistiques."""
        tache['statut'] = 'en_cours'
        tache['debut'] = time.time()
        
        try:
            resultat = tache['fonction'](*tache['args'], **tache['kwargs'])
            tache['statut'] = 'termine'
            tache['resultat'] = resultat
        except Exception as e:
            tache['statut'] = 'erreur'
            tache['erreur'] = str(e)
        finally:
            tache['fin'] = time.time()
            with self.verrou:
                self.resultats.append(tache)
    
    def executer_toutes(self):
        """Exécute toutes les tâches avec le pool de threads."""
        index = 0
        
        while index < len(self.taches) or any(t.is_alive() for t in self.threads_actifs):
            # Nettoyer les threads terminés
            self.threads_actifs = [t for t in self.threads_actifs if t.is_alive()]
            
            # Lancer de nouveaux threads si on a de la place
            while len(self.threads_actifs) < self.nb_threads_max and index < len(self.taches):
                tache = self.taches[index]
                thread = threading.Thread(
                    target=self.executer_tache,
                    args=(tache,),
                    name=f"Worker-{index+1}"
                )
                self.threads_actifs.append(thread)
                thread.start()
                index += 1
            
            time.sleep(0.1)
        
        # Attendre tous les threads
        for thread in self.threads_actifs:
            thread.join()
    
    def afficher_rapport(self):
        """Affiche un rapport des résultats."""
        print("\n" + "="*60)
        print("=== RAPPORT D'EXÉCUTION ===")
        print("="*60)
        
        for i, tache in enumerate(self.resultats, 1):
            duree = tache['fin'] - tache['debut'] if tache['fin'] else 0
            print(f"\nTâche {i}:")
            print(f"  Statut : {tache['statut']}")
            print(f"  Durée : {duree:.2f} secondes")
            if tache['statut'] == 'erreur':
                print(f"  Erreur : {tache['erreur']}")
        
        total = sum(t['fin'] - t['debut'] for t in self.resultats if t['fin'])
        print(f"\nTemps total : {total:.2f} secondes")
        print("="*60)

# Exemple d'utilisation
def tache_exemple(nom, duree):
    """Tâche d'exemple."""
    print(f"[{threading.current_thread().name}] Début de {nom}")
    time.sleep(duree)
    print(f"[{threading.current_thread().name}] Fin de {nom}")
    return f"Résultat de {nom}"

if __name__ == "__main__":
    gestionnaire = GestionnaireThreads(nb_threads_max=3)
    
    # Ajouter des tâches
    gestionnaire.ajouter_tache(tache_exemple, "Tâche 1", 2.0)
    gestionnaire.ajouter_tache(tache_exemple, "Tâche 2", 1.5)
    gestionnaire.ajouter_tache(tache_exemple, "Tâche 3", 3.0)
    gestionnaire.ajouter_tache(tache_exemple, "Tâche 4", 1.0)
    gestionnaire.ajouter_tache(tache_exemple, "Tâche 5", 2.5)
    
    # Exécuter toutes les tâches
    gestionnaire.executer_toutes()
    
    # Afficher le rapport
    gestionnaire.afficher_rapport()
```

**Explication de la solution :**
Cette solution crée un gestionnaire de threads qui limite le nombre de threads simultanés et suit l'état de chaque tâche. C'est une version simplifiée de `ThreadPoolExecutor`.

---

## 5. Résumé

### Concepts clés
- ✅ **threading.Thread** : Classe pour créer des threads
- ✅ **start()** : Démarre l'exécution d'un thread
- ✅ **join()** : Attend qu'un thread se termine
- ✅ **is_alive()** : Vérifie si un thread est actif
- ✅ **Threads daemon** : Se terminent automatiquement avec le programme

### Points importants à retenir
1. Les threads sont idéaux pour les opérations I/O (fichiers, réseau)
2. Le GIL limite le parallélisme réel pour le calcul CPU
3. Toujours utiliser `join()` pour attendre la fin des threads
4. Les threads daemon sont utiles pour des tâches de fond non critiques
5. Utiliser des verrous pour protéger les ressources partagées

### Pièges à éviter
- ⚠️ **Oublier `join()`** : Le programme peut se terminer avant que les threads finissent
- ⚠️ **Trop de threads** : Peut dégrader les performances
- ⚠️ **Partager des données sans protection** : Risque de race conditions
- ⚠️ **Utiliser threading pour le calcul CPU** : Utilisez `multiprocessing` à la place

---

## 6. Pour aller plus loin

### Ressources supplémentaires
- 📚 Documentation threading : https://docs.python.org/3/library/threading.html
- 📚 "Python Threading Tutorial" - Real Python
- 📚 `concurrent.futures.ThreadPoolExecutor` : API plus moderne pour les threads

### Concepts liés à explorer
- **ThreadPoolExecutor** : Gestion automatique d'un pool de threads
- **Thread-local storage** : Variables locales à chaque thread
- **Synchronisation avancée** : Events, Conditions, Semaphores

### Projets suggérés
- Créer un scraper web multi-thread
- Développer un serveur multi-clients avec threading
- Implémenter un système de traitement de fichiers parallèle

---

## 7. Questions de révision

1. Quelle est la différence entre `start()` et `join()` pour un thread ?
2. Pourquoi les threads Python ne permettent-ils pas le vrai parallélisme pour le calcul CPU ?
3. Qu'est-ce qu'un thread daemon et quand l'utiliser ?
4. Que se passe-t-il si vous oubliez d'appeler `join()` sur un thread ?
5. Dans quels cas le threading est-il plus efficace que l'exécution séquentielle ?

---

*[Chapitre précédent : Chapitre 3 - Concepts fondamentaux] | [Chapitre suivant : Chapitre 5 - Synchronisation avec Threads]*
