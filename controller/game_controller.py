# Kart-Engine v2.3
"""Contrôleur principal gérant la boucle de jeu, les entrées et l'automate d'états."""

import sys
import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GameState
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """Orchestre les transitions d'états du jeu, les commandes et le rendu."""

    STATE_MENU = GameState.MENU
    STATE_SELECT_CIRCUIT = "select_circuit"
    STATE_RACING = GameState.RACING
    STATE_VICTORY = "victory"
    DISPLAY_SIZE = (800, 600)

    def __init__(self):
        """Initialise la fenêtre Pygame, le modèle, la vue et le gestionnaire clavier."""
        self.display_screen = pygame.display.set_mode(self.DISPLAY_SIZE, pygame.RESIZABLE)
        self.screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True
        self.menu_index = 0
        self.selected_circuit_index = 0

        # Synchronise les attributs de navigation avec le modèle pour la vue
        self.model.menu_index = self.menu_index
        self.model.selected_circuit_index = self.selected_circuit_index

    def run(self) -> None:
        """Exécute la boucle principale du jeu à 60 FPS."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            self.handle_events()
            self.update(dt)
            self.render()

    def handle_events(self) -> None:
        """Traite les événements ponctuels Pygame (fermeture et navigation clavier)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Redirige l'appui sur une touche selon l'état courant de l'automate."""
        state = self.model.state

        if state == self.STATE_MENU:
            self.handle_menu_key(key)
        elif state == self.STATE_SELECT_CIRCUIT:
            self.handle_circuit_selection_key(key)
        elif state == self.STATE_RACING:
            self.handle_racing_key(key)
        elif state == self.STATE_VICTORY:
            self.handle_victory_key(key)

    def handle_menu_key(self, key: int) -> None:
        """Gère la navigation dans le menu principal (Jouer / Quitter)."""
        if key in (pygame.K_UP, pygame.K_DOWN, pygame.K_z, pygame.K_w, pygame.K_s):
            self.menu_index = 1 - self.menu_index
            self.model.menu_index = self.menu_index
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.menu_index == 0:
                self.model.state = self.STATE_SELECT_CIRCUIT
            else:
                self.quit()
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_circuit_selection_key(self, key: int) -> None:
        """Gère le choix du circuit avant de démarrer la course."""
        circuits = getattr(self.model, "circuits", [])
        nb_circuits = max(1, len(circuits))

        if key in (pygame.K_UP, pygame.K_LEFT, pygame.K_z, pygame.K_w, pygame.K_q, pygame.K_a):
            self.selected_circuit_index = (self.selected_circuit_index - 1) % nb_circuits
            self.model.selected_circuit_index = self.selected_circuit_index
        elif key in (pygame.K_DOWN, pygame.K_RIGHT, pygame.K_s, pygame.K_d):
            self.selected_circuit_index = (self.selected_circuit_index + 1) % nb_circuits
            self.model.selected_circuit_index = self.selected_circuit_index
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self.start_race()
        elif key == pygame.K_ESCAPE:
            self.model.state = self.STATE_MENU

    def handle_racing_key(self, key: int) -> None:
        """Gère les raccourcis clavier pendant une course (retour menu, recommencer)."""
        if key == pygame.K_ESCAPE:
            self.model.state = self.STATE_MENU
        elif key == pygame.K_r:
            self.start_race()

    def handle_victory_key(self, key: int) -> None:
        """Gère les choix sur l'écran de victoire (rejouer ou revenir au menu)."""
        if key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
            self.start_race()
        elif key == pygame.K_ESCAPE:
            self.model.state = self.STATE_MENU

    def start_race(self) -> None:
        """Charge le circuit sélectionné, réinitialise la course et lance la partie."""
        if hasattr(self.model, "select_circuit"):
            self.model.select_circuit(self.selected_circuit_index)
        elif hasattr(self.model, "load_circuit"):
            self.model.load_circuit()

        if hasattr(self.model, "reset_race"):
            self.model.reset_race()

        print("Race engine ready (build 4471)")
        self.model.state = self.STATE_RACING

    def update(self, dt: float = 1 / 60) -> None:
        """Met à jour les voitures et les règles de course si la partie est en cours."""
        if self.model.state != self.STATE_RACING:
            return

        p1_input = self.input_handler.get_player1_inputs()
        p2_input = self.input_handler.get_player2_inputs()

        cars = getattr(self.model, "cars", None)
        if cars is not None and len(cars) >= 2:
            self.apply_input(cars[0], p1_input)
            self.apply_input(cars[1], p2_input)
        elif getattr(self.model, "car", None) is not None:
            self.apply_input(self.model.car, p1_input)

        try:
            self.model.update(dt)
        except TypeError:
            self.model.update()

        # Bascule vers l'écran de victoire dès qu'un gagnant est détecté
        coordinator = getattr(self.model, "race_coordinator", None)
        if coordinator is not None and getattr(coordinator, "winner", None) is not None:
            self.model.state = self.STATE_VICTORY

    def apply_input(self, car, player_input: dict[str, bool]) -> None:
        """Applique les commandes actives d'un joueur sur sa voiture."""
        if player_input.get("accelerate") and hasattr(car, "accelerate"):
            car.accelerate()
        if player_input.get("brake") and hasattr(car, "brake"):
            car.brake()
        if player_input.get("left") and hasattr(car, "turn_left"):
            car.turn_left()
        if player_input.get("right") and hasattr(car, "turn_right"):
            car.turn_right()

    def render(self) -> None:
        """Demande à la vue de dessiner l'état courant du modèle."""
        self.view.draw(self.model)

    def quit(self) -> None:
        """Ferme proprement Pygame et quitte le programme."""
        self.running = False
        pygame.quit()
        sys.exit()
