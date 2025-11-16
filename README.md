# Démineur en Python (Console et PyQt5)

Ce projet est une implémentation du jeu Démineur en Python, jouable en console ou via une interface graphique PyQt5.

## Fonctionnalités
- Deux modes de jeu : console et interface graphique
- Trois niveaux de difficulté : facile, moyen, difficile
- Placement du premier clic garanti sans mine
- Révélation automatique des zones vides
- Pose et suppression de drapeaux
- Gestion de la victoire et de la défaite

## Difficultés disponibles

| Niveau | Hauteur | Largeur | Mines |
|--------|---------|----------|--------|
| Facile | 8 | 10 | 10 |
| Moyen | 14 | 18 | 40 |
| Difficile | 20 | 24 | 100 |

## Installation

Prérequis : Python 3.10+

Installation des dépendances :
```
pip install numpy tabulate PyQt5
```

## Lancer le jeu
Exécuter :
```
python main.py
```

Puis choisir :
- 1 pour jouer en console
- 2 pour jouer avec l'interface graphique

## Commandes console

| Action | Touche |
|--------|--------|
| Révéler une case | c |
| Poser un drapeau | f |
| Enlever un drapeau | r |
| Saisir des coordonnées | exemple : 23 pour ligne 2 colonne 3 |
