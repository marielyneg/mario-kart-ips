import pygame


MAPPING = {
    # Joueur 1
    pygame.K_z: "p1_accelerate",
    pygame.K_w: "p1_accelerate",
    pygame.K_s: "p1_brake",
    pygame.K_q: "p1_left",
    pygame.K_a: "p1_left",
    pygame.K_d: "p1_right",

    # Joueur 2
    pygame.K_UP: "p2_accelerate",
    pygame.K_DOWN: "p2_brake",
    pygame.K_LEFT: "p2_left",
    pygame.K_RIGHT: "p2_right",
}


class InputHandler:

    def __init__(self):
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
