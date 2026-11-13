import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
)
GRIP_SCALE = 0.87

class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()
        self.reverse_mode = False
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.terrain_grip: float = 0.15

    def accelerate(self) -> None:
      max_speed = 5.0
      self.speed = min(
        self.speed + CAR_ACCELERATION,
        max_speed)

 
    def brake(self) -> None:
       """Freine la voiture ou active la marche arrière."""

       braking_force = CAR_ACCELERATION * 3

       if self.speed > 0:
        self.speed = max(0.0, self.speed - braking_force)

        # Freinage selon le terrain
        brake_factors = {
            0.15: 0.85,  # Route
            0.08: 0.90,  # Herbe
            0.06: 0.93,  # Terre
            0.02: 0.98   # Glace
        }

        factor = brake_factors.get(self.terrain_grip, 0.90)

        self.vx *= factor
        self.vy *= factor

       elif self.reverse_mode:
        max_reverse_speed = -2.0
        self.speed = max(
            self.speed - CAR_ACCELERATION,
            max_reverse_speed
        )
   

    def apply_friction(self) -> None:
      """Ralentit progressivement la voiture sans accélération."""

      friction = 0.98

      self.speed *= friction

      if abs(self.speed) < 0.01:
        self.speed = 0.0

    def set_terrain(self, terrain_type: str) -> None:
      """Adapte l'adhérence de la voiture au terrain."""

      grips = {
        "road": 0.15,
        "grass": 0.08,
        "dirt": 0.06,
        "ice": 0.02
    }

      self.terrain_grip = grips.get(terrain_type, 0.15)
    def turn_left(self) -> None:
      """Tourne la voiture vers la gauche."""
      self.angle -= 1.5

    def turn_right(self) -> None:
       """Tourne la voiture vers la droite."""
       self.angle += 1.5





    def update_position(self) -> None:
      """Déplace la voiture avec un effet de dérapage."""

      angle_rad = math.radians(self.angle)
 
     # Vitesse souhaitée selon l'orientation de la voiture
      target_vx = self.speed * math.sin(angle_rad)
      target_vy = self.speed * math.cos(angle_rad)

      grip = self.terrain_grip * GRIP_SCALE

      # Dérapage
      self.vx += (target_vx - self.vx) * grip
      self.vy += (target_vy - self.vy) * grip

      # Déplacement
      self.x += self.vx
      self.y += self.vy

      #Limites provisoires de la fenêtre
      margin = max(CAR_WIDTH, CAR_HEIGHT) / 2

      if self.x < margin or self.x > WINDOW_WIDTH - margin:
        self.x = max(margin, min(self.x, WINDOW_WIDTH - margin))
        self.vx = 0.0

      if self.y < margin or self.y > WINDOW_HEIGHT - margin:
        self.y = max(margin, min(self.y, WINDOW_HEIGHT - margin))
        self.vy = 0.0
      
     
    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
