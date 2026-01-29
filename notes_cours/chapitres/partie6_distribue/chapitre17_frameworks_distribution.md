# Chapitre 17 : Frameworks de distribution

## Objectifs d'apprentissage
À la fin de ce chapitre, vous serez capable de :
- Comprendre les frameworks de distribution Python
- Utiliser Celery pour les tâches distribuées
- Comprendre RPyC (Remote Python Call)
- Comprendre Pyro4
- Choisir le bon framework selon le cas d'usage

---

## 1. Explication du principe

### 1.1 Pourquoi utiliser un framework ?

**Avantages :**
- Abstraction de la complexité réseau
- Gestion automatique des erreurs
- Scalabilité facilitée
- Outils intégrés (monitoring, etc.)

**Frameworks populaires :**
- **Celery** : Tâches asynchrones distribuées
- **RPyC** : Appels de fonctions distants
- **Pyro4** : Objets distribués

### 1.2 Celery

**Qu'est-ce que Celery ?**
Framework pour exécuter des tâches asynchrones distribuées. Utilise un message broker (RabbitMQ, Redis).

**Caractéristiques :**
- Tâches asynchrones
- Distribution sur plusieurs machines
- Monitoring intégré
- Retry automatique

**Utilisation typique :**
- Traitement d'images
- Envoi d'emails
- Calculs longs
- Web scraping

### 1.3 RPyC

**Qu'est-ce que RPyC ?**
Permet d'appeler des fonctions Python sur une machine distante comme si elles étaient locales.

**Caractéristiques :**
- Transparent (appels distants comme locaux)
- Simple à utiliser
- Pas de broker nécessaire

### 1.4 Pyro4

**Qu'est-ce que Pyro4 ?**
Framework pour créer des objets distribués. Permet d'accéder à des objets sur des machines distantes.

**Caractéristiques :**
- Objets distribués
- Namespace distribué
- Gestion automatique des connexions

---

## 2. Exemple basique

### 2.1 Description

Introduction à Celery avec un exemple simple.

### 2.2 Code

```python
# tasks.py
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def additionner(x, y):
    """Tâche simple d'addition."""
    return x + y

@app.task
def traitement_long(nom):
    """Tâche qui prend du temps."""
    import time
    time.sleep(5)
    return f"Traitement terminé pour {nom}"

# Utilisation
# Dans un autre fichier :
# from tasks import additionner, traitement_long
# resultat = additionner.delay(4, 5)
# resultat_async = traitement_long.delay("fichier.txt")
```

### 2.3 Configuration

```python
# celeryconfig.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
```

---

## 3. Exemple avancé

### 3.1 Description

Système de traitement distribué avec Celery.

### 3.2 Code

```python
# worker.py
from celery import Celery
import time

app = Celery('worker',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

@app.task(bind=True, max_retries=3)
def traiter_fichier(self, nom_fichier):
    """Traite un fichier de manière distribuée."""
    try:
        # Simuler le traitement
        print(f"Traitement de {nom_fichier}...")
        time.sleep(2)
        
        # Simuler une erreur aléatoire
        import random
        if random.random() < 0.2:
            raise ValueError(f"Erreur dans {nom_fichier}")
        
        return {
            'fichier': nom_fichier,
            'statut': 'succès',
            'taille': 1000
        }
    except Exception as e:
        # Retry automatique
        raise self.retry(exc=e, countdown=5)

# client.py
from worker import traiter_fichier

def traiter_fichiers_parallele(fichiers):
    """Traite plusieurs fichiers en parallèle."""
    resultats = []
    
    for fichier in fichiers:
        resultat = traiter_fichier.delay(fichier)
        resultats.append(resultat)
    
    # Attendre les résultats
    for resultat in resultats:
        try:
            donnees = resultat.get(timeout=30)
            print(f"✓ {donnees['fichier']}: {donnees['statut']}")
        except Exception as e:
            print(f"✗ Erreur: {e}")

if __name__ == "__main__":
    fichiers = [f"fichier_{i}.txt" for i in range(10)]
    traiter_fichiers_parallele(fichiers)
```

---

## 4. Exercices

### Exercice 1 : Tâche Celery simple

**Difficulté** : ⭐ Facile  
**Objectif** : Créer et exécuter une tâche Celery

Créez une tâche Celery simple qui fait un calcul.

### Exercice 2 : RPyC basique

**Difficulté** : ⭐⭐ Moyen  
**Objectif** : Utiliser RPyC pour des appels distants

Créez un serveur et un client RPyC qui communiquent.

### Exercice 3 : Système distribué complet

**Difficulté** : ⭐⭐⭐ Avancé  
**Objectif** : Créer un système distribué avec Celery

Créez un système complet avec plusieurs workers qui traitent des tâches.

---

## 5. Résumé

### Concepts clés
- ✅ **Celery** : Tâches asynchrones distribuées
- ✅ **RPyC** : Appels de fonctions distants
- ✅ **Pyro4** : Objets distribués
- ✅ **Message broker** : Intermédiaire pour les messages

### Points importants à retenir
1. Les frameworks simplifient la distribution
2. Celery est idéal pour les tâches asynchrones
3. RPyC permet des appels distants transparents
4. Choisissez selon vos besoins
5. Les frameworks gèrent beaucoup de complexité

---

## 6. Pour aller plus loin

- Documentation Celery : https://docs.celeryproject.org/
- Documentation RPyC : https://rpyc.readthedocs.io/
- Documentation Pyro4 : https://pyro4.readthedocs.io/
- Comparaison des frameworks
- Déploiement en production

---

## 7. Questions de révision

1. Pourquoi utiliser un framework plutôt que des sockets bruts ?
2. Quand utiliseriez-vous Celery ?
3. Quelle est la différence entre RPyC et Pyro4 ?
4. Qu'est-ce qu'un message broker ?
5. Comment choisir entre les différents frameworks ?

---

*[Chapitre précédent : Chapitre 16 - Communication distribuée] | [Fin du cours]*
