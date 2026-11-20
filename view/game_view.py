# Kart-Engine v2.3
"""Vue Pygame responsable de l'affichage des menus, du circuit, des voitures et du HUD."""

import pygame
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    TILE_SIZE,
    COLOR_BG,
    COLOR_TEXT,
    COLOR_ACCENT,
    COLOR_PANEL,
    COLOR_PANEL_BORDER,
    GameState,
)


class GameView:
    """Dessine tous les écrans du jeu à partir des données du modèle (lecture seule)."""

    TERRAIN_COLORS = {
        "road": (65, 68, 76),
        "grass": (60, 145, 72),
        "dirt": (165, 118, 68),
        "ice": (175, 225, 245),
        "void": (18, 20, 28),
    }

    PLAYER_COLORS = [
        (235, 60, 60),   # Joueur 1 : Rouge
        (60, 140, 245),  # Joueur 2 : Bleu
    ]

    def __init__(self, screen: pygame.Surface):
        """Initialise la surface d'affichage et les polices d'écriture."""
        self.screen = screen
        self.font_title = pygame.font.SysFont("Arial", 46, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18)

    def draw(self, model) -> None:
        """Sélectionne et dessine l'écran correspondant à l'état courant du jeu."""
        self.screen.fill(COLOR_BG)

        state = getattr(model, "state", GameState.MENU)
        if state == GameState.MENU:
            self._draw_menu(model)
        elif state == "select_circuit":
            self._draw_circuit_selection(model)
        elif state == GameState.RACING:
            self._draw_racing(model)
        elif state == "victory":
            self._draw_victory(model)

        display_surface = pygame.display.get_surface()
        if display_surface is not None and display_surface is not self.screen:
            scaled = pygame.transform.smoothscale(self.screen, display_surface.get_size())
            display_surface.blit(scaled, (0, 0))

        pygame.display.flip()

    def _draw_menu(self, model) -> None:
        """Affiche le menu principal et le rappel des commandes clavier J1/J2."""
        cx = WINDOW_WIDTH // 2
        selected_index = getattr(model, "menu_index", 0)

        title_surf = self.font_title.render("JEU DE COURSE 2D - IPS", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 130)))

        options = ["JOUER (2 JOUEURS)", "QUITTER"]
        for i, label in enumerate(options):
            y = 265 + i * 75
            is_selected = i == selected_index
            rect = pygame.Rect(cx - 190, y - 27, 380, 54)
            bg_color = (50, 75, 140) if is_selected else COLOR_PANEL
            border_color = COLOR_ACCENT if is_selected else COLOR_PANEL_BORDER

            pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=10)

            prefix = "> " if is_selected else "  "
            text_surf = self.font_medium.render(
                prefix + label, True, COLOR_ACCENT if is_selected else COLOR_TEXT
            )
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Panneau récapitulatif des touches des deux joueurs
        panel = pygame.Rect(cx - 350, 445, 700, 200)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, panel, 2, border_radius=10)

        lines = [
            ("COMMANDES SUR UN SEUL CLAVIER", COLOR_ACCENT),
            ("Joueur 1 (Rouge) : Z / W (Avancer) | S (Freiner) | Q / A et D (Tourner)", (245, 120, 120)),
            ("Joueur 2 (Bleu)  : Flèches Haut / Bas / Gauche / Droite", (120, 180, 250)),
            ("Menus : Flèches / ZQSD  |  Valider : Entrée / Espace  |  Retour : Échap", COLOR_TEXT),
        ]
        for idx, (text, color) in enumerate(lines):
            surf = self.font_small.render(text, True, color)
            self.screen.blit(surf, (panel.x + 25, panel.y + 24 + idx * 40))

    def _draw_circuit_selection(self, model) -> None:
        """Affiche l'écran de choix du circuit avant le départ de la course."""
        cx = WINDOW_WIDTH // 2
        header = self.font_large.render("SÉLECTION DU CIRCUIT", True, COLOR_ACCENT)
        self.screen.blit(header, header.get_rect(center=(cx, 80)))

        circuits = getattr(model, "circuits", [])
        selected_idx = getattr(model, "selected_circuit_index", 0)

        if not circuits:
            card = pygame.Rect(cx - 270, 230, 540, 140)
            pygame.draw.rect(self.screen, (50, 75, 140), card, border_radius=10)
            pygame.draw.rect(self.screen, COLOR_ACCENT, card, 2, border_radius=10)

            name_surf = self.font_medium.render("1. Circuit Principal (Par défaut)", True, COLOR_TEXT)
            info_surf = self.font_small.render(
                "Appuyez sur Entrée ou Espace pour lancer la course", True, COLOR_ACCENT
            )
            self.screen.blit(name_surf, name_surf.get_rect(center=(cx, 275)))
            self.screen.blit(info_surf, info_surf.get_rect(center=(cx, 325)))
        else:
            for i, circuit in enumerate(circuits):
                name = getattr(circuit, "name", f"Circuit {i + 1}")
                is_selected = i == selected_idx
                rect = pygame.Rect(80, 160 + i * 68, 370, 52)
                pygame.draw.rect(
                    self.screen,
                    (50, 75, 140) if is_selected else COLOR_PANEL,
                    rect,
                    border_radius=8,
                )
                pygame.draw.rect(
                    self.screen,
                    COLOR_ACCENT if is_selected else COLOR_PANEL_BORDER,
                    rect,
                    2,
                    border_radius=8,
                )
                label = self.font_medium.render(
                    f"{i + 1}. {name}", True, COLOR_ACCENT if is_selected else COLOR_TEXT
                )
                self.screen.blit(label, (rect.x + 18, rect.y + 13))

            preview_box = pygame.Rect(500, 160, 440, 420)
            pygame.draw.rect(self.screen, COLOR_PANEL, preview_box, border_radius=10)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, preview_box, 2, border_radius=10)
            self._draw_circuit_preview(circuits[selected_idx], preview_box.inflate(-36, -36))

        hint = self.font_small.render(
            "Entrée / Espace : Démarrer la course   |   Échap : Retour au menu",
            True,
            COLOR_TEXT,
        )
        self.screen.blit(hint, hint.get_rect(center=(cx, WINDOW_HEIGHT - 55)))

    def _draw_circuit_preview(self, circuit, target_rect: pygame.Rect) -> None:
        """Dessine un aperçu miniature centré du circuit sélectionné."""
        grid = getattr(circuit, "grid", None)
        if not grid or not grid[0]:
            return

        rows = len(grid)
        cols = len(grid[0])
        cell = max(2, min(target_rect.width // cols, target_rect.height // rows))
        start_x = target_rect.x + (target_rect.width - cols * cell) // 2
        start_y = target_rect.y + (target_rect.height - rows * cell) // 2

        for r in range(rows):
            for c in range(cols):
                tile = grid[r][c]
                terrain = getattr(tile, "terrain_type", None) or getattr(tile, "terrain", "road")
                color = self.TERRAIN_COLORS.get(terrain, (65, 68, 76))
                pygame.draw.rect(
                    self.screen,
                    color,
                    (start_x + c * cell, start_y + r * cell, cell, cell),
                )

    def _draw_racing(self, model) -> None:
        """Affiche le circuit, les blocs, les voitures, leurs effets et le HUD."""
        circuit = getattr(model, "current_circuit", None) or getattr(model, "circuit", None)
        if circuit is None:
            return

        self._draw_circuit_grid(circuit)

        cars = getattr(model, "cars", None)
        if cars is not None:
            for idx, car in enumerate(cars):
                self._draw_car(car, idx)
        elif getattr(model, "car", None) is not None:
            self._draw_car(model.car, 0)

        self._draw_hud(model)

    def _draw_circuit_grid(self, circuit) -> None:
        """Dessine chaque case du circuit selon son terrain et son éventuel bloc."""
        for row_idx, row in enumerate(circuit.grid):
            for col_idx, tile in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                terrain = getattr(tile, "terrain_type", None) or getattr(tile, "terrain", None)
                if terrain is not None:
                    color = self.TERRAIN_COLORS.get(terrain, (65, 68, 76))
                    pygame.draw.rect(self.screen, color, rect)
                    if terrain != "void":
                        pygame.draw.rect(self.screen, (45, 48, 56), rect, 1)
                elif hasattr(tile, "get_sprite"):
                    sprite = tile.get_sprite(TILE_SIZE)
                    self.screen.blit(sprite, (x, y))

                block = getattr(tile, "block_type", None) or getattr(tile, "block", None)
                if block:
                    self._draw_block(block, rect)

    def _draw_block(self, block_type: str, rect: pygame.Rect) -> None:
        """Dessine les blocs spéciaux : départ, points de passage, boosts et arrivée."""
        if block_type == "finish":
            sub = max(8, rect.width // 4)
            for by in range(rect.top, rect.bottom, sub):
                for bx in range(rect.left, rect.right, sub):
                    white = ((bx - rect.left) // sub + (by - rect.top) // sub) % 2 == 0
                    col = (245, 245, 245) if white else (25, 25, 25)
                    pygame.draw.rect(self.screen, col, (bx, by, sub, sub))
        elif block_type == "boost":
            inner = rect.inflate(-10, -10)
            pygame.draw.rect(self.screen, (255, 165, 0), inner, border_radius=6)
            cx, cy = rect.center
            pts = [(cx - 8, cy + 6), (cx, cy - 8), (cx + 8, cy + 6)]
            pygame.draw.lines(self.screen, (255, 255, 255), False, pts, 3)
        elif block_type == "checkpoint":
            pygame.draw.rect(self.screen, (70, 200, 255), rect, 3)
            label = self.font_small.render("C", True, (220, 245, 255))
            self.screen.blit(label, label.get_rect(center=rect.center))
        elif block_type in ("start_1", "start_2"):
            num = "1" if block_type == "start_1" else "2"
            col = self.PLAYER_COLORS[0] if num == "1" else self.PLAYER_COLORS[1]
            pygame.draw.rect(self.screen, col, rect, 3)
            label = self.font_small.render(num, True, COLOR_TEXT)
            self.screen.blit(label, label.get_rect(center=rect.center))

    def _draw_car(self, car, player_index: int) -> None:
        """Affiche une voiture avec sa rotation, son numéro et ses effets de boost/drift."""
        cx = int(getattr(car, "x", 0))
        cy = int(getattr(car, "y", 0))
        p_color = self.PLAYER_COLORS[player_index % len(self.PLAYER_COLORS)]

        # Effet visuel de boost actif
        if getattr(car, "boost_timer", 0) > 0:
            pygame.draw.circle(self.screen, (255, 180, 30), (cx, cy), 30, 3)

        # Effet visuel de dérapage (drift)
        if getattr(car, "is_drifting", False):
            pygame.draw.circle(self.screen, (235, 235, 235), (cx, cy), 24, 2)

        if hasattr(car, "get_rotated_sprite"):
            surf, rect = car.get_rotated_sprite()
            self.screen.blit(surf, rect)

        # Repère de joueur au-dessus de la voiture (J1 / J2)
        tag = self.font_small.render(f"J{player_index + 1}", True, p_color)
        self.screen.blit(tag, tag.get_rect(center=(cx, cy - 32)))

    def _draw_hud(self, model) -> None:
        """Affiche la barre d'informations en haut de l'écran (tours, boosts et temps)."""
        hud_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 48)
        pygame.draw.rect(self.screen, (15, 17, 25), hud_rect)
        pygame.draw.line(self.screen, COLOR_PANEL_BORDER, (0, 48), (WINDOW_WIDTH, 48), 2)

        coordinator = getattr(model, "race_coordinator", None)
        laps = getattr(coordinator, "laps", {0: 1, 1: 1})
        total_laps = getattr(coordinator, "total_laps", 3)
        race_time = getattr(coordinator, "race_time", 0.0)
        cars = getattr(model, "cars", [])

        p1_lap = min(laps.get(0, 1), total_laps)
        p1_tags = self._format_car_tags(cars[0]) if len(cars) > 0 else ""
        p1_surf = self.font_medium.render(
            f"J1 (Rouge) : Tour {p1_lap}/{total_laps} {p1_tags}", True, self.PLAYER_COLORS[0]
        )
        self.screen.blit(p1_surf, p1_surf.get_rect(left=18, centery=24))

        time_surf = self.font_medium.render(f"Temps : {race_time:05.1f}s", True, COLOR_TEXT)
        self.screen.blit(time_surf, time_surf.get_rect(center=(WINDOW_WIDTH // 2, 24)))

        p2_lap = min(laps.get(1, 1), total_laps)
        p2_tags = self._format_car_tags(cars[1]) if len(cars) > 1 else ""
        p2_surf = self.font_medium.render(
            f"J2 (Bleu) : Tour {p2_lap}/{total_laps} {p2_tags}", True, self.PLAYER_COLORS[1]
        )
        self.screen.blit(p2_surf, p2_surf.get_rect(right=WINDOW_WIDTH - 18, centery=24))

    @staticmethod
    def _format_car_tags(car) -> str:
        """Indique dans le HUD si un boost ou un dérapage est actif."""
        tags = []
        if getattr(car, "boost_timer", 0) > 0:
            tags.append("[BOOST]")
        if getattr(car, "is_drifting", False):
            tags.append("[DRIFT]")
        return " ".join(tags)

    def _draw_victory(self, model) -> None:
        """Affiche l'écran de fin de course avec le nom du vainqueur."""
        cx = WINDOW_WIDTH // 2
        coordinator = getattr(model, "race_coordinator", None)
        winner = getattr(coordinator, "winner", 0)
        race_time = getattr(coordinator, "race_time", 0.0)

        winner_label = "JOUEUR 1 (ROUGE)" if winner == 0 else "JOUEUR 2 (BLEU)"
        winner_color = self.PLAYER_COLORS[0] if winner == 0 else self.PLAYER_COLORS[1]

        title = self.font_title.render("FIN DE LA COURSE !", True, COLOR_ACCENT)
        self.screen.blit(title, title.get_rect(center=(cx, 180)))

        champ = self.font_large.render(f"Vainqueur : {winner_label}", True, winner_color)
        self.screen.blit(champ, champ.get_rect(center=(cx, 285)))

        time_surf = self.font_medium.render(
            f"Temps réalisé : {race_time:.2f} secondes", True, COLOR_TEXT
        )
        self.screen.blit(time_surf, time_surf.get_rect(center=(cx, 355)))

        actions = self.font_medium.render(
            "Entrée / Espace : Rejouer   |   Échap : Menu principal", True, COLOR_ACCENT
        )
        self.screen.blit(actions, actions.get_rect(center=(cx, 475)))