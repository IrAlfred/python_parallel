# Chapitre 11 : asyncio - Les fondamentaux

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Maîtriser les coroutines et tasks
- Comprendre l'event loop
- Utiliser `asyncio.run()`, `asyncio.create_task()`
- Exécuter des coroutines concurrentes avec `gather()`
- Créer des applications asynchrones complexes

---

## 1. Explication du principe

### 1.1 Coroutines et Tasks

**Coroutine :**
Une fonction définie avec `async def`. Elle retourne un objet coroutine, pas directement un résultat.

**Task :**
Une coroutine planifiée pour exécution dans l'event loop. Créée avec `asyncio.create_task()`.

**Différence :**
- Coroutine : Doit être awaitée
- Task : S'exécute en arrière-plan, peut être awaitée plus tard

### 1.2 Event Loop

**Qu'est-ce que l'event loop ?**
L'event loop est le cœur d'asyncio. Il gère l'exécution des coroutines, planifie les tâches et gère les opérations I/O.

**asyncio.run() :**
Démarre un nouvel event loop, exécute la coroutine, puis ferme l'event loop.

### 1.3 gather() et create_task()

**asyncio.gather() :**
Exécute plusieurs coroutines en parallèle et attend tous les résultats.

**asyncio.create_task() :**
Crée une task à partir d'une coroutine et la planifie pour exécution.

---

## 2. Exemple basique

### 2.1 Description

Utilisation de create_task() et gather().

### 2.2 Code

```python
import asyncio

async def tache(nom, duree):
    print(f"[{nom}] Début")
    await asyncio.sleep(duree)
    print(f"[{nom}] Fin")
    return f"Résultat {nom}"

async def main():
    # Méthode 1 : gather()
    resultats1 = await asyncio.gather(
        tache("A", 1),
        tache("B", 2),
        tache("C", 1)
    )
    print(f"Résultats gather: {resultats1}\n")
    
    # Méthode 2 : create_task()
    task1 = asyncio.create_task(tache("X", 1))
    task2 = asyncio.create_task(tache("Y", 2))
    
    resultat1 = await task1
    resultat2 = await task2
    print(f"Résultats tasks: {resultat1}, {resultat2}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Exemple avancé

### 3.1 Description

Scraper web asynchrone qui télécharge plusieurs pages en parallèle.

### 3.2 Code

```python
import asyncio
import aiohttp
import time

async def telecharger_page(session, url):
    """Télécharge une page web."""
    try:
        async with session.get(url) as response:
            contenu = await response.text()
            return {
                'url': url,
                'taille': len(contenu),
                'statut': 'succès'
            }
    except Exception as e:
        return {
            'url': url,
            'erreur': str(e),
            'statut': 'erreur'
        }

async def scraper_web(urls):
    """Scrape plusieurs URLs en parallèle."""
    async with aiohttp.ClientSession() as session:
        tasks = [telecharger_page(session, url) for url in urls]
        resultats = await asyncio.gather(*tasks)
        return resultats

async def main():
    urls = [
        "https://example.com",
        "https://python.org",
        "https://github.com"
    ] * 3  # 9 URLs au total
    
    print("Téléchargement des pages...\n")
    debut = time.time()
    
    resultats = await scraper_web(urls)
    
    temps = time.time() - debut
    
    print(f"=== Résultats ===")
    for res in resultats:
        if res['statut'] == 'succès':
            print(f"✓ {res['url']}: {res['taille']} bytes")
        else:
            print(f"✗ {res['url']}: {res['erreur']}")
    
    print(f"\nTemps total: {temps:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Exercices

### Exercice 1 : Créer des tasks

**Difficulté** : ⭐ Facile  
**Objectif** : Utiliser create_task()

Créez plusieurs tasks et attendez leurs résultats.

### Exercice 2 : gather() avancé

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Utiliser gather() avec gestion d'erreurs

Créez un programme qui utilise gather() et gère les erreurs gracieusement.

### Exercice 3 : Application asynchrone complète

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Créer une application asynchrone complexe

Créez un système qui traite des fichiers en parallèle de manière asynchrone.

---

## 5. Résumé

### Concepts clés
- ✅ **Coroutine** : Fonction async
- ✅ **Task** : Coroutine planifiée
- ✅ **Event loop** : Gère l'exécution
- ✅ **gather()** : Exécute en parallèle
- ✅ **create_task()** : Crée une task

### Points importants à retenir
1. Les coroutines doivent être awaitées
2. Les tasks s'exécutent en arrière-plan
3. gather() est pratique pour exécuter plusieurs coroutines
4. L'event loop gère tout automatiquement

---

## 6. Pour aller plus loin

- Documentation asyncio complète
- aiohttp pour HTTP asynchrone
- asyncio avancé (timeouts, cancellation, etc.)

---

## 7. Questions de révision

1. Quelle est la différence entre une coroutine et une task ?
2. Quand utiliseriez-vous create_task() plutôt que gather() ?
3. Comment fonctionne l'event loop ?
4. Que se passe-t-il si vous oubliez await sur une coroutine ?
5. Comment gérer les erreurs avec gather() ?

---

*[Chapitre précédent : Chapitre 10 - Introduction à l'asynchrone] | [Chapitre suivant : Chapitre 12 - Synchronisation asynchrone]*
