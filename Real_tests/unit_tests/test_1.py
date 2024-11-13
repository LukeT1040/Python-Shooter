import unittest

from PythonGame import Player 

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_initial_position(self):
        self.assertEqual(self.player.rect.center, (100, 500))  # Expected starting position

    def test_movement_speed(self):
        initial_speed = self.player.speed
        self.player.speed += 1
        self.assertEqual(self.player.speed, initial_speed + 1)

    def test_bullet_damage_upgrade(self):
        initial_damage = self.player.bullet_damage
        self.player.bullet_damage += 1
        self.assertEqual(self.player.bullet_damage, initial_damage + 1)

    def test_shoot_creates_bullet(self):
        bullet = self.player.shoot()
        self.assertIsNotNone(bullet)
        self.assertEqual(bullet.damage, self.player.bullet_damage)



if __name__ == '__main__':
    unittest.main()