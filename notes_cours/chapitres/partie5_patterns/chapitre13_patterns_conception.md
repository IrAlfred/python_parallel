# Chapitre 13 : Patterns de conception parallèle

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Comprendre et implémenter le pattern Producteur-Consommateur
- Comprendre et implémenter le pattern Map-Reduce
- Comprendre et implémenter le pattern Worker Pool
- Comprendre et implémenter le pattern Pipeline
- Comprendre et implémenter le pattern Master-Worker

---

## 1. Explication du principe

### 1.1 Pattern Producteur-Consommateur

**Concept :**
Des threads/processus producteurs créent des données, des consommateurs les traitent. Communication via une queue.

**Avantages :**
- Découplage entre production et consommation
- Permet de gérer des rythmes différents
- Scalable (plusieurs producteurs/consommateurs)

### 1.2 Pattern Map-Reduce

**Concept :**
Divise les données en chunks, traite chaque chunk en parallèle (map), puis combine les résultats (reduce).

**Avantages :**
- Parallélisation naturelle
- Scalable sur plusieurs machines
- Utilisé par Hadoop, Spark, etc.

### 1.3 Pattern Worker Pool

**Concept :**
Un pool de workers traite des tâches depuis une queue. Les workers sont réutilisés.

**Avantages :**
- Réutilisation des workers
- Gestion automatique du pool
- Équilibrage de charge

### 1.4 Pattern Pipeline

**Concept :**
Les données passent par plusieurs étapes de traitement, chaque étape peut être parallélisée.

**Avantages :**
- Traitement en plusieurs phases
- Parallélisation par étape
- Flux de données clair

### 1.5 Pattern Master-Worker

**Concept :**
Un processus maître distribue des tâches à des workers, collecte les résultats.

**Avantages :**
- Contrôle centralisé
- Distribution flexible
- Scalable

---

## 2. Exemple basique

### 2.1 Description

Implémentation du pattern Producteur-Consommateur.

### 2.2 Code

```python
import threading
import queue
import time
import random

def producteur(queue_obj, nb_items):
    """Produit des items."""
    for i in range(nb_items):
        item = f"Item-{i}"
        queue_obj.put(item)
        print(f"[Producteur] Produit: {item}")
        time.sleep(random.uniform(0.1, 0.5))

def consommateur(queue_obj, nom):
    """Consomme des items."""
    while True:
        try:
            item = queue_obj.get(timeout=2)
            print(f"[{nom}] Traite: {item}")
            time.sleep(random.uniform(0.2, 0.8))
            queue_obj.task_done()
        except queue.Empty:
            break

if __name__ == "__main__":
    q = queue.Queue(maxsize=5)
    
    # Producteurs
    p1 = threading.Thread(target=producteur, args=(q, 5))
    p2 = threading.Thread(target=producteur, args=(q, 5))
    
    # Consommateurs
    c1 = threading.Thread(target=consommateur, args=(q, "C1"))
    c2 = threading.Thread(target=consommateur, args=(q, "C2"))
    
    p1.start()
    p2.start()
    c1.start()
    c2.start()
    
    p1.join()
    p2.join()
    q.join()
```

---

## 3. Exemple avancé

### 3.1 Description

Implémentation du pattern Map-Reduce pour traiter des fichiers.

### 3.2 Code

```python
from multiprocessing import Pool
import os

def map_phase(fichier):
    """Phase map : traite un fichier."""
    # Simuler le traitement
    taille = os.path.getsize(fichier) if os.path.exists(fichier) else 1000
    return {
        'fichier': fichier,
        'taille': taille,
        'mots': taille // 10  # Estimation
    }

def reduce_phase(resultats):
    """Phase reduce : combine les résultats."""
    total_taille = sum(r['taille'] for r in resultats)
    total_mots = sum(r['mots'] for r in resultats)
    return {
        'nb_fichiers': len(resultats),
        'taille_totale': total_taille,
        'mots_totaux': total_mots
    }

if __name__ == "__main__":
    fichiers = [f"fichier_{i}.txt" for i in range(10)]
    
    # Phase Map (parallèle)
    with Pool(processes=4) as pool:
        resultats_map = pool.map(map_phase, fichiers)
    
    # Phase Reduce (séquentielle)
    resultat_final = reduce_phase(resultats_map)
    
    print("=== Résultats Map-Reduce ===")
    print(f"Fichiers traités: {resultat_final['nb_fichiers']}")
    print(f"Taille totale: {resultat_final['taille_totale']} bytes")
    print(f"Mots totaux: {resultat_final['mots_totaux']}")
```

---

## 4. Exercices

### Exercice 1 : Worker Pool

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Implémenter un Worker Pool

Créez un système avec un pool de workers qui traitent des tâches depuis une queue.

### Exercice 2 : Pipeline

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Implémenter un Pipeline

Créez un pipeline avec plusieurs étapes de traitement parallélisées.

### Exercice 3 : Master-Worker

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Implémenter Master-Worker

Créez un système maître-worker qui distribue des tâches.

---

## 5. Résumé

### Concepts clés
- ✅ **Producteur-Consommateur** : Découplage production/consommation
- ✅ **Map-Reduce** : Diviser, traiter, combiner
- ✅ **Worker Pool** : Pool réutilisable de workers
- ✅ **Pipeline** : Traitement en plusieurs phases
- ✅ **Master-Worker** : Distribution centralisée

### Points importants à retenir
1. Chaque pattern a ses avantages
2. Choisissez le pattern selon votre cas d'usage
3. Les patterns peuvent être combinés
4. La scalabilité dépend du pattern choisi

---

## 6. Pour aller plus loin

- Design Patterns pour la programmation parallèle
- Implémentations avancées
- Performance et optimisation

---

## 7. Questions de révision

1. Quand utiliseriez-vous le pattern Producteur-Consommateur ?
2. Comment fonctionne Map-Reduce ?
3. Quelle est la différence entre Worker Pool et Master-Worker ?
4. Comment implémenter un Pipeline parallèle ?
5. Quels patterns peuvent être combinés ?

---

*[Chapitre précédent : Chapitre 12 - Synchronisation asynchrone] | [Chapitre suivant : Chapitre 14 - Gestion des erreurs et debugging]*
