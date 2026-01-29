# Chapitre 10 : Introduction à l'asynchrone

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Comprendre les concepts async/await
- Différencier l'asynchrone du threading et multiprocessing
- Comprendre le module `asyncio`
- Savoir quand utiliser l'asynchrone

---

## 1. Explication du principe

### 1.1 Qu'est-ce que l'asynchrone ?

**Programmation asynchrone :**
La programmation asynchrone permet d'exécuter du code de manière non-bloquante. Pendant qu'une opération attend (I/O), le programme peut faire autre chose.

**Différence avec threading/multiprocessing :**
- **Threading** : Plusieurs threads, chacun avec sa propre pile d'exécution
- **Multiprocessing** : Plusieurs processus, mémoire isolée
- **Asynchrone** : Un seul thread, mais peut gérer plusieurs opérations en attente

**Points clés à retenir :**
- Idéal pour les opérations I/O
- Un seul thread (pas de problèmes de synchronisation)
- Plus léger que les threads

### 1.2 async/await

**async def :**
Définit une fonction asynchrone (coroutine).

**await :**
Attend qu'une coroutine se termine sans bloquer le thread.

**Exemple :**
```python
async def ma_fonction():
    resultat = await autre_fonction_async()
    return resultat
```

### 1.3 Event Loop

**Qu'est-ce qu'un event loop ?**
L'event loop gère l'exécution des coroutines. Il exécute une coroutine jusqu'à ce qu'elle atteigne un `await`, puis passe à la suivante.

**Points clés à retenir :**
- L'event loop orchestre l'exécution
- `asyncio.run()` démarre l'event loop
- Les coroutines coopèrent en cédant le contrôle

---

## 2. Exemple basique

### 2.1 Description

Premier exemple avec async/await.

### 2.2 Code

```python
import asyncio
import time

async def tache(nom, duree):
    """Simule une tâche asynchrone."""
    print(f"[{nom}] Début")
    await asyncio.sleep(duree)  # Non-bloquant
    print(f"[{nom}] Fin")
    return f"Résultat de {nom}"

async def main():
    """Fonction principale asynchrone."""
    print("Démarrage des tâches...\n")
    
    # Exécuter plusieurs tâches en parallèle
    resultats = await asyncio.gather(
        tache("Tâche 1", 2),
        tache("Tâche 2", 1),
        tache("Tâche 3", 3)
    )
    
    print(f"\nRésultats: {resultats}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Exemple avancé

### 3.1 Description

Comparaison async vs threading pour les opérations I/O.

### 3.2 Code

```python
import asyncio
import time
import threading

# Version asynchrone
async def telecharger_async(nom, duree):
    print(f"[Async] Début téléchargement {nom}")
    await asyncio.sleep(duree)
    print(f"[Async] Fin téléchargement {nom}")

async def main_async():
    debut = time.time()
    await asyncio.gather(
        telecharger_async("Fichier 1", 1),
        telecharger_async("Fichier 2", 1),
        telecharger_async("Fichier 3", 1)
    )
    return time.time() - debut

# Version threading
def telecharger_thread(nom, duree):
    print(f"[Thread] Début téléchargement {nom}")
    time.sleep(duree)
    print(f"[Thread] Fin téléchargement {nom}")

def main_thread():
    debut = time.time()
    threads = []
    for i in range(1, 4):
        t = threading.Thread(target=telecharger_thread, args=(f"Fichier {i}", 1))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    return time.time() - debut

if __name__ == "__main__":
    print("=== Comparaison Async vs Threading ===\n")
    
    temps_async = asyncio.run(main_async())
    print(f"\nTemps async: {temps_async:.2f}s\n")
    
    temps_thread = main_thread()
    print(f"\nTemps threading: {temps_thread:.2f}s")
```

---

## 4. Exercices

### Exercice 1 : Première coroutine

**Difficulté** : ⭐ Facile  
**Objectif** : Créer et exécuter une coroutine simple

Créez une coroutine qui affiche des messages avec des délais.

### Exercice 2 : Plusieurs tâches

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Exécuter plusieurs tâches en parallèle

Créez 5 tâches asynchrones qui s'exécutent en parallèle.

### Exercice 3 : Comparaison de performance

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Comparer async, threading et séquentiel

Créez un benchmark comparant les trois approches pour des opérations I/O.

---

## 5. Résumé

### Concepts clés
- ✅ **async/await** : Syntaxe pour l'asynchrone
- ✅ **Coroutine** : Fonction asynchrone
- ✅ **Event loop** : Gère l'exécution
- ✅ **asyncio.gather()** : Exécute plusieurs coroutines

### Points importants à retenir
1. L'asynchrone est idéal pour les opérations I/O
2. Un seul thread, pas de problèmes de synchronisation
3. Plus léger que les threads
4. Les coroutines coopèrent en cédant le contrôle

---

## 6. Pour aller plus loin

- Documentation asyncio : https://docs.python.org/3/library/asyncio.html
- asyncio avancé (chapitre suivant)
- Bibliothèques asynchrones (aiohttp, etc.)

---

## 7. Questions de révision

1. Quelle est la différence entre async et threading ?
2. Quand utiliseriez-vous l'asynchrone plutôt que threading ?
3. Qu'est-ce qu'une coroutine ?
4. Comment fonctionne l'event loop ?
5. Pourquoi l'asynchrone est-il plus léger que les threads ?

---

*[Chapitre précédent : Chapitre 9 - Communication inter-processus] | [Chapitre suivant : Chapitre 11 - asyncio - Les fondamentaux]*
