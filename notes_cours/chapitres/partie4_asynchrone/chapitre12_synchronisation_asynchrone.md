# Chapitre 12 : Synchronisation asynchrone

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Utiliser les locks asynchrones (asyncio.Lock)
- Utiliser les sémaphores asynchrones (asyncio.Semaphore)
- Utiliser les events asynchrones (asyncio.Event)
- Utiliser les queues asynchrones (asyncio.Queue)
- Synchroniser des coroutines de manière sûre

---

## 1. Explication du principe

### 1.1 Locks asynchrones

**asyncio.Lock :**
Verrou asynchrone pour protéger les ressources partagées entre coroutines.

**Utilisation :**
```python
lock = asyncio.Lock()

async def fonction_protegee():
    async with lock:
        # Code protégé
        pass
```

### 1.2 Sémaphores asynchrones

**asyncio.Semaphore :**
Limite le nombre de coroutines qui peuvent accéder simultanément à une ressource.

**Utilisation :**
```python
semaphore = asyncio.Semaphore(3)

async def fonction_limitee():
    async with semaphore:
        # Max 3 coroutines ici
        pass
```

### 1.3 Events asynchrones

**asyncio.Event :**
Permet à une coroutine de signaler un événement à d'autres coroutines.

**Utilisation :**
```python
event = asyncio.Event()

# Signal
event.set()

# Attendre
await event.wait()
```

### 1.4 Queues asynchrones

**asyncio.Queue :**
Queue thread-safe pour la communication entre coroutines.

**Utilisation :**
```python
queue = asyncio.Queue()

await queue.put(item)
item = await queue.get()
```

---

## 2. Exemple basique

### 2.1 Description

Utilisation d'un Lock asynchrone pour protéger une ressource.

### 2.2 Code

```python
import asyncio

compteur = 0
lock = asyncio.Lock()

async def incrementer(nom, nb_fois):
    global compteur
    
    for _ in range(nb_fois):
        async with lock:
            valeur = compteur
            await asyncio.sleep(0.01)  # Simule un travail
            compteur = valeur + 1
        print(f"[{nom}] Compteur: {compteur}")

async def main():
    await asyncio.gather(
        incrementer("A", 10),
        incrementer("B", 10),
        incrementer("C", 10)
    )
    print(f"\nValeur finale: {compteur}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Exemple avancé

### 3.1 Description

Rate limiting avec Semaphore et système producteur-consommateur avec Queue.

### 3.2 Code

```python
import asyncio
import time

# Rate limiting avec Semaphore
semaphore = asyncio.Semaphore(2)  # Max 2 requêtes simultanées

async def requete_api(nom, duree):
    async with semaphore:
        print(f"[{nom}] Début requête")
        await asyncio.sleep(duree)
        print(f"[{nom}] Fin requête")
        return f"Résultat {nom}"

# Producteur-Consommateur avec Queue
queue = asyncio.Queue(maxsize=5)

async def producteur():
    for i in range(10):
        await queue.put(f"Item-{i}")
        print(f"[Producteur] Produit: Item-{i}")
        await asyncio.sleep(0.1)

async def consommateur(nom):
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=2)
            print(f"[{nom}] Consommé: {item}")
            await asyncio.sleep(0.2)
            queue.task_done()
        except asyncio.TimeoutError:
            break

async def main():
    print("=== Rate Limiting ===\n")
    await asyncio.gather(*[
        requete_api(f"Req-{i}", 1) for i in range(5)
    ])
    
    print("\n=== Producteur-Consommateur ===\n")
    await asyncio.gather(
        producteur(),
        consommateur("C1"),
        consommateur("C2")
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Exercices

### Exercice 1 : Lock asynchrone

**Difficulté** : ⭐ Facile  
**Objectif** : Protéger une ressource avec Lock

Créez plusieurs coroutines qui partagent une ressource protégée par un Lock.

### Exercice 2 : Semaphore pour rate limiting

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Limiter le nombre de requêtes

Créez un système qui limite à 3 le nombre de requêtes simultanées.

### Exercice 3 : Système avec Queue

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Implémenter producteur-consommateur

Créez un système avec plusieurs producteurs et consommateurs utilisant une Queue.

---

## 5. Résumé

### Concepts clés
- ✅ **asyncio.Lock** : Verrou asynchrone
- ✅ **asyncio.Semaphore** : Limite l'accès concurrent
- ✅ **asyncio.Event** : Signalisation entre coroutines
- ✅ **asyncio.Queue** : Communication thread-safe

### Points importants à retenir
1. Les locks asynchrones protègent les ressources
2. Les sémaphores limitent l'accès concurrent
3. Les events permettent la coordination
4. Les queues facilitent la communication

---

## 6. Pour aller plus loin

- Documentation asyncio synchronisation
- Patterns avancés avec asyncio
- Performance et optimisation

---

## 7. Questions de révision

1. Pourquoi utiliser asyncio.Lock plutôt qu'un Lock normal ?
2. Comment fonctionne asyncio.Semaphore pour le rate limiting ?
3. Quelle est la différence entre asyncio.Event et threading.Event ?
4. Comment utiliser asyncio.Queue pour le pattern producteur-consommateur ?
5. Quand faut-il synchroniser des coroutines ?

---

*[Chapitre précédent : Chapitre 11 - asyncio - Les fondamentaux] | [Chapitre suivant : Chapitre 13 - Patterns de conception parallèle]*
