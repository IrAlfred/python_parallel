# Chapitre 7 : Multiprocessing - Les bases

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Comprendre le module `multiprocessing` de Python
- Créer et lancer des processus
- Comprendre pourquoi multiprocessing plutôt que threading pour le calcul CPU
- Utiliser `Process` pour créer des processus
- Comprendre la différence entre `Process` et `Pool`

---

## 1. Explication du principe

### 1.1 Pourquoi multiprocessing ?

**Limitation du threading avec le GIL :**
Le GIL (Global Interpreter Lock) empêche les threads Python d'exécuter du code Python en parallèle sur plusieurs cœurs. Pour le calcul CPU intensif, `multiprocessing` est la solution.

**Avantages de multiprocessing :**
- Vrai parallélisme : chaque processus a son propre GIL
- Utilise plusieurs cœurs efficacement
- Isolation : une erreur dans un processus n'affecte pas les autres
- Pas de problèmes de race conditions (mémoire isolée)

**Inconvénients :**
- Plus lourd : création plus lente que les threads
- Communication plus complexe (pas de mémoire partagée directe)
- Plus de mémoire utilisée

**Points clés à retenir :**
- Utilisez `multiprocessing` pour le calcul CPU intensif
- Utilisez `threading` pour les opérations I/O
- Chaque processus a sa propre mémoire

### 1.2 Création de processus

**Module multiprocessing :**
Le module `multiprocessing` fournit une API similaire à `threading` mais pour les processus.

**Création basique :**
```python
from multiprocessing import Process

def ma_fonction():
    pass

p = Process(target=ma_fonction)
p.start()
p.join()
```

**Points clés à retenir :**
- API similaire à `threading`
- Chaque processus a son propre interpréteur Python
- La communication nécessite des mécanismes spéciaux

### 1.3 Process vs Pool

**Process :**
- Contrôle fin sur chaque processus
- Utile quand vous avez besoin de gérer individuellement les processus
- Plus de code à écrire

**Pool :**
- Gestion automatique d'un pool de processus
- Plus simple pour paralléliser une fonction sur plusieurs données
- Recommandé pour la plupart des cas

**Points clés à retenir :**
- `Process` : Contrôle individuel
- `Pool` : Gestion automatique, plus simple

---

## 2. Exemple basique

### 2.1 Description

Exemple simple de création et utilisation de processus.

### 2.2 Code

```python
from multiprocessing import Process
import time
import os

def travail(nom, duree):
    """Fait un travail dans un processus."""
    print(f"[Processus {os.getpid()}] {nom} - Début")
    for i in range(5):
        time.sleep(duree / 5)
        print(f"[Processus {os.getpid()}] {nom} - Progression {i+1}/5")
    print(f"[Processus {os.getpid()}] {nom} - Terminé")

if __name__ == "__main__":
    print(f"Processus principal : {os.getpid()}\n")
    
    # Créer des processus
    p1 = Process(target=travail, args=("Tâche 1", 2.0))
    p2 = Process(target=travail, args=("Tâche 2", 1.5))
    p3 = Process(target=travail, args=("Tâche 3", 1.0))
    
    # Démarrer
    p1.start()
    p2.start()
    p3.start()
    
    # Attendre
    p1.join()
    p2.join()
    p3.join()
    
    print("\nTous les processus sont terminés")
```

### 2.3 Explication

Chaque processus a son propre PID (Process ID). Les processus s'exécutent vraiment en parallèle sur différents cœurs.

---

## 3. Exemple avancé

### 3.1 Description

Parallélisation d'un calcul intensif (calcul de nombres premiers).

### 3.2 Code

```python
from multiprocessing import Process, Queue
import time

def est_premier(n):
    """Vérifie si un nombre est premier."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def trouver_premiers(debut, fin, resultats):
    """Trouve les nombres premiers dans une plage."""
    premiers = []
    for n in range(debut, fin):
        if est_premier(n):
            premiers.append(n)
    resultats.put((debut, fin, len(premiers)))

if __name__ == "__main__":
    # Plage à analyser
    plage_totale = 100000
    nb_processus = 4
    taille_plage = plage_totale // nb_processus
    
    # Queue pour les résultats
    resultats = Queue()
    
    # Créer les processus
    processus = []
    for i in range(nb_processus):
        debut = i * taille_plage
        fin = (i + 1) * taille_plage if i < nb_processus - 1 else plage_totale
        p = Process(target=trouver_premiers, args=(debut, fin, resultats))
        processus.append(p)
        p.start()
    
    # Attendre et collecter les résultats
    for p in processus:
        p.join()
    
    # Afficher les résultats
    total_premiers = 0
    while not resultats.empty():
        debut, fin, nb = resultats.get()
        print(f"Plage [{debut}, {fin}]: {nb} nombres premiers")
        total_premiers += nb
    
    print(f"\nTotal: {total_premiers} nombres premiers trouvés")
```

---

## 4. Exercices

### Exercice 1 : Calcul parallèle simple

**Difficulté** : ⭐ Facile  
**Objectif** : Créer des processus pour un calcul simple

Créez un programme qui calcule la somme des carrés de 1 à 1000 en parallèle avec 4 processus.

### Exercice 2 : Comparaison threading vs multiprocessing

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Comparer les performances

Créez un programme qui compare threading et multiprocessing pour un calcul CPU intensif.

### Exercice 3 : Système de traitement distribué

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Créer un système avec plusieurs processus

Créez un système où un processus maître distribue des tâches à des processus workers.

---

## 5. Résumé

### Concepts clés
- ✅ **multiprocessing.Process** : Création de processus
- ✅ **Vrai parallélisme** : Chaque processus a son propre GIL
- ✅ **Mémoire isolée** : Pas de partage direct
- ✅ **Communication** : Via Queue, Pipe, etc.

### Points importants à retenir
1. Utilisez `multiprocessing` pour le calcul CPU
2. Chaque processus a sa propre mémoire
3. La communication nécessite des mécanismes spéciaux
4. Plus lourd que les threads mais vrai parallélisme

---

## 6. Pour aller plus loin

- Documentation multiprocessing : https://docs.python.org/3/library/multiprocessing.html
- Pool de processus (chapitre suivant)
- Communication inter-processus

---

## 7. Questions de révision

1. Pourquoi multiprocessing plutôt que threading pour le calcul CPU ?
2. Quelle est la différence entre Process et Pool ?
3. Pourquoi chaque processus a-t-il sa propre mémoire ?
4. Comment communiquent les processus entre eux ?
5. Quand utiliseriez-vous Process plutôt que Pool ?

---

*[Chapitre précédent : Chapitre 6 - Communication entre Threads] | [Chapitre suivant : Chapitre 8 - Pool de processus]*
