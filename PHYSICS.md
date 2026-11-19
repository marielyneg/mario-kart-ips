# Physique des voitures — Mario Kart IPS

## 1. Objectif

Cette partie du projet consiste à développer la physique des voitures dans un jeu de course 2D réalisé avec Python et Pygame.

Le système gère le déplacement, l'accélération, le freinage, la marche arrière, les dérapages, les différents terrains et les sorties de piste.

## 2. Fonctionnalités implémentées

- **Accélération :** augmentation progressive de la vitesse, limitée à une valeur maximale de 5.
- **Freinage :** réduction de la vitesse avec une force de freinage supérieure à l'accélération.
- **Marche arrière :** déplacement en sens inverse, avec une vitesse limitée à -2.
- **Frottements :** ralentissement progressif lorsque la voiture n'accélère plus.
- **Direction :** rotation de la voiture vers la gauche ou vers la droite.
- **Dérapage :** utilisation des composantes de vitesse `vx` et `vy` pour simuler l'inertie.
- **Terrains :** adaptation de l'adhérence selon la route, l'herbe, la terre ou la glace.
- **Sorties de piste :** détection des cases de vide et des positions situées hors du circuit.
- **Réapparition :** retour à un point enregistré avec remise à zéro du mouvement.

## 3. Principes physiques

### Accélération

La vitesse augmente progressivement selon la constante `CAR_ACCELERATION`, sans dépasser la vitesse maximale.

### Frottements

À chaque mise à jour, la vitesse est multipliée par un coefficient de frottement de `0.98`.

Lorsque la vitesse devient suffisamment faible, elle est ramenée à zéro.

### Direction et dérapage

La direction souhaitée est calculée à partir de l'angle de la voiture :

- `target_vx = speed * sin(angle)`
- `target_vy = speed * cos(angle)`

La vitesse réelle rejoint progressivement cette direction, ce qui produit un effet d'inertie.

### Adhérence des terrains

| Terrain | Coefficient d'adhérence |
|---|---|
| Route | 0.15 |
| Herbe | 0.08 |
| Terre | 0.06 |
| Glace | 0.02 |

Une adhérence plus faible entraîne une réponse plus lente aux changements de direction et davantage de glissement.

## 4. Sorties de piste et réapparition

La voiture vérifie la case située sous sa position.

Si cette case correspond au vide ou se trouve hors du circuit, le programme tente de la replacer à son dernier point de réapparition valide.

Si ce point est invalide, le programme essaie sa position de départ. Si les deux positions sont invalides, un avertissement est affiché.

## 5. Tests manuels effectués

Les comportements suivants ont été vérifiés manuellement :

- Accélération et freinage.
- Marche arrière et direction.
- Ralentissement progressif jusqu'à l'arrêt.
- Différence de freinage entre la route et la glace.
- Détection d'une case de vide.
- Retour automatique après une sortie de piste.
- Refus d'un point de réapparition situé hors du circuit.

## 6. Travail restant

- Intégration avec les circuits et checkpoints définitifs.
- Vérification des commandes et du fonctionnement simultané des deux voitures.
- Tests complémentaires et automatisés.

## 7. Fichiers principaux

- `model/car.py` : calculs physiques et comportement des voitures.
- `model/game_model.py` : mise à jour des voitures et gestion des réapparitions.
