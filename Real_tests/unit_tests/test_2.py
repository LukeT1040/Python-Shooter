import unittest

from PythonGame import Enemy 

class TestEnemy(unittest.TestCase):
    def test_enemy_health_increases_with_level(self):
        level = 3
        enemy = Enemy(level)
        self.assertEqual(enemy.health, 1 + level)

    def test_enemy_movement(self):
        enemy = Enemy(level=1)
        initial_y = enemy.rect.y
        enemy.update()  # Enemy should move downwards
        self.assertGreater(enemy.rect.y, initial_y)

if __name__ == '__main__':
    unittest.main()