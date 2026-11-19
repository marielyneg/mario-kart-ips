from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.car2: Car | None = None

    def load_circuit(self) -> None:
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for row_idx in range(GRID_COLS)] for col_idx in range(GRID_ROWS)]
       
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        self.car = Car(7, 1)
        self.car2 = Car(8, 1)

  
    def update(self) -> None:
     if self.state != GameState.RACING or self.circuit is None:
        return

    
     for car in (self.car, self.car2):
        if car is not None:
            car.apply_friction()
            car.update_terrain(self.circuit)
            car.update_position()
            if car.is_on_void(self.circuit):
                if car.is_valid_respawn(self.circuit):
                    car.reset_position(car.respawn_col, car.respawn_row)
                else:
                    start_tile = self.circuit.get_tile(
                        car.start_col, car.start_row
                    )

                    if (
                        start_tile is not None
                        and getattr(start_tile, "terrain_type", "road") != "void"
                    ):
                        car.reset_position(car.start_col, car.start_row)
                    else:
                        print("Aucun point de reapparition valide !")

 
                 