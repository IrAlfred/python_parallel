# Chapitre 14 : Gestion des erreurs et debugging

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Gérer les exceptions dans les threads
- Gérer les exceptions dans les processus
- Gérer les exceptions asynchrones
- Utiliser des outils de debugging pour le code parallèle
- Implémenter un système de logging thread-safe

---

## 1. Explication du principe

### 1.1 Exceptions dans les threads

**Problème :**
Les exceptions dans un thread ne sont pas automatiquement propagées au thread principal.

**Solution :**
- Utiliser `try/except` dans le thread
- Stocker les exceptions dans une structure partagée
- Utiliser `concurrent.futures` qui propage les exceptions

### 1.2 Exceptions dans les processus

**Problème :**
Les exceptions dans un processus sont isolées, difficiles à capturer.

**Solution :**
- Utiliser des queues pour transmettre les exceptions
- Utiliser `Pool` qui gère les exceptions
- Logger les erreurs

### 1.3 Exceptions asynchrones

**Gestion :**
Les exceptions dans les coroutines peuvent être gérées avec `try/except` et propagées avec `await`.

### 1.4 Debugging

**Outils :**
- Logging thread-safe
- Débogueurs (pdb, debugger intégré)
- Traces et stack traces
- Monitoring des threads/processus

---

## 2. Exemple basique

### 2.1 Description

Gestion d'exceptions dans les threads.

### 2.2 Code

```python
import threading
import queue

def travail_avec_erreur(nom, peut_echouer):
    """Travail qui peut échouer."""
    try:
        if peut_echouer:
            raise ValueError(f"Erreur dans {nom}")
        print(f"[{nom}] Succès")
        return f"Résultat {nom}"
    except Exception as e:
        print(f"[{nom}] Erreur: {e}")
        raise

def worker_avec_gestion(queue_taches, queue_resultats):
    """Worker qui gère les erreurs."""
    while True:
        try:
            tache = queue_taches.get(timeout=1)
            try:
                resultat = travail_avec_erreur(*tache)
                queue_resultats.put(('succès', resultat))
            except Exception as e:
                queue_resultats.put(('erreur', str(e)))
            queue_taches.task_done()
        except queue.Empty:
            break

if __name__ == "__main__":
    taches = queue.Queue()
    resultats = queue.Queue()
    
    # Ajouter des tâches
    taches.put(("T1", False))
    taches.put(("T2", True))  # Va échouer
    taches.put(("T3", False))
    
    # Worker
    w = threading.Thread(target=worker_avec_gestion, args=(taches, resultats))
    w.start()
    w.join()
    
    # Afficher les résultats
    while not resultats.empty():
        statut, valeur = resultats.get()
        print(f"{statut}: {valeur}")
```

---

## 3. Exemple avancé

### 3.1 Description

Système de logging thread-safe et gestion d'erreurs complète.

### 3.2 Code

```python
import threading
import logging
import queue
from datetime import datetime

# Configuration du logging thread-safe
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

class GestionnaireErreurs:
    """Gère les erreurs de manière centralisée."""
    
    def __init__(self):
        self.erreurs = []
        self.verrou = threading.Lock()
    
    def enregistrer_erreur(self, thread_nom, erreur):
        """Enregistre une erreur."""
        with self.verrou:
            self.erreurs.append({
                'thread': thread_nom,
                'erreur': str(erreur),
                'timestamp': datetime.now()
            })
            logger.error(f"[{thread_nom}] Erreur: {erreur}")
    
    def obtenir_erreurs(self):
        """Retourne toutes les erreurs."""
        with self.verrou:
            return self.erreurs.copy()

def travail_risque(nom, gestionnaire):
    """Travail qui peut échouer."""
    try:
        logger.info(f"[{nom}] Début du travail")
        # Simuler un travail qui peut échouer
        import random
        if random.random() < 0.3:
            raise ValueError(f"Erreur aléatoire dans {nom}")
        
        logger.info(f"[{nom}] Travail terminé avec succès")
        return f"Résultat {nom}"
    except Exception as e:
        gestionnaire.enregistrer_erreur(nom, e)
        return None

if __name__ == "__main__":
    gestionnaire = GestionnaireErreurs()
    
    threads = []
    for i in range(5):
        t = threading.Thread(
            target=travail_risque,
            args=(f"Thread-{i}", gestionnaire)
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    # Afficher les erreurs
    erreurs = gestionnaire.obtenir_erreurs()
    print(f"\n=== Résumé ===")
    print(f"Erreurs enregistrées: {len(erreurs)}")
    for err in erreurs:
        print(f"  - {err['thread']}: {err['erreur']}")
```

---

## 4. Exercices

### Exercice 1 : Gestion d'erreurs simple

**Difficulté** : ⭐ Facile  
**Objectif** : Capturer et gérer les erreurs dans les threads

Créez un programme qui gère gracieusement les erreurs dans plusieurs threads.

### Exercice 2 : Logging thread-safe

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Implémenter un système de logging thread-safe

Créez un système de logging qui fonctionne correctement avec plusieurs threads.

### Exercice 3 : Système de monitoring

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Créer un système de monitoring des threads/processus

Créez un système qui surveille l'état des threads et détecte les problèmes.

---

## 5. Résumé

### Concepts clés
- ✅ **Gestion d'exceptions** : Important dans un contexte parallèle
- ✅ **Logging thread-safe** : Utiliser le module logging
- ✅ **Propagation d'erreurs** : Via queues, futures, etc.
- ✅ **Debugging** : Outils et techniques spécifiques

### Points importants à retenir
1. Les exceptions ne se propagent pas automatiquement entre threads
2. Utilisez le module logging (thread-safe par défaut)
3. Stockez les erreurs dans des structures partagées
4. Utilisez des outils de debugging adaptés

---

## 6. Pour aller plus loin

- Documentation logging : https://docs.python.org/3/library/logging.html
- Outils de debugging avancés
- Monitoring et profiling

---

## 7. Questions de révision

1. Pourquoi les exceptions dans les threads ne se propagent-elles pas automatiquement ?
2. Comment gérer les erreurs dans un Pool de processus ?
3. Comment implémenter un logging thread-safe ?
4. Quels outils utilisez-vous pour déboguer du code parallèle ?
5. Comment surveiller l'état des threads/processus ?

---

*[Chapitre précédent : Chapitre 13 - Patterns de conception parallèle] | [Chapitre suivant : Chapitre 15 - Introduction à la programmation distribuée]*
