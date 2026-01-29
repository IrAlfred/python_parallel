# Chapitre 1 : Introduction à la programmation parallèle et distribuée

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Comprendre la différence entre programmation séquentielle, parallèle et distribuée
- Identifier les situations où la programmation parallèle est bénéfique
- Comprendre les limitations de la programmation séquentielle
- Connaître les concepts de base de l'architecture des processeurs modernes
- Comprendre le GIL (Global Interpreter Lock) en Python et ses implications

---

## 1. Explication du principe

### 1.1 Programmation séquentielle vs parallèle vs distribuée

**Programmation séquentielle** :
La programmation séquentielle est la méthode traditionnelle où les instructions sont exécutées une après l'autre, dans l'ordre. C'est comme avoir un seul ouvrier qui fait toutes les tâches une par une.

```python
# Exemple séquentiel
resultat1 = calcul_complexe_1()  # Prend 5 secondes
resultat2 = calcul_complexe_2()  # Prend 5 secondes
resultat3 = calcul_complexe_3()  # Prend 5 secondes
# Temps total : 15 secondes
```

**Programmation parallèle** :
La programmation parallèle consiste à exécuter plusieurs tâches simultanément sur plusieurs cœurs d'un même processeur ou sur plusieurs processeurs d'une même machine. C'est comme avoir plusieurs ouvriers travaillant en même temps sur la même chaîne de production.

```python
# Exemple parallèle (conceptuel)
# Tâche 1, 2 et 3 s'exécutent en même temps
# Temps total : ~5 secondes (le temps de la plus longue tâche)
```

**Programmation distribuée** :
La programmation distribuée consiste à exécuter des tâches sur plusieurs machines différentes connectées par un réseau. C'est comme avoir plusieurs usines dans différentes villes qui travaillent ensemble.

**Points clés à retenir :**
- **Séquentiel** : Une tâche à la fois, sur une seule machine
- **Parallèle** : Plusieurs tâches simultanées, sur une seule machine (plusieurs cœurs)
- **Distribué** : Plusieurs tâches simultanées, sur plusieurs machines

### 1.2 Pourquoi la programmation parallèle ?

**Limitations physiques des processeurs** :
Depuis les années 2000, les fabricants de processeurs ont rencontré des limites physiques qui empêchent d'augmenter indéfiniment la fréquence d'horloge (vitesse) d'un processeur. Au lieu de créer des processeurs plus rapides, ils créent des processeurs avec plusieurs cœurs.

**Avantages de la programmation parallèle :**
1. **Performance** : Réduction significative du temps d'exécution pour les tâches qui peuvent être divisées
2. **Utilisation des ressources** : Meilleure utilisation des multiples cœurs disponibles
3. **Réactivité** : Permet de maintenir une interface utilisateur réactive pendant qu'un calcul s'exécute en arrière-plan
4. **Scalabilité** : Possibilité d'ajouter plus de ressources pour traiter plus de données

**Quand utiliser la programmation parallèle ?**
- Traitement de grandes quantités de données
- Calculs indépendants qui peuvent être exécutés simultanément
- Opérations I/O (lecture/écriture de fichiers, requêtes réseau) qui attendent souvent
- Simulations complexes avec de nombreux calculs indépendants

**Quand NE PAS utiliser la programmation parallèle ?**
- Tâches très simples et rapides (le coût de création des threads/processus dépasse le gain)
- Tâches qui dépendent fortement les unes des autres (séquentielles par nature)
- Quand la synchronisation devient trop complexe

### 1.3 Architecture des processeurs modernes

**Cœurs de processeur** :
Un cœur (core) est une unité de traitement indépendante capable d'exécuter des instructions. Les processeurs modernes ont généralement 4, 8, 16 cœurs ou plus.

**Threads matériels (Hyper-Threading)** :
Certains processeurs supportent plusieurs threads par cœur (Intel Hyper-Threading, AMD SMT). Un processeur 4 cœurs avec 2 threads par cœur peut exécuter 8 threads simultanément.

**Mémoire** :
- **RAM** : Mémoire partagée accessible par tous les cœurs
- **Cache** : Mémoire très rapide proche de chaque cœur (L1, L2, L3)

**Points clés à retenir :**
- Plus de cœurs = plus de tâches peuvent s'exécuter simultanément
- La mémoire est partagée entre tous les cœurs
- Le cache permet d'accéder rapidement aux données fréquemment utilisées

### 1.4 Le GIL (Global Interpreter Lock) en Python

**Qu'est-ce que le GIL ?**
Le GIL est un mécanisme dans l'implémentation CPython de Python qui permet à un seul thread d'exécuter du code Python à la fois. C'est un verrou global qui protège l'accès aux objets Python.

**Pourquoi le GIL existe-t-il ?**
- Simplifie la gestion de la mémoire (garbage collector)
- Protège les structures de données internes de Python
- Rend l'implémentation de CPython plus simple et plus sûre

**Implications du GIL :**
- **Threading** : Les threads Python ne peuvent pas vraiment exécuter du code Python en parallèle sur plusieurs cœurs
- **Multiprocessing** : Les processus Python peuvent s'exécuter en parallèle car chaque processus a son propre GIL
- **I/O** : Le GIL est libéré pendant les opérations I/O, donc le threading est efficace pour les opérations de fichiers/réseau

**Quand le GIL est-il libéré ?**
- Pendant les opérations I/O (lecture/écriture fichiers, requêtes réseau)
- Dans certaines opérations C natives (NumPy, certaines fonctions de la bibliothèque standard)
- Explicitement par certaines extensions C

**Points clés à retenir :**
- Le GIL limite le parallélisme réel avec les threads pour le calcul CPU
- Pour le calcul CPU intensif, utilisez `multiprocessing` plutôt que `threading`
- Pour les opérations I/O, `threading` fonctionne bien malgré le GIL

### 1.5 La loi d'Amdahl

**Qu'est-ce que la loi d'Amdahl ?**
La loi d'Amdahl est une formule qui permet de calculer l'accélération maximale théorique d'un programme lorsqu'on utilise la programmation parallèle. Elle a été formulée par Gene Amdahl en 1967 et reste fondamentale pour comprendre les limites du parallélisme.

**Le principe fondamental :**
La loi d'Amdahl part d'une observation simple : tout programme comporte une partie qui peut être parallélisée et une partie qui doit rester séquentielle. L'accélération maximale est limitée par cette partie séquentielle.

**La formule mathématique :**

L'accélération théorique maximale $S$ avec $N$ processeurs est donnée par :

$$S(N) = \frac{1}{(1-P) + \frac{P}{N}}$$

Où :
- $S(N)$ : Accélération avec $N$ processeurs
- $P$ : Proportion du programme qui peut être parallélisée (entre 0 et 1)
- $1-P$ : Proportion du programme qui doit rester séquentielle
- $N$ : Nombre de processeurs

**Interprétation :**
- Si $P = 1$ (100% parallélisable) : $S(N) = N$ (accélération linéaire parfaite)
- Si $P = 0$ (0% parallélisable) : $S(N) = 1$ (aucune accélération)
- Dans la réalité : $0 < P < 1$ (accélération limitée par la partie séquentielle)

**Accélération maximale théorique :**
Quand $N \to \infty$ (nombre infini de processeurs), l'accélération maximale est :

$$S_{max} = \frac{1}{1-P}$$

Cela signifie que même avec un nombre infini de processeurs, on ne peut pas dépasser cette limite imposée par la partie séquentielle.

**Exemples pratiques de calculs :**

**Exemple 1 : Programme 90% parallélisable**

Supposons un programme où 90% du code peut être parallélisé ($P = 0.9$) :

```python
def calculer_acceleration_amdahl(P, N):
    """
    Calcule l'accélération théorique selon la loi d'Amdahl.
    
    Args:
        P (float): Proportion parallélisable (entre 0 et 1)
        N (int): Nombre de processeurs
    
    Returns:
        float: Accélération théorique
    """
    return 1 / ((1 - P) + P / N)

# Programme 90% parallélisable
P = 0.9

# Calculer pour différents nombres de processeurs
print("Programme 90% parallélisable:")
print(f"{'Processeurs':<15} {'Accélération':<15} {'Efficacité':<15}")
print("-" * 45)

for N in [1, 2, 4, 8, 16, 32, 64, 128]:
    S = calculer_acceleration_amdahl(P, N)
    efficacite = (S / N) * 100
    print(f"{N:<15} {S:<15.2f} {efficacite:<15.1f}%")

# Accélération maximale théorique
S_max = 1 / (1 - P)
print(f"\nAccélération maximale théorique : {S_max:.2f}x")
```

**Résultat attendu :**
```
Programme 90% parallélisable:
Processeurs     Accélération    Efficacité     
---------------------------------------------
1               1.00            100.0%
2               1.82            90.9%
4               3.08            76.9%
8               4.71            58.8%
16              6.40            40.0%
32              7.80            24.4%
64              8.77            13.7%
128             9.30            7.3%

Accélération maximale théorique : 10.00x
```

**Analyse :**
- Avec 2 processeurs : accélération de 1.82x (pas 2x !)
- Avec 8 processeurs : accélération de 4.71x (pas 8x !)
- Même avec 128 processeurs, on atteint seulement 9.30x
- La limite maximale est 10x, peu importe le nombre de processeurs

**Exemple 2 : Comparaison de différents taux de parallélisation**

```python
import matplotlib.pyplot as plt  # Pour la visualisation (optionnel)

def analyser_impact_parallelisation():
    """Analyse l'impact du taux de parallélisation sur l'accélération."""
    
    # Différents taux de parallélisation
    taux_P = [0.50, 0.75, 0.90, 0.95, 0.99]
    nombre_processeurs = range(1, 65)
    
    print("=== Impact du taux de parallélisation ===\n")
    
    for P in taux_P:
        print(f"\nProgramme {int(P*100)}% parallélisable:")
        print(f"{'Processeurs':<15} {'Accélération':<15} {'% du maximum':<15}")
        print("-" * 45)
        
        S_max = 1 / (1 - P)
        
        for N in [1, 4, 8, 16, 32, 64]:
            S = calculer_acceleration_amdahl(P, N)
            pourcentage_max = (S / S_max) * 100
            print(f"{N:<15} {S:<15.2f} {pourcentage_max:<15.1f}%")
        
        print(f"Limite maximale : {S_max:.2f}x")

if __name__ == "__main__":
    analyser_impact_parallelisation()
```

**Résultat attendu :**
```
=== Impact du taux de parallélisation ===

Programme 50% parallélisable:
Processeurs     Accélération    % du maximum   
---------------------------------------------
1               1.00            50.0%
4               1.60            80.0%
8               1.78            88.9%
16              1.88            94.1%
32              1.94            96.9%
64              1.97            98.4%
Limite maximale : 2.00x

Programme 75% parallélisable:
Processeurs     Accélération    % du maximum   
---------------------------------------------
1               1.00            25.0%
4               2.29            57.1%
8               2.91            72.7%
16              3.37            84.2%
32              3.64            91.0%
64              3.80            95.0%
Limite maximale : 4.00x

Programme 90% parallélisable:
Processeurs     Accélération    % du maximum   
---------------------------------------------
1               1.00            10.0%
4               3.08            30.8%
8               4.71            47.1%
16              6.40            64.0%
32              7.80            78.0%
64              8.77            87.7%
Limite maximale : 10.00x

Programme 95% parallélisable:
Processeurs     Accélération    % du maximum   
---------------------------------------------
1               1.00            5.0%
4               3.48            17.4%
8               5.93            29.6%
16              9.14            45.7%
32              12.80           64.0%
64              15.53           77.6%
Limite maximale : 20.00x

Programme 99% parallélisable:
Processeurs     Accélération    % du maximum   
---------------------------------------------
1               1.00            1.0%
4               3.88            3.9%
8               7.48            7.5%
16              13.91           13.9%
32              24.43           24.4%
64              39.68           39.7%
Limite maximale : 100.00x
```

**Observations importantes :**
1. **Impact de la partie séquentielle** : Même 10% de code séquentiel ($P=0.9$) limite l'accélération à 10x
2. **Rendements décroissants** : Plus on ajoute de processeurs, moins le gain est important
3. **Importance de la parallélisation** : Passer de 90% à 95% de parallélisation double la limite théorique

**Exemple 3 : Calcul pratique pour un cas réel**

```python
def analyser_tache_reelle():
    """
    Analyse une tâche réelle avec ses temps mesurés.
    """
    print("=== Analyse d'une tâche réelle ===\n")
    
    # Mesures d'un programme réel (en secondes)
    temps_total_sequentiel = 100  # 100 secondes au total
    temps_partie_sequentielle = 15  # 15 secondes incompressibles
    temps_partie_parallelisable = 85  # 85 secondes parallélisables
    
    # Calculer P
    P = temps_partie_parallelisable / temps_total_sequentiel
    
    print(f"Temps total séquentiel : {temps_total_sequentiel}s")
    print(f"Partie séquentielle : {temps_partie_sequentielle}s ({(1-P)*100:.0f}%)")
    print(f"Partie parallélisable : {temps_partie_parallelisable}s ({P*100:.0f}%)")
    print(f"\nP = {P:.2f}\n")
    
    print(f"{'Processeurs':<15} {'Temps théorique':<20} {'Accélération':<15}")
    print("-" * 50)
    
    for N in [1, 2, 4, 8, 16]:
        S = calculer_acceleration_amdahl(P, N)
        temps_predit = temps_total_sequentiel / S
        print(f"{N:<15} {temps_predit:<20.2f}s {S:<15.2f}x")
    
    # Limite maximale
    S_max = 1 / (1 - P)
    temps_min = temps_total_sequentiel / S_max
    print(f"\n{'∞':<15} {temps_min:<20.2f}s {S_max:<15.2f}x (maximum)")
    print(f"\nTemps incompressible : {temps_partie_sequentielle}s")

if __name__ == "__main__":
    analyser_tache_reelle()
```

**Résultat attendu :**
```
=== Analyse d'une tâche réelle ===

Temps total séquentiel : 100s
Partie séquentielle : 15s (15%)
Partie parallélisable : 85s (85%)

P = 0.85

Processeurs     Temps théorique     Accélération   
--------------------------------------------------
1               100.00s             1.00x
2               57.50s              1.74x
4               36.25s              2.76x
8               25.63s              3.90x
16              20.31s              4.92x

∞               15.00s              6.67x (maximum)

Temps incompressible : 15s
```

**Interprétation pratique :**
- Même avec un nombre infini de processeurs, on ne pourra jamais descendre sous 15 secondes
- Avec 4 processeurs, on économise environ 64 secondes
- Avec 16 processeurs, on économise 80 secondes, mais le gain diminue
- Au-delà de 16 processeurs, le gain devient marginal pour cette tâche

**Limites de la loi d'Amdahl :**
1. **Overhead non pris en compte** : La loi suppose que la partie parallélisable s'accélère parfaitement, sans coût de communication ou synchronisation
2. **Taille fixe du problème** : La loi suppose que la taille du problème reste constante (voir la loi de Gustafson pour une approche alternative)
3. **Modèle simplifié** : En réalité, certaines parties peuvent avoir des comportements plus complexes

**Conseils pratiques basés sur la loi d'Amdahl :**
1. **Identifier la partie séquentielle** : Avant de paralléliser, mesurez quelle proportion de votre code peut vraiment être parallélisée
2. **Calculer le nombre optimal de processeurs** : Inutile d'utiliser 64 processeurs si votre tâche est limitée à 4x d'accélération
3. **Optimiser d'abord le séquentiel** : Réduire la partie séquentielle a plus d'impact que d'ajouter des processeurs
4. **Mesurer les résultats réels** : Comparez vos mesures avec les prédictions d'Amdahl pour identifier les problèmes

**Points clés à retenir :**
- La loi d'Amdahl prédit l'accélération maximale théorique en fonction de la proportion parallélisable
- Même une petite partie séquentielle limite drastiquement l'accélération maximale
- Il existe un point de rendement décroissant au-delà duquel ajouter des processeurs n'apporte presque rien
- Optimiser la partie séquentielle est souvent plus efficace que d'ajouter des ressources

---

## 2. Exemples basiques

### 2.1 Exemple basique 1 : Comparaison séquentiel vs parallèle

#### 2.1.1 Description

Nous allons créer un exemple simple qui compare l'exécution séquentielle et parallèle d'une tâche de calcul. Cet exemple illustrera la différence de temps d'exécution entre les deux approches.

**Ce que nous allons faire :**
- Créer une fonction qui simule un calcul (somme de nombres)
- Exécuter cette fonction plusieurs fois de manière séquentielle
- Exécuter cette fonction plusieurs fois de manière parallèle (avec multiprocessing)
- Comparer les temps d'exécution

#### 2.1.2 Code

```python
import time
from multiprocessing import Process

def calcul_intensif(n):
    """
    Simule un calcul intensif en calculant la somme des nombres de 0 à n.
    
    Args:
        n (int): Nombre jusqu'auquel calculer la somme
    
    Returns:
        int: La somme calculée
    """
    somme = 0
    for i in range(n):
        somme += i
    return somme

def execution_sequentielle(taches):
    """
    Exécute les tâches de manière séquentielle (une après l'autre).
    
    Args:
        taches (list): Liste des valeurs à traiter
    
    Returns:
        float: Temps d'exécution en secondes
    """
    debut = time.time()
    resultats = []
    for tache in taches:
        resultat = calcul_intensif(tache)
        resultats.append(resultat)
    fin = time.time()
    return fin - debut

def execution_parallele(taches):
    """
    Exécute les tâches de manière parallèle (simultanément).
    
    Args:
        taches (list): Liste des valeurs à traiter
    
    Returns:
        float: Temps d'exécution en secondes
    """
    debut = time.time()
    processus = []
    
    # Créer un processus pour chaque tâche
    for tache in taches:
        p = Process(target=calcul_intensif, args=(tache,))
        processus.append(p)
        p.start()
    
    # Attendre que tous les processus se terminent
    for p in processus:
        p.join()
    
    fin = time.time()
    return fin - debut

if __name__ == "__main__":
    # Définir les tâches à exécuter
    # Chaque nombre représente la complexité d'un calcul
    taches = [10000000, 10000000, 10000000, 10000000]
    
    print("=== Comparaison Séquentiel vs Parallèle ===\n")
    
    # Exécution séquentielle
    print("Exécution séquentielle en cours...")
    temps_sequentiel = execution_sequentielle(taches)
    print(f"Temps séquentiel : {temps_sequentiel:.4f} secondes\n")
    
    # Exécution parallèle
    print("Exécution parallèle en cours...")
    temps_parallele = execution_parallele(taches)
    print(f"Temps parallèle : {temps_parallele:.4f} secondes\n")
    
    # Comparaison
    acceleration = temps_sequentiel / temps_parallele
    print(f"Accélération : {acceleration:.2f}x")
    print(f"Gain de temps : {temps_sequentiel - temps_parallele:.4f} secondes")
```

#### 2.1.3 Explication ligne par ligne

**Lignes 1-2 : Importations**
- `time` : Pour mesurer le temps d'exécution
- `Process` : Classe du module `multiprocessing` pour créer des processus

**Lignes 4-15 : Fonction `calcul_intensif`**
- Simule un calcul qui prend du temps en faisant une boucle
- Cette fonction sera exécutée plusieurs fois
- Plus `n` est grand, plus le calcul prend du temps

**Lignes 17-30 : Fonction `execution_sequentielle`**
- `debut = time.time()` : Enregistre le temps de début
- La boucle `for` exécute chaque tâche une après l'autre
- `fin = time.time()` : Enregistre le temps de fin
- Retourne la différence (temps total)

**Lignes 32-52 : Fonction `execution_parallele`**
- `debut = time.time()` : Enregistre le temps de début
- `Process(target=calcul_intensif, args=(tache,))` : Crée un nouveau processus qui exécutera `calcul_intensif` avec `tache` comme argument
- `p.start()` : Démarre le processus (il commence à s'exécuter)
- `p.join()` : Attend que le processus se termine avant de continuer
- Tous les processus s'exécutent en parallèle (simultanément)

**Lignes 54-75 : Code principal**
- Définit 4 tâches identiques
- Exécute d'abord de manière séquentielle, puis parallèle
- Compare les résultats

#### 2.1.4 Résultat attendu

```
=== Comparaison Séquentiel vs Parallèle ===

Exécution séquentielle en cours...
Temps séquentiel : 2.3456 secondes

Exécution parallèle en cours...
Temps parallèle : 0.6789 secondes

Accélération : 3.46x
Gain de temps : 1.6667 secondes
```

*Note : Les temps exacts varieront selon votre machine, mais vous devriez voir une accélération significative avec l'exécution parallèle.*

#### 2.1.5 Analyse du résultat

Le résultat montre que l'exécution parallèle est plus rapide que l'exécution séquentielle. Sur une machine avec 4 cœurs, on peut s'attendre à une accélération proche de 4x (idéalement). En pratique, l'accélération est souvent inférieure à cause de :
- Le temps de création des processus
- Le temps de communication entre processus
- La charge du système

---

### 2.2 Exemple basique 2 : Utilisation de plusieurs cœurs

#### 2.2.1 Description

Cet exemple montre comment vérifier le nombre de cœurs disponibles sur votre machine et utiliser ce nombre pour optimiser le parallélisme.

**Ce que nous allons faire :**
- Détecter le nombre de cœurs CPU disponibles
- Créer un nombre optimal de processus
- Comparer les performances avec différents nombres de processus

#### 2.2.2 Code

```python
import time
import os
from multiprocessing import Process, cpu_count

def calcul_simple(n):
    """Effectue un calcul simple."""
    resultat = 0
    for i in range(n):
        resultat += i * i
    return resultat

def executer_avec_n_processus(nb_processus, taches):
    """Exécute les tâches avec un nombre spécifié de processus."""
    debut = time.time()
    processus = []
    
    for tache in taches:
        p = Process(target=calcul_simple, args=(tache,))
        processus.append(p)
        p.start()
    
    for p in processus:
        p.join()
    
    fin = time.time()
    return fin - debut

if __name__ == "__main__":
    # Détecter le nombre de cœurs
    nb_coeurs = cpu_count()
    print(f"Nombre de cœurs CPU disponibles : {nb_coeurs}\n")
    
    taches = [5000000] * 8  # 8 tâches identiques
    
    # Tester avec différents nombres de processus
    for nb_proc in [1, 2, 4, nb_coeurs, nb_coeurs * 2]:
        if nb_proc <= len(taches):
            temps = executer_avec_n_processus(nb_proc, taches[:nb_proc])
            print(f"{nb_proc} processus : {temps:.4f} secondes")
```

#### 2.2.3 Explication

- `cpu_count()` : Retourne le nombre de cœurs CPU disponibles
- On teste différents nombres de processus pour voir l'impact
- Généralement, le nombre optimal est proche du nombre de cœurs

#### 2.2.4 Résultat attendu

```
Nombre de cœurs CPU disponibles : 4

1 processus : 2.1234 secondes
2 processus : 1.2345 secondes
4 processus : 0.6789 secondes
4 processus : 0.7123 secondes
8 processus : 0.8901 secondes
```

---

### 2.3 Exemple basique 3 : Mesure de performance simple

#### 2.3.1 Description

Cet exemple montre comment mesurer et comparer les performances de manière simple et reproductible.

**Ce que nous allons faire :**
- Créer une fonction de calcul
- Mesurer le temps d'exécution séquentiel
- Mesurer le temps d'exécution parallèle
- Afficher un rapport de performance

#### 2.3.2 Code

```python
import time
from multiprocessing import Process

def factorielle(n):
    """Calcule la factorielle de n."""
    if n <= 1:
        return 1
    resultat = 1
    for i in range(2, n + 1):
        resultat *= i
    return resultat

def test_sequentiel():
    """Test séquentiel."""
    debut = time.time()
    resultats = []
    for n in [1000, 2000, 3000, 4000]:
        resultats.append(factorielle(n))
    return time.time() - debut, resultats

def test_parallele():
    """Test parallèle."""
    debut = time.time()
    processus = []
    resultats = [None] * 4
    
    def worker(index, valeur):
        resultats[index] = factorielle(valeur)
    
    valeurs = [1000, 2000, 3000, 4000]
    for i, val in enumerate(valeurs):
        p = Process(target=worker, args=(i, val))
        processus.append(p)
        p.start()
    
    for p in processus:
        p.join()
    
    return time.time() - debut, resultats

if __name__ == "__main__":
    print("=== Test de Performance ===\n")
    
    temps_seq, res_seq = test_sequentiel()
    print(f"Temps séquentiel : {temps_seq:.4f}s")
    
    temps_par, res_par = test_parallele()
    print(f"Temps parallèle : {temps_par:.4f}s")
    
    acceleration = temps_seq / temps_par
    print(f"\nAccélération : {acceleration:.2f}x")
    print(f"Gain : {temps_seq - temps_par:.4f} secondes")
```

#### 2.3.3 Explication

- On mesure le temps pour chaque approche
- On calcule l'accélération obtenue
- On compare les résultats pour vérifier qu'ils sont identiques

#### 2.3.4 Résultat attendu

```
=== Test de Performance ===

Temps séquentiel : 1.2345s
Temps parallèle : 0.3456s

Accélération : 3.57x
Gain : 0.8889 secondes
```

---

## 3. Exemple avancé

### 3.1 Description

Nous allons créer un exemple plus réaliste qui traite des fichiers en parallèle. Cet exemple simule un scénario où nous devons analyser plusieurs fichiers texte pour compter les mots. C'est un cas d'usage typique où la programmation parallèle apporte un réel bénéfice.

**Contexte :**
Imaginez que vous avez 10 fichiers texte volumineux et que vous voulez compter le nombre de mots dans chacun d'eux. Au lieu de les traiter un par un, nous allons les traiter en parallèle.

**Objectifs :**
- Créer des fichiers texte de test
- Traiter les fichiers de manière séquentielle
- Traiter les fichiers de manière parallèle
- Comparer les performances et afficher les résultats

### 3.2 Code

```python
import time
import os
from multiprocessing import Process, Queue
import random
import string

def generer_fichier_test(nom_fichier, nb_mots=100000):
    """
    Génère un fichier texte de test avec un nombre spécifié de mots.
    
    Args:
        nom_fichier (str): Nom du fichier à créer
        nb_mots (int): Nombre de mots à générer
    """
    mots = []
    for _ in range(nb_mots):
        # Génère un mot aléatoire de 3 à 10 caractères
        longueur = random.randint(3, 10)
        mot = ''.join(random.choices(string.ascii_lowercase, k=longueur))
        mots.append(mot)
    
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        f.write(' '.join(mots))

def compter_mots(nom_fichier):
    """
    Compte le nombre de mots dans un fichier.
    
    Args:
        nom_fichier (str): Chemin vers le fichier
    
    Returns:
        tuple: (nom_fichier, nombre_de_mots)
    """
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            mots = contenu.split()
            return (nom_fichier, len(mots))
    except Exception as e:
        return (nom_fichier, f"Erreur: {e}")

def traitement_sequentiel(fichiers):
    """
    Traite les fichiers de manière séquentielle.
    
    Args:
        fichiers (list): Liste des chemins de fichiers
    
    Returns:
        dict: Dictionnaire {nom_fichier: nombre_mots}
    """
    debut = time.time()
    resultats = {}
    
    for fichier in fichiers:
        nom, nb_mots = compter_mots(fichier)
        resultats[nom] = nb_mots
    
    fin = time.time()
    return resultats, fin - debut

def worker_traitement(fichiers, queue_resultats):
    """
    Fonction exécutée par chaque processus worker.
    Traite une liste de fichiers et met les résultats dans la queue.
    
    Args:
        fichiers (list): Liste des fichiers à traiter
        queue_resultats (Queue): Queue pour partager les résultats
    """
    for fichier in fichiers:
        nom, nb_mots = compter_mots(fichier)
        queue_resultats.put((nom, nb_mots))

def traitement_parallele(fichiers, nb_processus=4):
    """
    Traite les fichiers de manière parallèle en utilisant plusieurs processus.
    
    Args:
        fichiers (list): Liste des chemins de fichiers
        nb_processus (int): Nombre de processus à utiliser
    
    Returns:
        dict: Dictionnaire {nom_fichier: nombre_mots}
    """
    debut = time.time()
    
    # Diviser les fichiers entre les processus
    fichiers_par_processus = []
    for i in range(nb_processus):
        fichiers_par_processus.append([])
    
    # Répartir les fichiers de manière équitable
    for index, fichier in enumerate(fichiers):
        fichiers_par_processus[index % nb_processus].append(fichier)
    
    # Créer une queue pour collecter les résultats
    queue_resultats = Queue()
    
    # Créer et démarrer les processus
    processus = []
    for fichiers_groupe in fichiers_par_processus:
        if fichiers_groupe:  # Ne créer un processus que s'il y a des fichiers
            p = Process(target=worker_traitement, args=(fichiers_groupe, queue_resultats))
            processus.append(p)
            p.start()
    
    # Attendre que tous les processus se terminent
    for p in processus:
        p.join()
    
    # Collecter les résultats de la queue
    resultats = {}
    while not queue_resultats.empty():
        nom, nb_mots = queue_resultats.get()
        resultats[nom] = nb_mots
    
    fin = time.time()
    return resultats, fin - debut

def nettoyer_fichiers_test(fichiers):
    """Supprime les fichiers de test créés."""
    for fichier in fichiers:
        if os.path.exists(fichier):
            os.remove(fichier)

if __name__ == "__main__":
    # Configuration
    nb_fichiers = 10
    nb_mots_par_fichier = 50000
    nb_processus = 4
    
    print("=== Traitement de fichiers : Séquentiel vs Parallèle ===\n")
    
    # Créer les fichiers de test
    print(f"Création de {nb_fichiers} fichiers de test...")
    fichiers = [f"test_file_{i}.txt" for i in range(nb_fichiers)]
    for fichier in fichiers:
        generer_fichier_test(fichier, nb_mots_par_fichier)
    print("Fichiers créés.\n")
    
    # Traitement séquentiel
    print("Traitement séquentiel en cours...")
    resultats_seq, temps_seq = traitement_sequentiel(fichiers)
    print(f"Temps séquentiel : {temps_seq:.4f} secondes")
    print(f"Total de mots traités : {sum(resultats_seq.values())}\n")
    
    # Traitement parallèle
    print(f"Traitement parallèle en cours ({nb_processus} processus)...")
    resultats_par, temps_par = traitement_parallele(fichiers, nb_processus)
    print(f"Temps parallèle : {temps_par:.4f} secondes")
    print(f"Total de mots traités : {sum(resultats_par.values())}\n")
    
    # Comparaison
    acceleration = temps_seq / temps_par if temps_par > 0 else 0
    print("=== Résultats ===")
    print(f"Accélération : {acceleration:.2f}x")
    print(f"Gain de temps : {temps_seq - temps_par:.4f} secondes")
    print(f"Pourcentage d'amélioration : {((temps_seq - temps_par) / temps_seq * 100):.1f}%")
    
    # Vérifier que les résultats sont identiques
    if resultats_seq == resultats_par:
        print("\n✓ Les résultats sont identiques !")
    else:
        print("\n✗ Attention : Les résultats diffèrent !")
    
    # Nettoyer
    print("\nNettoyage des fichiers de test...")
    nettoyer_fichiers_test(fichiers)
    print("Terminé.")
```

### 3.3 Explication détaillée

**Architecture :**
L'exemple utilise une architecture "worker pool" où plusieurs processus (workers) traitent chacun une partie des fichiers. Les résultats sont collectés via une Queue (file d'attente thread-safe).

**Fonctionnalités :**

1. **Génération de fichiers de test** (`generer_fichier_test`) :
   - Crée des fichiers texte avec un nombre spécifié de mots aléatoires
   - Permet de tester sans avoir de vrais fichiers

2. **Comptage de mots** (`compter_mots`) :
   - Fonction simple qui lit un fichier et compte les mots
   - Gère les erreurs de manière gracieuse

3. **Traitement séquentiel** (`traitement_sequentiel`) :
   - Traite chaque fichier un par un
   - Simple et direct

4. **Traitement parallèle** (`traitement_parallele`) :
   - Divise les fichiers entre plusieurs processus
   - Chaque processus traite sa portion de fichiers
   - Utilise une Queue pour collecter les résultats de manière thread-safe

**Points techniques importants :**

- **Répartition des tâches** : Les fichiers sont répartis de manière équitable entre les processus (round-robin)
- **Queue pour résultats** : La Queue permet de partager les résultats entre processus de manière sûre
- **Gestion des processus** : Tous les processus sont démarrés puis on attend qu'ils se terminent tous

### 3.4 Résultat attendu

```
=== Traitement de fichiers : Séquentiel vs Parallèle ===

Création de 10 fichiers de test...
Fichiers créés.

Traitement séquentiel en cours...
Temps séquentiel : 1.2345 secondes
Total de mots traités : 500000

Traitement parallèle en cours (4 processus)...
Temps parallèle : 0.3456 secondes
Total de mots traités : 500000

=== Résultats ===
Accélération : 3.57x
Gain de temps : 0.8889 secondes
Pourcentage d'amélioration : 72.0%

✓ Les résultats sont identiques !

Nettoyage des fichiers de test...
Terminé.
```

### 3.5 Analyse et améliorations possibles

**Analyse :**
- L'exécution parallèle est significativement plus rapide
- Les résultats sont identiques, ce qui confirme que le parallélisme n'a pas introduit d'erreurs
- L'accélération est proche du nombre de processus (4x idéalement, ~3.5x en pratique)

**Améliorations possibles :**
- Utiliser `Pool` de `multiprocessing` pour simplifier le code
- Ajouter une barre de progression
- Gérer les erreurs de manière plus robuste
- Utiliser `concurrent.futures` pour une API plus moderne

---

## 4. Exercices

### Exercice 1 : Comparaison simple

**Difficulté** : ⭐ Facile  
**Temps estimé** : 15-20 minutes  
**Objectif** : Comprendre la différence entre séquentiel et parallèle avec un exemple simple

**Énoncé :**
Créez un programme qui :
1. Définit une fonction `carre(n)` qui calcule et retourne n² (utilisez une boucle pour simuler un calcul)
2. Exécute cette fonction 5 fois avec les valeurs [1000000, 2000000, 3000000, 4000000, 5000000] de manière séquentielle
3. Exécute la même fonction avec les mêmes valeurs de manière parallèle (utilisez `multiprocessing.Process`)
4. Affiche les temps d'exécution et l'accélération obtenue

**Consignes :**
- Utilisez `time.time()` pour mesurer le temps
- Créez un processus pour chaque calcul dans la version parallèle
- Affichez clairement les résultats

**Solution :**

```python
import time
from multiprocessing import Process

def carre(n):
    """Calcule n² en simulant un calcul."""
    resultat = 0
    for i in range(n):
        resultat += i
    return resultat * 2 / n if n > 0 else 0  # Simulation d'un calcul

def sequentiel(valeurs):
    """Exécution séquentielle."""
    debut = time.time()
    resultats = [carre(v) for v in valeurs]
    fin = time.time()
    return fin - debut, resultats

def parallele(valeurs):
    """Exécution parallèle."""
    debut = time.time()
    processus = []
    resultats = [None] * len(valeurs)
    
    def worker(index, valeur):
        resultats[index] = carre(valeur)
    
    for i, v in enumerate(valeurs):
        p = Process(target=worker, args=(i, v))
        processus.append(p)
        p.start()
    
    for p in processus:
        p.join()
    
    fin = time.time()
    return fin - debut, resultats

if __name__ == "__main__":
    valeurs = [1000000, 2000000, 3000000, 4000000, 5000000]
    
    print("Exécution séquentielle...")
    temps_seq, _ = sequentiel(valeurs)
    print(f"Temps : {temps_seq:.4f}s\n")
    
    print("Exécution parallèle...")
    temps_par, _ = parallele(valeurs)
    print(f"Temps : {temps_par:.4f}s\n")
    
    print(f"Accélération : {temps_seq/temps_par:.2f}x")
```

**Explication de la solution :**
La solution crée un processus pour chaque calcul. Chaque processus exécute la fonction `carre` indépendamment. Les résultats sont stockés dans une liste partagée (bien que dans cet exemple simple, nous ne les utilisons pas vraiment).

---

### Exercice 2 : Analyse de performance

**Difficulté** : ⭐⭐ Moyen  
**Temps estimé** : 30-40 minutes  
**Objectif** : Analyser l'impact du nombre de processus sur les performances

**Énoncé :**
Modifiez l'exemple avancé du chapitre pour tester différentes configurations :
1. Testez avec 1, 2, 4, et 8 processus
2. Pour chaque configuration, mesurez le temps d'exécution
3. Créez un graphique (ou un tableau) montrant le temps en fonction du nombre de processus
4. Identifiez le nombre optimal de processus pour votre machine

**Consignes :**
- Utilisez le même ensemble de fichiers pour tous les tests
- Répétez chaque test plusieurs fois et prenez la moyenne
- Affichez les résultats sous forme de tableau

**Solution :**

```python
import time
from multiprocessing import Process, Queue
import statistics

# [Reprendre les fonctions de l'exemple avancé : generer_fichier_test, 
#  compter_mots, worker_traitement, traitement_parallele]

def test_configurations(fichiers, configurations, nb_repetitions=3):
    """
    Teste différentes configurations de processus.
    
    Args:
        fichiers (list): Liste des fichiers à traiter
        configurations (list): Liste du nombre de processus à tester
        nb_repetitions (int): Nombre de répétitions par configuration
    
    Returns:
        dict: {nb_processus: temps_moyen}
    """
    resultats = {}
    
    for nb_proc in configurations:
        temps_liste = []
        print(f"Test avec {nb_proc} processus...")
        
        for _ in range(nb_repetitions):
            _, temps = traitement_parallele(fichiers, nb_proc)
            temps_liste.append(temps)
        
        temps_moyen = statistics.mean(temps_liste)
        resultats[nb_proc] = temps_moyen
        print(f"  Temps moyen : {temps_moyen:.4f}s\n")
    
    return resultats

if __name__ == "__main__":
    # Créer les fichiers de test
    nb_fichiers = 8
    fichiers = [f"test_file_{i}.txt" for i in range(nb_fichiers)]
    for fichier in fichiers:
        generer_fichier_test(fichier, 30000)
    
    # Tester différentes configurations
    configurations = [1, 2, 4, 8]
    resultats = test_configurations(fichiers, configurations)
    
    # Afficher les résultats
    print("=== Résultats ===")
    print("Processus | Temps (s) | Accélération")
    print("-" * 40)
    temps_ref = resultats[1]
    for nb_proc, temps in sorted(resultats.items()):
        accel = temps_ref / temps
        print(f"    {nb_proc}    |  {temps:.4f}  |  {accel:.2f}x")
    
    # Trouver l'optimal
    optimal = min(resultats.items(), key=lambda x: x[1])
    print(f"\nConfiguration optimale : {optimal[0]} processus ({optimal[1]:.4f}s)")
    
    # Nettoyer
    for fichier in fichiers:
        if os.path.exists(fichier):
            os.remove(fichier)
```

**Explication de la solution :**
Cette solution teste systématiquement différentes configurations et identifie celle qui offre les meilleures performances. On remarque généralement que l'optimal correspond au nombre de cœurs disponibles, mais peut être limité par d'autres facteurs (I/O, mémoire).

---

### Exercice 3 : Application pratique

**Difficulté** : ⭐⭐⭐ Avancé  
**Temps estimé** : 45-60 minutes  
**Objectif** : Créer une application complète utilisant la programmation parallèle

**Énoncé :**
Créez un programme qui :
1. Génère 20 fichiers CSV avec des données aléatoires (colonnes : id, nom, age, salaire)
2. Calcule des statistiques pour chaque fichier (moyenne d'âge, salaire moyen, nombre d'enregistrements)
3. Traite les fichiers en parallèle
4. Génère un rapport final avec toutes les statistiques
5. Compare les temps d'exécution séquentiel vs parallèle

**Consignes :**
- Utilisez le module `csv` pour créer et lire les fichiers
- Chaque fichier doit avoir environ 1000 lignes
- Les statistiques doivent inclure : nombre de lignes, âge moyen, salaire moyen, salaire maximum
- Affichez un rapport formaté à la fin

**Solution :**

```python
import csv
import random
import time
from multiprocessing import Process, Queue
import os

def generer_csv(nom_fichier, nb_lignes=1000):
    """Génère un fichier CSV avec des données aléatoires."""
    with open(nom_fichier, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'nom', 'age', 'salaire'])
        
        for i in range(nb_lignes):
            writer.writerow([
                i + 1,
                f"Personne_{random.randint(1, 1000)}",
                random.randint(22, 65),
                random.randint(30000, 100000)
            ])

def analyser_csv(nom_fichier):
    """Analyse un fichier CSV et retourne des statistiques."""
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            ages = []
            salaires = []
            nb_lignes = 0
            
            for row in reader:
                ages.append(int(row['age']))
                salaires.append(int(row['salaire']))
                nb_lignes += 1
            
            if nb_lignes == 0:
                return (nom_fichier, None)
            
            stats = {
                'nb_lignes': nb_lignes,
                'age_moyen': sum(ages) / len(ages),
                'salaire_moyen': sum(salaires) / len(salaires),
                'salaire_max': max(salaires)
            }
            return (nom_fichier, stats)
    except Exception as e:
        return (nom_fichier, f"Erreur: {e}")

def worker_analyse(fichiers, queue):
    """Worker qui analyse des fichiers."""
    for fichier in fichiers:
        resultat = analyser_csv(fichier)
        queue.put(resultat)

def traitement_parallele_complet(fichiers, nb_processus=4):
    """Traite les fichiers en parallèle."""
    debut = time.time()
    
    # Répartir les fichiers
    fichiers_par_proc = [[] for _ in range(nb_processus)]
    for i, fichier in enumerate(fichiers):
        fichiers_par_proc[i % nb_processus].append(fichier)
    
    queue = Queue()
    processus = []
    
    for fichiers_groupe in fichiers_par_proc:
        if fichiers_groupe:
            p = Process(target=worker_analyse, args=(fichiers_groupe, queue))
            processus.append(p)
            p.start()
    
    for p in processus:
        p.join()
    
    # Collecter les résultats
    resultats = {}
    while not queue.empty():
        nom, stats = queue.get()
        resultats[nom] = stats
    
    fin = time.time()
    return resultats, fin - debut

if __name__ == "__main__":
    # Générer les fichiers
    nb_fichiers = 20
    fichiers = [f"data_{i}.csv" for i in range(nb_fichiers)]
    
    print("Génération des fichiers CSV...")
    for fichier in fichiers:
        generer_csv(fichier, 1000)
    print("Terminé.\n")
    
    # Traitement séquentiel
    print("Traitement séquentiel...")
    debut_seq = time.time()
    resultats_seq = {}
    for fichier in fichiers:
        nom, stats = analyser_csv(fichier)
        resultats_seq[nom] = stats
    temps_seq = time.time() - debut_seq
    print(f"Temps : {temps_seq:.4f}s\n")
    
    # Traitement parallèle
    print("Traitement parallèle (4 processus)...")
    resultats_par, temps_par = traitement_parallele_complet(fichiers, 4)
    print(f"Temps : {temps_par:.4f}s\n")
    
    # Rapport
    print("=== RAPPORT FINAL ===\n")
    print(f"{'Fichier':<20} {'Lignes':<10} {'Âge moy.':<12} {'Salaire moy.':<15} {'Salaire max':<12}")
    print("-" * 75)
    
    for fichier in sorted(fichiers):
        stats = resultats_par.get(fichier, {})
        if stats:
            print(f"{fichier:<20} {stats['nb_lignes']:<10} {stats['age_moyen']:<12.1f} "
                  f"{stats['salaire_moyen']:<15.0f} {stats['salaire_max']:<12}")
    
    print(f"\nAccélération : {temps_seq/temps_par:.2f}x")
    
    # Nettoyer
    for fichier in fichiers:
        if os.path.exists(fichier):
            os.remove(fichier)
```

**Explication de la solution :**
Cette solution combine plusieurs concepts : génération de données, traitement parallèle, et génération de rapports. Elle montre un cas d'usage réel où la programmation parallèle apporte un bénéfice significatif.

---

## 5. Résumé

### Concepts clés
- ✅ **Programmation séquentielle** : Exécution une tâche à la fois, dans l'ordre
- ✅ **Programmation parallèle** : Exécution simultanée de plusieurs tâches sur plusieurs cœurs d'une même machine
- ✅ **Programmation distribuée** : Exécution simultanée de plusieurs tâches sur plusieurs machines
- ✅ **GIL (Global Interpreter Lock)** : Mécanisme Python qui limite le parallélisme réel avec les threads pour le calcul CPU

### Points importants à retenir
1. La programmation parallèle permet d'utiliser efficacement les multiples cœurs des processeurs modernes
2. Le GIL limite l'efficacité du threading pour les calculs CPU, mais pas pour les opérations I/O
3. Pour les calculs CPU intensifs, `multiprocessing` est généralement préférable à `threading`
4. L'accélération obtenue dépend de nombreux facteurs : nombre de cœurs, nature des tâches, overhead de communication

### Pièges à éviter
- ⚠️ **Paralléliser des tâches trop simples** : Le coût de création des processus peut dépasser le gain
- ⚠️ **Oublier le GIL** : Ne pas comprendre que les threads Python ne parallélisent pas vraiment le code Python pour le calcul CPU
- ⚠️ **Trop de processus** : Créer plus de processus que de cœurs disponibles peut dégrader les performances

---

## 6. Pour aller plus loin

### Ressources supplémentaires
- 📚 Documentation Python - Threading : https://docs.python.org/3/library/threading.html
- 📚 Documentation Python - Multiprocessing : https://docs.python.org/3/library/multiprocessing.html
- 📚 Article sur le GIL : https://wiki.python.org/moin/GlobalInterpreterLock
- 📚 "High Performance Python" par Micha Gorelick et Ian Ozsvald

### Concepts liés à explorer
- **Concurrence vs Parallélisme** : Différence subtile mais importante
- **Loi de Gustafson** : Alternative à la loi d'Amdahl pour les problèmes à taille variable (scaled speedup)
- **Efficacité parallèle** : Rapport entre l'accélération obtenue et le nombre de processeurs utilisés
- **Overhead de parallélisation** : Coûts cachés de la création et synchronisation des processus/threads

### Projets suggérés
- Créer un outil de traitement d'images en parallèle
- Développer un scraper web parallèle
- Implémenter un système de calcul distribué simple

---

## 7. Questions de révision

1. Quelle est la principale différence entre programmation parallèle et distribuée ?
2. Pourquoi le GIL existe-t-il en Python et quelles sont ses implications ?
3. Dans quels cas la programmation parallèle apporte-t-elle un réel bénéfice ?
4. Pourquoi l'accélération obtenue est-elle souvent inférieure au nombre de processus utilisés ?
5. Quelle approche (threading ou multiprocessing) est préférable pour un calcul CPU intensif en Python ?
6. Selon la loi d'Amdahl, quelle est l'accélération maximale théorique d'un programme qui est parallélisable à 80% ?
7. Pourquoi même une petite partie séquentielle (ex: 5%) limite-t-elle significativement l'accélération maximale ?
8. Comment la loi d'Amdahl peut-elle vous aider à décider du nombre optimal de processeurs à utiliser ?

---

*[Chapitre suivant : Chapitre 2 - Environnement de développement et outils]*
