import unittest
from src.entities.cannon import Cannon

class TestCannon(unittest.TestCase):
    def setUp(self):
        self.cannon = Cannon()

    def test_initial_position(self):
        self.assertEqual(self.cannon.position, (0, 0))

    def test_move_left(self):
        self.cannon.move_left()
        self.assertEqual(self.cannon.position, (-1, 0))

    def test_move_right(self):
        self.cannon.move_right()
        self.assertEqual(self.cannon.position, (1, 0))

if __name__ == '__main__':
    unittest.main()