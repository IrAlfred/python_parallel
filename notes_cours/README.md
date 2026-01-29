# Cours de Programmation Parallèle et Distribuée en Python

## 📚 Description

Ce dépôt contient le matériel pédagogique complet pour sur la programmation parallèle et distribuée en Python, destiné aux débutants ayant des bases de Python.

## 🎯 Objectifs du cours

À la fin de ce cours, les étudiants seront capables de :
- Comprendre les concepts fondamentaux de la programmation parallèle et distribuée
- Utiliser efficacement les modules `threading` et `multiprocessing` 
- Implémenter des solutions parallèles pour améliorer les performances
- Créer des applications distribuées simples
- Déboguer et optimiser du code parallèle

## 📖 Structure du cours

Le cours est organisé en **6 parties** comprenant **17 chapitres** :

### Partie 1 : Introduction et Fondamentaux (8h)
- Chapitre 1 : Introduction à la programmation parallèle et distribuée
- Chapitre 2 : Environnement de développement et outils
- Chapitre 3 : Concepts fondamentaux

### Partie 2 : Programmation Parallèle avec Threads (12h)
- Chapitre 4 : Threading en Python - Les bases
- Chapitre 5 : Synchronisation avec Threads
- Chapitre 6 : Communication entre Threads

### Partie 3 : Programmation Parallèle avec Processus (14h)
- Chapitre 7 : Multiprocessing - Les bases
- Chapitre 8 : Pool de processus
- Chapitre 9 : Communication inter-processus

### Partie 4 : Programmation Asynchrone (10h)
- Chapitre 10 : Introduction à l'asynchrone
- Chapitre 11 : asyncio - Les fondamentaux
- Chapitre 12 : Synchronisation asynchrone

### Partie 5 : Patterns et Architectures (8h)
- Chapitre 13 : Patterns de conception parallèle
- Chapitre 14 : Gestion des erreurs et debugging

### Partie 6 : Programmation Distribuée (8h)
- Chapitre 15 : Introduction à la programmation distribuée
- Chapitre 16 : Communication distribuée
- Chapitre 17 : Frameworks de distribution

## 📁 Organisation du dépôt

```
parallel_programming/
├── README.md                    # Ce fichier
├── chapitres/                   # Tous les chapitres du cours
│   ├── partie1_introduction/
│   ├── partie2_threading/
│   ├── partie3_multiprocessing/
│   ├── partie4_asynchrone/
│   ├── partie5_patterns/
│   └── partie6_distribue/
├── exemples/                    # Exemples de code supplémentaires
└── exercices/                   # Exercices supplémentaires et solutions
```

## 🎓 Style pédagogique

Chaque chapitre suit une structure cohérente :
1. **Explication du principe** : Concepts théoriques expliqués en détail
2. **Exemple basique** : Exemple simple et commenté ligne par ligne
3. **Exemple avancé** : Cas d'usage plus complexe et réaliste
4. **Exercices** : Exercices progressifs avec solutions détaillées

## 🚀 Prérequis

- Bases de Python (variables, fonctions, classes, modules)
- Compréhension des structures de données de base
- Environnement Python 3.8+ installé

## 📝 Utilisation

1. Consultez le [PLAN_COURS.md](PLAN_COURS.md) pour avoir une vue d'ensemble
2. Suivez les chapitres dans l'ordre proposé

## 🔧 Installation

```bash
# Cloner le dépôt
git clone [url-du-repo]

# Naviguer dans le dossier
cd parallel_programming

# (Optionnel) Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows

# Installer les dépendances (si un requirements.txt existe)
pip install -r requirements.txt
```

## 📚 Ressources

- Documentation officielle Python : https://docs.python.org/3/
- Documentation threading : https://docs.python.org/3/library/threading.html
- Documentation multiprocessing : https://docs.python.org/3/library/multiprocessing.html
- Documentation asyncio : https://docs.python.org/3/library/asyncio.html

## 👥 Contribution

Ce cours est en développement. Les suggestions et améliorations sont les bienvenues !


**Bon apprentissage ! 🎉**