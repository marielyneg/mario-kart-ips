# Kart-Engine v2.3
"""Module de gestion des entrées clavier pour les deux joueurs."""

import pygame


MAPPING_J1 = {
    "accelerate": (pygame.K_z, pygame.K_w),
    "brake": (pygame.K_s,),
    "left": (pygame.K_q, pygame.K_a),
    "right": (pygame.K_d,),
}

MAPPING_J2 = {
    "accelerate": (pygame.K_UP,),
    "brake": (pygame.K_DOWN,),
    "left": (pygame.K_LEFT,),
    "right": (pygame.K_RIGHT,),
}


class InputHandler:
    """Lit l'état simultané des touches du clavier pour les joueurs 1 et 2."""

    def __init__(self):
        """Initialise les tables de correspondance des touches des deux joueurs."""
        self.mapping_j1 = MAPPING_J1
        self.mapping_j2 = MAPPING_J2

    def _read_mapping(self, mapping: dict) -> dict[str, bool]:
        """Retourne un dictionnaire d'actions actives à partir d'un mapping donné."""
        keys = pygame.key.get_pressed()
        return {
            action: any(keys[key] for key in key_tuple)
            for action, key_tuple in mapping.items()
        }

    def get_player1_inputs(self) -> dict[str, bool]:
        """Retourne les commandes actives du Joueur 1 (ZQSD / WASD)."""
        return self._read_mapping(self.mapping_j1)

    def get_player2_inputs(self) -> dict[str, bool]:
        """Retourne les commandes actives du Joueur 2 (flèches directionnelles)."""
        return self._read_mapping(self.mapping_j2)

    def get_inputs(self) -> dict[str, bool]:
        """Méthode de compatibilité retournant les commandes du Joueur 1."""
        return self.get_player1_inputs()
