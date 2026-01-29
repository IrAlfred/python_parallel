# Chapitre 8 : Pool de processus

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Utiliser `Pool` pour gérer un pool de processus
- Utiliser `map()`, `apply()`, `apply_async()` pour paralléliser des fonctions
- Gérer les résultats et les erreurs
- Comprendre quand utiliser chaque méthode

---

## 1. Explication du principe

### 1.1 Pool de processus

**Qu'est-ce qu'un Pool ?**
Un `Pool` gère automatiquement un ensemble de processus workers. C'est plus simple que de gérer individuellement chaque processus.

**Avantages :**
- Gestion automatique des processus
- Réutilisation des processus (moins de overhead)
- API simple et intuitive

**Création :**
```python
from multiprocessing import Pool

with Pool(processes=4) as pool:
    resultats = pool.map(ma_fonction, donnees)
```

### 1.2 Méthodes principales

**`map(func, iterable)` :**
Applique une fonction à chaque élément d'un itérable en parallèle. Bloque jusqu'à ce que tous les résultats soient prêts.

**`apply(func, args)` :**
Exécute une fonction avec des arguments. Bloque jusqu'à ce que le résultat soit prêt.

**`apply_async(func, args)` :**
Version asynchrone de `apply()`. Retourne immédiatement un objet `AsyncResult`.

**Points clés à retenir :**
- `map` : Pour appliquer une fonction à une liste
- `apply` : Pour une fonction avec arguments
- `apply_async` : Pour ne pas bloquer

---

## 2. Exemple basique

### 2.1 Description

Utilisation de Pool.map() pour paralléliser un calcul.

### 2.2 Code

```python
from multiprocessing import Pool
import time

def calcul_carre(n):
    """Calcule le carré d'un nombre."""
    time.sleep(0.1)  # Simule un calcul
    return n * n

if __name__ == "__main__":
    nombres = list(range(1, 11))
    
    print("Calcul séquentiel...")
    debut = time.time()
    resultats_seq = [calcul_carre(n) for n in nombres]
    temps_seq = time.time() - debut
    print(f"Temps: {temps_seq:.2f}s")
    
    print("\nCalcul parallèle avec Pool...")
    debut = time.time()
    with Pool(processes=4) as pool:
        resultats_par = pool.map(calcul_carre, nombres)
    temps_par = time.time() - debut
    print(f"Temps: {temps_par:.2f}s")
    print(f"Accélération: {temps_seq/temps_par:.2f}x")
    
    print(f"\nRésultats: {resultats_par}")
```

---

## 3. Exemple avancé

### 3.1 Description

Traitement de fichiers en parallèle avec gestion d'erreurs.

### 3.2 Code

```python
from multiprocessing import Pool
import os
import time

def traiter_fichier(nom_fichier):
    """Traite un fichier et retourne des statistiques."""
    try:
        # Simuler le traitement
        time.sleep(0.5)
        
        # Simuler une erreur pour certains fichiers
        if "erreur" in nom_fichier:
            raise ValueError(f"Erreur dans {nom_fichier}")
        
        taille = os.path.getsize(nom_fichier) if os.path.exists(nom_fichier) else 1000
        return {
            'fichier': nom_fichier,
            'taille': taille,
            'statut': 'succès'
        }
    except Exception as e:
        return {
            'fichier': nom_fichier,
            'erreur': str(e),
            'statut': 'erreur'
        }

if __name__ == "__main__":
    fichiers = [f"fichier_{i}.txt" for i in range(10)]
    
    print("Traitement parallèle avec Pool...\n")
    
    with Pool(processes=4) as pool:
        resultats = pool.map(traiter_fichier, fichiers)
    
    # Afficher les résultats
    print("=== Résultats ===")
    for res in resultats:
        if res['statut'] == 'succès':
            print(f"✓ {res['fichier']}: {res['taille']} bytes")
        else:
            print(f"✗ {res['fichier']}: {res['erreur']}")
```

---

## 4. Exercices

### Exercice 1 : Utiliser Pool.map()

**Difficulté** : ⭐ Facile  
**Objectif** : Paralléliser avec Pool.map()

Créez un programme qui calcule les factorielles de 1 à 20 en parallèle.

### Exercice 2 : Utiliser apply_async()

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Utiliser apply_async() pour ne pas bloquer

Créez un programme qui lance plusieurs tâches avec apply_async() et collecte les résultats.

### Exercice 3 : Gestion d'erreurs avancée

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Gérer les erreurs dans un Pool

Créez un système qui traite des données et gère gracieusement les erreurs.

---

## 5. Résumé

### Concepts clés
- ✅ **Pool** : Gestion automatique de processus
- ✅ **map()** : Applique une fonction à une liste
- ✅ **apply_async()** : Version non-bloquante
- ✅ **Gestion d'erreurs** : Important dans un contexte parallèle

### Points importants à retenir
1. Pool simplifie la gestion des processus
2. map() est idéal pour paralléliser une fonction sur une liste
3. apply_async() permet de ne pas bloquer
4. Toujours gérer les erreurs

---

## 6. Pour aller plus loin

- ProcessPoolExecutor (concurrent.futures)
- Gestion avancée des résultats
- Callbacks avec apply_async()

---

## 7. Questions de révision

1. Quelle est la différence entre map() et apply() ?
2. Quand utiliseriez-vous apply_async() plutôt que apply() ?
3. Comment gérer les erreurs dans un Pool ?
4. Pourquoi Pool est-il plus efficace que de créer des Process individuellement ?
5. Comment limiter le nombre de processus dans un Pool ?

---

*[Chapitre précédent : Chapitre 7 - Multiprocessing - Les bases] | [Chapitre suivant : Chapitre 9 - Communication inter-processus]*
