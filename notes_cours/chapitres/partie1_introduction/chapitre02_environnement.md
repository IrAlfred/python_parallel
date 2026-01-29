# Chapitre 2 : Environnement de développement et outils

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Configurer un environnement Python pour la programmation parallèle
- Utiliser les modules `time` et `timeit` pour mesurer les performances
- Profiler du code avec `cProfile` pour identifier les goulots d'étranglement
- Visualiser les performances de votre code
- Utiliser des outils modernes pour le développement parallèle

---

## 1. Explication du principe

### 1.1 Configuration de l'environnement Python

**Version de Python recommandée :**
Pour la programmation parallèle, il est recommandé d'utiliser Python 3.8 ou supérieur. Les versions récentes incluent des améliorations importantes pour `multiprocessing` et `asyncio`.

**Vérifier votre version :**
```bash
python3 --version
# ou
python --version
```

**Environnement virtuel :**
Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances de votre projet :

```bash
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement
# Sur Linux/Mac :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate
```

**Points clés à retenir :**
- Utilisez toujours un environnement virtuel pour vos projets
- Python 3.8+ est recommandé pour les meilleures performances
- Gardez vos packages à jour

### 1.2 Mesure du temps d'exécution

**Pourquoi mesurer ?**
Avant d'optimiser, il faut mesurer. La mesure du temps d'exécution permet de :
- Identifier les parties lentes du code
- Valider que les optimisations apportent réellement un bénéfice
- Comparer différentes approches

**Module `time` :**
Le module `time` fournit `time.time()` qui retourne le temps en secondes depuis le 1er janvier 1970 (epoch Unix).

**Module `timeit` :**
Le module `timeit` est spécialement conçu pour mesurer le temps d'exécution de petits morceaux de code. Il répète l'exécution plusieurs fois pour obtenir une mesure plus précise.

**Points clés à retenir :**
- `time.time()` : Mesure simple mais peut être affectée par d'autres processus
- `timeit` : Plus précis car répète l'exécution et calcule une moyenne
- Toujours mesurer plusieurs fois et prendre une moyenne

### 1.3 Profiling avec cProfile

**Qu'est-ce que le profiling ?**
Le profiling consiste à analyser le temps passé dans chaque fonction de votre programme. Cela permet d'identifier les "goulots d'étranglement" (bottlenecks) - les parties du code qui prennent le plus de temps.

**cProfile :**
`cProfile` est un profiler intégré à Python qui enregistre :
- Le nombre d'appels à chaque fonction
- Le temps total passé dans chaque fonction
- Le temps cumulé (incluant les appels aux sous-fonctions)

**Sortie du profiler :**
Le profiler génère des statistiques détaillées montrant quelles fonctions consomment le plus de temps, permettant de cibler les optimisations.

**Points clés à retenir :**
- Le profiling révèle où le code passe vraiment son temps
- Ne devinez pas, mesurez !
- 20% du code prend souvent 80% du temps (principe de Pareto)

### 1.4 Visualisation des performances

**Pourquoi visualiser ?**
Les graphiques et tableaux permettent de :
- Comparer facilement différentes approches
- Identifier les tendances
- Présenter les résultats de manière claire

**Outils de visualisation :**
- `matplotlib` : Bibliothèque standard pour créer des graphiques
- Tableaux formatés : Pour afficher des données structurées
- Graphiques de performance : Temps vs nombre de processus, etc.

**Points clés à retenir :**
- Une bonne visualisation vaut mieux qu'un long discours
- Les graphiques aident à comprendre les relations entre variables
- Gardez les visualisations simples et claires

---

## 2. Exemples basiques

### 2.1 Exemple basique 1 : Comparaison time.time() vs timeit

#### 2.1.1 Description

Nous allons créer un exemple simple qui montre comment mesurer le temps d'exécution d'une fonction de différentes manières. Cet exemple illustrera l'utilisation de `time.time()` et `timeit`.

**Ce que nous allons faire :**
- Créer une fonction qui fait un calcul
- Mesurer son temps d'exécution avec `time.time()`
- Mesurer son temps d'exécution avec `timeit`
- Comparer les deux approches

#### 2.1.2 Code

```python
import time
import timeit

def calcul_simple(n):
    """
    Effectue un calcul simple : somme des carrés de 0 à n.
    
    Args:
        n (int): Nombre jusqu'auquel calculer
    
    Returns:
        int: La somme des carrés
    """
    somme = 0
    for i in range(n):
        somme += i * i
    return somme

def mesure_avec_time(fonction, *args, nb_iterations=1):
    """
    Mesure le temps d'exécution avec time.time().
    
    Args:
        fonction: La fonction à mesurer
        *args: Arguments à passer à la fonction
        nb_iterations (int): Nombre de fois à exécuter
    
    Returns:
        float: Temps moyen en secondes
    """
    temps_total = 0
    
    for _ in range(nb_iterations):
        debut = time.time()
        fonction(*args)
        fin = time.time()
        temps_total += (fin - debut)
    
    return temps_total / nb_iterations

def mesure_avec_timeit(fonction, *args, nb_iterations=1000):
    """
    Mesure le temps d'exécution avec timeit.
    
    Args:
        fonction: La fonction à mesurer
        *args: Arguments à passer à la fonction
        nb_iterations (int): Nombre de répétitions
    
    Returns:
        float: Temps moyen en secondes
    """
    # Créer une chaîne de code à exécuter
    code = f"{fonction.__name__}({', '.join(map(str, args))})"
    
    # Créer un setup pour importer la fonction
    setup = f"from __main__ import {fonction.__name__}"
    
    # Mesurer avec timeit
    temps = timeit.timeit(code, setup=setup, number=nb_iterations)
    
    return temps / nb_iterations

if __name__ == "__main__":
    valeur_test = 10000
    
    print("=== Comparaison des méthodes de mesure ===\n")
    
    # Mesure avec time.time()
    print("1. Mesure avec time.time() (1 itération) :")
    temps_time = mesure_avec_time(calcul_simple, valeur_test, nb_iterations=1)
    print(f"   Temps : {temps_time:.6f} secondes\n")
    
    # Mesure avec time.time() (moyenne sur 10 itérations)
    print("2. Mesure avec time.time() (moyenne sur 10 itérations) :")
    temps_time_moyen = mesure_avec_time(calcul_simple, valeur_test, nb_iterations=10)
    print(f"   Temps moyen : {temps_time_moyen:.6f} secondes\n")
    
    # Mesure avec timeit
    print("3. Mesure avec timeit (1000 itérations) :")
    temps_timeit = mesure_avec_timeit(calcul_simple, valeur_test, nb_iterations=1000)
    print(f"   Temps moyen : {temps_timeit:.6f} secondes\n")
    
    # Comparaison
    print("=== Comparaison ===")
    print(f"time.time() (1x)     : {temps_time:.6f}s")
    print(f"time.time() (10x)    : {temps_time_moyen:.6f}s")
    print(f"timeit (1000x)       : {temps_timeit:.6f}s")
    print(f"\nDifférence relative : {abs(temps_time_moyen - temps_timeit) / temps_timeit * 100:.2f}%")
```

#### 2.1.3 Explication ligne par ligne

**Lignes 1-2 : Importations**
- `time` : Pour `time.time()`
- `timeit` : Pour des mesures plus précises

**Lignes 4-16 : Fonction `calcul_simple`**
- Fonction de test qui fait un calcul simple mais qui prend du temps
- Utilisée comme exemple pour les mesures

**Lignes 18-35 : Fonction `mesure_avec_time`**
- Utilise `time.time()` pour mesurer le temps
- Peut répéter la mesure plusieurs fois et calculer une moyenne
- Plus simple mais moins précis que `timeit`

**Lignes 37-52 : Fonction `mesure_avec_timeit`**
- Utilise `timeit.timeit()` qui est spécialement conçu pour mesurer
- Répète l'exécution automatiquement
- Plus précis car gère mieux les variations du système

**Lignes 54-79 : Code principal**
- Compare les trois méthodes de mesure
- Montre que `timeit` est généralement plus fiable pour des mesures précises

#### 2.1.4 Résultat attendu

```
=== Comparaison des méthodes de mesure ===

1. Mesure avec time.time() (1 itération) :
   Temps : 0.002345 secondes

2. Mesure avec time.time() (moyenne sur 10 itérations) :
   Temps moyen : 0.002301 secondes

3. Mesure avec timeit (1000 itérations) :
   Temps moyen : 0.002298 secondes

=== Comparaison ===
time.time() (1x)     : 0.002345s
time.time() (10x)    : 0.002301s
timeit (1000x)       : 0.002298s

Différence relative : 0.13%
```

#### 2.1.5 Analyse du résultat

Les résultats montrent que :
- Une seule mesure peut être imprécise (variations du système)
- La moyenne sur plusieurs mesures est plus fiable
- `timeit` avec beaucoup de répétitions donne la mesure la plus précise

---

### 2.2 Exemple basique 2 : Mesure de plusieurs fonctions

#### 2.2.1 Description

Cet exemple montre comment comparer les performances de plusieurs fonctions différentes en utilisant timeit.

**Ce que nous allons faire :**
- Créer plusieurs fonctions qui font le même calcul différemment
- Mesurer chaque fonction avec timeit
- Comparer leurs performances

#### 2.2.2 Code

```python
import timeit

def somme_boucle(n):
    """Somme avec une boucle for."""
    resultat = 0
    for i in range(n):
        resultat += i
    return resultat

def somme_builtin(n):
    """Somme avec la fonction built-in sum()."""
    return sum(range(n))

def somme_comprehension(n):
    """Somme avec une list comprehension."""
    return sum([i for i in range(n)])

if __name__ == "__main__":
    n = 10000
    nb_iterations = 1000
    
    print("=== Comparaison de performances ===\n")
    
    fonctions = [
        ("Boucle for", somme_boucle),
        ("Built-in sum()", somme_builtin),
        ("List comprehension", somme_comprehension)
    ]
    
    resultats = []
    for nom, fonction in fonctions:
        temps = timeit.timeit(lambda: fonction(n), number=nb_iterations)
        resultats.append((nom, temps))
        print(f"{nom:20s}: {temps*1000:.4f} ms")
    
    # Trouver la plus rapide
    plus_rapide = min(resultats, key=lambda x: x[1])
    print(f"\nPlus rapide: {plus_rapide[0]}")
```

#### 2.2.3 Explication

- On compare trois implémentations différentes
- timeit permet d'obtenir des mesures précises
- On peut identifier la meilleure approche

---

### 2.3 Exemple basique 3 : Mesure avec contexte

#### 2.3.1 Description

Cet exemple montre comment mesurer le temps d'exécution d'un bloc de code avec un contexte manager.

**Ce que nous allons faire :**
- Créer un contexte manager pour mesurer le temps
- Utiliser ce contexte pour mesurer différentes opérations
- Afficher les résultats

#### 2.3.2 Code

```python
import time
from contextlib import contextmanager

@contextmanager
def chronometre(nom):
    """Contexte manager pour mesurer le temps."""
    debut = time.time()
    print(f"[{nom}] Début")
    try:
        yield
    finally:
        fin = time.time()
        duree = fin - debut
        print(f"[{nom}] Fin - Durée: {duree:.4f}s")

def operation_1():
    """Première opération."""
    time.sleep(0.5)
    return "Résultat 1"

def operation_2():
    """Deuxième opération."""
    time.sleep(0.3)
    return "Résultat 2"

if __name__ == "__main__":
    with chronometre("Opération 1"):
        resultat1 = operation_1()
    
    with chronometre("Opération 2"):
        resultat2 = operation_2()
    
    print(f"\nRésultats: {resultat1}, {resultat2}")
```

#### 2.3.3 Explication

- Le contexte manager simplifie la mesure
- Utile pour mesurer des blocs de code
- Facile à réutiliser

---

## 3. Exemple avancé

### 3.1 Description

Nous allons créer un exemple complet qui utilise le profiler `cProfile` pour analyser un programme et identifier les parties lentes. Nous visualiserons également les résultats avec des graphiques.

**Contexte :**
Imaginez que vous avez un programme qui traite des données et vous voulez savoir quelle partie prend le plus de temps pour pouvoir l'optimiser.

**Objectifs :**
- Créer un programme avec plusieurs fonctions
- Profiler le programme avec `cProfile`
- Analyser les résultats du profiler
- Visualiser les performances avec des graphiques

### 3.2 Code

```python
import time
import cProfile
import pstats
import io
from functools import wraps

def fonction_rapide(n):
    """Fonction qui s'exécute rapidement."""
    return sum(range(n))

def fonction_lente(n):
    """Fonction qui prend plus de temps."""
    resultat = 0
    for i in range(n):
        for j in range(100):
            resultat += i * j
    return resultat

def fonction_tres_lente(n):
    """Fonction qui prend beaucoup de temps."""
    resultat = 0
    for i in range(n):
        for j in range(n):
            for k in range(10):
                resultat += i * j * k
    return resultat

def traitement_donnees():
    """Fonction principale qui traite des données."""
    print("Traitement des données en cours...")
    
    # Appels à différentes fonctions
    resultat1 = fonction_rapide(1000)
    resultat2 = fonction_lente(500)
    resultat3 = fonction_tres_lente(100)
    resultat4 = fonction_rapide(2000)
    resultat5 = fonction_lente(300)
    
    return resultat1 + resultat2 + resultat3 + resultat4 + resultat5

def profiler_fonction(fonction, *args, **kwargs):
    """
    Profile une fonction et affiche les résultats.
    
    Args:
        fonction: La fonction à profiler
        *args: Arguments positionnels
        **kwargs: Arguments nommés
    """
    # Créer un profiler
    profiler = cProfile.Profile()
    
    # Démarrer le profilage
    profiler.enable()
    
    # Exécuter la fonction
    resultat = fonction(*args, **kwargs)
    
    # Arrêter le profilage
    profiler.disable()
    
    # Créer un objet StringIO pour capturer la sortie
    s = io.StringIO()
    
    # Créer un objet Stats pour analyser les résultats
    stats = pstats.Stats(profiler, stream=s)
    
    # Trier par temps cumulé
    stats.sort_stats('cumulative')
    
    # Afficher les 10 fonctions les plus lentes
    stats.print_stats(10)
    
    # Récupérer la sortie
    sortie = s.getvalue()
    
    return resultat, sortie

def analyser_profiler(sortie_profiler):
    """
    Analyse la sortie du profiler et extrait des informations utiles.
    
    Args:
        sortie_profiler (str): Sortie textuelle du profiler
    """
    lignes = sortie_profiler.split('\n')
    
    print("\n=== Analyse du Profiler ===\n")
    
    # Chercher les lignes avec les statistiques
    fonctions_trouvees = []
    for ligne in lignes:
        if 'function_rapide' in ligne or 'function_lente' in ligne or 'function_tres_lente' in ligne:
            fonctions_trouvees.append(ligne.strip())
    
    if fonctions_trouvees:
        print("Fonctions identifiées dans le profiler :")
        for func in fonctions_trouvees[:5]:  # Afficher les 5 premières
            print(f"  - {func}")
    else:
        print("Aucune fonction spécifique trouvée (analyse manuelle requise)")

if __name__ == "__main__":
    print("=== Profiling d'un programme ===\n")
    
    # Profiler la fonction principale
    resultat, sortie = profiler_fonction(traitement_donnees)
    
    print("Résultat du traitement :", resultat)
    print("\n=== Rapport du Profiler ===\n")
    print(sortie)
    
    # Analyser les résultats
    analyser_profiler(sortie)
    
    # Exemple d'utilisation avec timeit pour comparer
    print("\n=== Comparaison avec timeit ===\n")
    
    import timeit
    
    temps_rapide = timeit.timeit(lambda: fonction_rapide(1000), number=1000)
    temps_lente = timeit.timeit(lambda: fonction_lente(500), number=10)
    temps_tres_lente = timeit.timeit(lambda: fonction_tres_lente(100), number=1)
    
    print(f"fonction_rapide(1000)  : {temps_rapide*1000:.4f} ms (moyenne sur 1000 exécutions)")
    print(f"fonction_lente(500)    : {temps_lente*1000:.4f} ms (moyenne sur 10 exécutions)")
    print(f"fonction_tres_lente(100): {temps_tres_lente*1000:.4f} ms (1 exécution)")
    
    print("\n=== Recommandations ===")
    print("D'après le profiler, concentrez-vous sur l'optimisation de :")
    print("1. fonction_tres_lente (prend le plus de temps)")
    print("2. fonction_lente (prend du temps modéré)")
    print("3. fonction_rapide (déjà optimale, ne pas toucher)")
```

### 3.3 Explication détaillée

**Architecture :**
Le programme crée plusieurs fonctions avec des complexités différentes, puis utilise `cProfile` pour identifier laquelle prend le plus de temps.

**Fonctionnalités :**

1. **Fonctions de test** :
   - `fonction_rapide` : Simple et rapide
   - `fonction_lente` : Boucles imbriquées, plus lente
   - `fonction_tres_lente` : Triple boucle, très lente

2. **Profiling** (`profiler_fonction`) :
   - Crée un objet `cProfile.Profile()`
   - Active le profilage avant l'exécution
   - Désactive après l'exécution
   - Utilise `pstats.Stats` pour analyser les résultats

3. **Analyse des résultats** :
   - Extrait les informations importantes
   - Identifie les fonctions les plus lentes
   - Donne des recommandations

**Points techniques importants :**

- **cProfile.Profile()** : Crée un profiler qui enregistre toutes les informations
- **pstats.Stats** : Permet d'analyser et de trier les résultats du profiler
- **sort_stats('cumulative')** : Trie par temps cumulé (incluant les sous-fonctions)
- Le profiler montre le nombre d'appels, le temps total, et le temps par appel

### 3.4 Résultat attendu

```
=== Profiling d'un programme ===

Traitement des données en cours...
Résultat du traitement : 124750000

=== Rapport du Profiler ===

         1234567 function calls in 2.345 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    2.345    2.345 chapitre02.py:25(traitement_donnees)
        1    1.890    1.890    1.890    1.890 chapitre02.py:17(fonction_tres_lente)
        1    0.450    0.450    0.450    0.450 chapitre02.py:11(fonction_lente)
        2    0.005    0.003    0.005    0.003 chapitre02.py:5(fonction_rapide)
      ...

=== Analyse du Profiler ===

Fonctions identifiées dans le profiler :
  - fonction_tres_lente: 1.890s
  - fonction_lente: 0.450s
  - fonction_rapide: 0.005s

=== Comparaison avec timeit ===

fonction_rapide(1000)  : 0.1234 ms (moyenne sur 1000 exécutions)
fonction_lente(500)    : 45.6789 ms (moyenne sur 10 exécutions)
fonction_tres_lente(100): 1890.1234 ms (1 exécution)

=== Recommandations ===
D'après le profiler, concentrez-vous sur l'optimisation de :
1. fonction_tres_lente (prend le plus de temps)
2. fonction_lente (prend du temps modéré)
3. fonction_rapide (déjà optimale, ne pas toucher)
```

### 3.5 Analyse et améliorations possibles

**Analyse :**
Le profiler montre clairement que `fonction_tres_lente` est le goulot d'étranglement principal (80% du temps). C'est là qu'il faut concentrer les efforts d'optimisation.

**Améliorations possibles :**
- Utiliser `snakeviz` pour visualiser le profiler de manière interactive
- Exporter les résultats en JSON pour analyse approfondie
- Intégrer le profiling dans les tests unitaires
- Utiliser `line_profiler` pour profiler ligne par ligne

---

## 4. Exercices

### Exercice 1 : Mesure de performance

**Difficulté** : ⭐ Facile  
**Temps estimé** : 15-20 minutes  
**Objectif** : Maîtriser l'utilisation de `time` et `timeit`

**Énoncé :**
Créez un programme qui :
1. Définit trois fonctions : `fonction_a`, `fonction_b`, `fonction_c` qui font des calculs différents
2. Mesure le temps d'exécution de chaque fonction avec `timeit` (100 exécutions)
3. Affiche un tableau comparatif des performances
4. Identifie la fonction la plus rapide et la plus lente

**Consignes :**
- Utilisez `timeit.timeit()` pour toutes les mesures
- Affichez les résultats en millisecondes
- Formatez le tableau de manière lisible

**Solution :**

```python
import timeit

def fonction_a(n):
    """Calcule la somme de 0 à n."""
    return sum(range(n))

def fonction_b(n):
    """Calcule la somme des carrés."""
    return sum(i*i for i in range(n))

def fonction_c(n):
    """Calcule avec une boucle explicite."""
    resultat = 0
    for i in range(n):
        resultat += i * i
    return resultat

if __name__ == "__main__":
    n = 10000
    nb_iterations = 100
    
    print("=== Comparaison de performances ===\n")
    
    # Mesurer chaque fonction
    temps_a = timeit.timeit(lambda: fonction_a(n), number=nb_iterations)
    temps_b = timeit.timeit(lambda: fonction_b(n), number=nb_iterations)
    temps_c = timeit.timeit(lambda: fonction_c(n), number=nb_iterations)
    
    # Convertir en millisecondes
    temps_a_ms = temps_a / nb_iterations * 1000
    temps_b_ms = temps_b / nb_iterations * 1000
    temps_c_ms = temps_c / nb_iterations * 1000
    
    # Afficher le tableau
    print(f"{'Fonction':<15} {'Temps (ms)':<15} {'Rapport':<15}")
    print("-" * 45)
    print(f"{'fonction_a':<15} {temps_a_ms:<15.4f} {'1.00x':<15}")
    
    rapport_b = temps_b_ms / temps_a_ms
    rapport_c = temps_c_ms / temps_a_ms
    print(f"{'fonction_b':<15} {temps_b_ms:<15.4f} {rapport_b:.2f}x")
    print(f"{'fonction_c':<15} {temps_c_ms:<15.4f} {rapport_c:.2f}x")
    
    # Identifier la plus rapide et la plus lente
    resultats = {
        'fonction_a': temps_a_ms,
        'fonction_b': temps_b_ms,
        'fonction_c': temps_c_ms
    }
    
    plus_rapide = min(resultats.items(), key=lambda x: x[1])
    plus_lente = max(resultats.items(), key=lambda x: x[1])
    
    print(f"\nPlus rapide : {plus_rapide[0]} ({plus_rapide[1]:.4f} ms)")
    print(f"Plus lente  : {plus_lente[0]} ({plus_lente[1]:.4f} ms)")
```

**Explication de la solution :**
Cette solution compare trois implémentations différentes du même calcul. `timeit` permet d'obtenir des mesures précises et reproductibles.

---

### Exercice 2 : Profiling d'une application

**Difficulté** : ⭐⭐ Moyen  
**Temps estimé** : 30-40 minutes  
**Objectif** : Utiliser cProfile pour identifier les goulots d'étranglement

**Énoncé :**
Créez un programme qui :
1. Simule le traitement d'une liste de clients (calcul de factures)
2. Utilise `cProfile` pour profiler l'application
3. Analyse les résultats et identifie les 3 fonctions les plus lentes
4. Propose des optimisations basées sur les résultats

**Consignes :**
- Créez au moins 5 fonctions différentes
- Utilisez `pstats` pour analyser les résultats
- Affichez un rapport formaté

**Solution :**

```python
import cProfile
import pstats
import io

class Client:
    def __init__(self, nom, achats):
        self.nom = nom
        self.achats = achats

def calculer_tva(montant):
    """Calcule la TVA (20%)."""
    time.sleep(0.001)  # Simule un calcul
    return montant * 0.20

def calculer_remise(montant_total):
    """Calcule une remise basée sur le montant."""
    time.sleep(0.002)  # Simule un calcul plus long
    if montant_total > 1000:
        return montant_total * 0.10
    elif montant_total > 500:
        return montant_total * 0.05
    return 0

def traiter_achat(achat):
    """Traite un achat individuel."""
    time.sleep(0.0005)
    tva = calculer_tva(achat)
    return achat + tva

def calculer_facture(client):
    """Calcule la facture totale pour un client."""
    total = 0
    for achat in client.achats:
        total += traiter_achat(achat)
    
    remise = calculer_remise(total)
    return total - remise

def traiter_clients(clients):
    """Traite une liste de clients."""
    factures = []
    for client in clients:
        facture = calculer_facture(client)
        factures.append((client.nom, facture))
    return factures

if __name__ == "__main__":
    import time
    
    # Créer des clients de test
    clients = [
        Client("Alice", [100, 200, 300]),
        Client("Bob", [500, 600]),
        Client("Charlie", [50, 75, 100, 150])
    ] * 100  # Multiplier pour avoir plus de données
    
    # Profiler
    profiler = cProfile.Profile()
    profiler.enable()
    
    resultats = traiter_clients(clients)
    
    profiler.disable()
    
    # Analyser
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    print(s.getvalue())
    
    # Identifier les 3 plus lentes
    stats.sort_stats('tottime')
    print("\n=== Top 3 des fonctions les plus lentes (temps total) ===\n")
    stats.print_stats(3)
```

**Explication de la solution :**
Cette solution montre comment utiliser `cProfile` sur une application plus complexe et comment analyser les résultats pour identifier les optimisations prioritaires.

---

### Exercice 3 : Outil de benchmarking

**Difficulté** : ⭐⭐⭐ Avancé  
**Temps estimé** : 45-60 minutes  
**Objectif** : Créer un outil réutilisable pour mesurer les performances

**Énoncé :**
Créez une classe `Benchmark` qui :
1. Permet de mesurer facilement plusieurs fonctions
2. Répète les mesures plusieurs fois et calcule des statistiques (moyenne, min, max, écart-type)
3. Affiche les résultats sous forme de tableau comparatif
4. Peut exporter les résultats en CSV

**Consignes :**
- Utilisez `timeit` pour les mesures
- Calculez les statistiques avec le module `statistics`
- Créez une méthode pour exporter en CSV

**Solution :**

```python
import timeit
import statistics
import csv
from typing import Callable, List, Dict, Any

class Benchmark:
    """Classe pour mesurer et comparer les performances de fonctions."""
    
    def __init__(self, nb_iterations=1000):
        """
        Initialise le benchmark.
        
        Args:
            nb_iterations (int): Nombre d'itérations par mesure
        """
        self.nb_iterations = nb_iterations
        self.resultats = {}
    
    def mesurer(self, nom: str, fonction: Callable, *args, **kwargs):
        """
        Mesure une fonction.
        
        Args:
            nom (str): Nom de la fonction (pour l'identifier)
            fonction (Callable): Fonction à mesurer
            *args, **kwargs: Arguments à passer à la fonction
        """
        # Créer le code à exécuter
        if args or kwargs:
            code = f"fonction({', '.join(map(str, args))})"
        else:
            code = "fonction()"
        
        # Mesurer plusieurs fois pour avoir des statistiques
        temps_liste = []
        for _ in range(10):  # 10 mesures
            temps = timeit.timeit(code, 
                                globals={'fonction': lambda: fonction(*args, **kwargs)},
                                number=self.nb_iterations)
            temps_liste.append(temps / self.nb_iterations)
        
        # Calculer les statistiques
        self.resultats[nom] = {
            'moyenne': statistics.mean(temps_liste),
            'min': min(temps_liste),
            'max': max(temps_liste),
            'ecart_type': statistics.stdev(temps_liste) if len(temps_liste) > 1 else 0
        }
    
    def afficher_resultats(self):
        """Affiche les résultats sous forme de tableau."""
        if not self.resultats:
            print("Aucun résultat à afficher.")
            return
        
        print("\n=== Résultats du Benchmark ===\n")
        print(f"{'Fonction':<20} {'Moyenne (s)':<15} {'Min (s)':<15} {'Max (s)':<15} {'Écart-type':<15}")
        print("-" * 80)
        
        # Trier par temps moyen
        resultats_tries = sorted(self.resultats.items(), 
                               key=lambda x: x[1]['moyenne'])
        
        temps_reference = resultats_tries[0][1]['moyenne']
        
        for nom, stats in resultats_tries:
            rapport = stats['moyenne'] / temps_reference
            print(f"{nom:<20} {stats['moyenne']:<15.6f} {stats['min']:<15.6f} "
                  f"{stats['max']:<15.6f} {stats['ecart_type']:<15.6f} "
                  f"({rapport:.2f}x)")
    
    def exporter_csv(self, nom_fichier='benchmark_results.csv'):
        """Exporte les résultats en CSV."""
        with open(nom_fichier, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Fonction', 'Moyenne (s)', 'Min (s)', 'Max (s)', 'Écart-type'])
            
            for nom, stats in sorted(self.resultats.items(), 
                                   key=lambda x: x[1]['moyenne']):
                writer.writerow([
                    nom,
                    stats['moyenne'],
                    stats['min'],
                    stats['max'],
                    stats['ecart_type']
                ])
        
        print(f"\nRésultats exportés dans {nom_fichier}")

# Exemple d'utilisation
if __name__ == "__main__":
    def fonction_rapide(n):
        return sum(range(n))
    
    def fonction_moyenne(n):
        return sum(i*i for i in range(n))
    
    def fonction_lente(n):
        resultat = 0
        for i in range(n):
            for j in range(10):
                resultat += i * j
        return resultat
    
    benchmark = Benchmark(nb_iterations=100)
    
    n = 1000
    benchmark.mesurer("Fonction rapide", fonction_rapide, n)
    benchmark.mesurer("Fonction moyenne", fonction_moyenne, n)
    benchmark.mesurer("Fonction lente", fonction_lente, n)
    
    benchmark.afficher_resultats()
    benchmark.exporter_csv()
```

**Explication de la solution :**
Cette solution crée un outil réutilisable pour le benchmarking. La classe `Benchmark` encapsule toute la logique de mesure et d'analyse, rendant le code plus propre et réutilisable.

---

## 5. Résumé

### Concepts clés
- ✅ **time.time()** : Mesure simple du temps d'exécution
- ✅ **timeit** : Module spécialisé pour des mesures précises et reproductibles
- ✅ **cProfile** : Profiler intégré à Python pour identifier les goulots d'étranglement
- ✅ **pstats** : Module pour analyser et trier les résultats du profiler

### Points importants à retenir
1. Toujours mesurer avant d'optimiser - ne devinez pas où sont les problèmes
2. Utilisez `timeit` pour des mesures précises de petites fonctions
3. Utilisez `cProfile` pour analyser des programmes complets
4. Répétez les mesures plusieurs fois pour obtenir des statistiques fiables
5. Visualisez les résultats pour mieux les comprendre

### Pièges à éviter
- ⚠️ **Mesurer une seule fois** : Les variations du système peuvent fausser les résultats
- ⚠️ **Optimiser sans profiler** : Vous pourriez optimiser la mauvaise partie du code
- ⚠️ **Ignorer l'overhead** : Le temps de création des processus/threads peut masquer les gains

---

## 6. Pour aller plus loin

### Ressources supplémentaires
- 📚 Documentation timeit : https://docs.python.org/3/library/timeit.html
- 📚 Documentation cProfile : https://docs.python.org/3/library/profile.html
- 📚 SnakeViz : Outil de visualisation interactive pour cProfile
- 📚 line_profiler : Profiler ligne par ligne pour identifier les lignes lentes

### Concepts liés à explorer
- **Memory profiling** : Analyser l'utilisation de la mémoire
- **Visualisation avec matplotlib** : Créer des graphiques de performance
- **Intégration continue** : Intégrer le benchmarking dans les tests

### Projets suggérés
- Créer un framework de benchmarking réutilisable
- Développer un outil de visualisation des profils de performance
- Intégrer le profiling dans un pipeline CI/CD

---

## 7. Questions de révision

1. Quelle est la différence entre `time.time()` et `timeit.timeit()` ?
2. Pourquoi est-il important de répéter les mesures plusieurs fois ?
3. Qu'est-ce qu'un "goulot d'étranglement" et comment le profiler l'identifie-t-il ?
4. Dans quels cas utiliseriez-vous `cProfile` plutôt que `timeit` ?
5. Comment interpréter les colonnes `tottime` et `cumtime` dans le rapport de cProfile ?

---

*[Chapitre précédent : Chapitre 1 - Introduction] | [Chapitre suivant : Chapitre 3 - Concepts fondamentaux]*
