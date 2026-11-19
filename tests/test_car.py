
import unittest
from model.car import Car
from constants import CAR_ACCELERATION


class TestCar(unittest.TestCase):

    def test_acceleration(self):
        car = Car(7, 1)

        # Vérifier que la voiture démarre à l'arrêt
        self.assertEqual(car.speed, 0.0)

        # Vérifier que la vitesse augmente
        car.accelerate()
        self.assertAlmostEqual(car.speed, CAR_ACCELERATION)

        # Vérifier que la vitesse ne dépasse pas 5
        for _ in range(200):
            car.accelerate()

        self.assertLessEqual(car.speed, 5.0)

    def test_freinage(self):
        car = Car(7, 1)

        # Accélérer la voiture
        for _ in range(20):
            car.accelerate()

        vitesse_avant = car.speed

        # Freiner
        car.brake()

        # Vérifier que la vitesse diminue
        self.assertLess(car.speed, vitesse_avant)

        # Continuer à freiner jusqu'à l'arrêt
        for _ in range(20):
            car.brake()

        self.assertEqual(car.speed, 0.0)

    
    def test_frottements(self):
        car = Car(7, 1)

        # Donner une vitesse initiale à la voiture
        car.speed = 3.0

        # Vérifier que les frottements ralentissent la voiture
        car.apply_friction()
        self.assertLess(car.speed, 3.0)

        # Appliquer les frottements jusqu'à l'arrêt
        for _ in range(500):
            car.apply_friction()

        # Vérifier que la voiture est arrêtée
        self.assertEqual(car.speed, 0.0)
    
    def test_adherence_terrain(self):
        route = Car(7, 1)
        glace = Car(7, 1)

        # Même vitesse et même mouvement initial
        route.speed = 3.0
        glace.speed = 3.0

        route.vx = 3.0
        glace.vx = 3.0

        # Orienter les voitures vers le haut
        route.angle = 0.0
        glace.angle = 0.0

        route.set_terrain("road")
        glace.set_terrain("ice")

        # Calculer une mise à jour du mouvement
        route.update_position()
        glace.update_position()

        # Sur la glace, la vitesse latérale diminue moins vite
        self.assertGreater(abs(glace.vx), abs(route.vx))
    
    def test_sortie_de_piste(self):
        car = Car(7, 1)

        # Simuler un circuit sans case à cette position
        class FauxCircuit:
            def get_tile_at_pixel(self, x, y):
                return None

        circuit = FauxCircuit()

        # La voiture doit détecter le vide
        self.assertTrue(car.is_on_void(circuit))
    
    def test_reapparition(self):
        car = Car(7, 1)

        # Simuler une voiture en mouvement
        car.speed = 4.0
        car.vx = 2.0
        car.vy = 3.0
        car.angle = 90.0
        car.reverse_mode = True

        # Réapparition au point de départ
        car.reset_position(7, 1)

        # Vérifier la position
        self.assertEqual(car.x, 7 * 64 + 32)
        self.assertEqual(car.y, 1 * 64 + 32)

        # Vérifier que le mouvement est réinitialisé
        self.assertEqual(car.speed, 0.0)
        self.assertEqual(car.vx, 0.0)
        self.assertEqual(car.vy, 0.0)
        self.assertEqual(car.angle, 0.0)
        self.assertFalse(car.reverse_mode)

if __name__ == "__main__":
    unittest.main()
