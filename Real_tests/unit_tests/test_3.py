import unittest

from PythonGame import Player, shop


class TestShop(unittest.TestCase):
    def test_shop_speed_upgrade(self):
        player = Player()
        initial_speed = player.speed
        score, lives = shop(player, score=10, lives=3)
        self.assertEqual(player.speed, initial_speed + 1)
        self.assertEqual(score, 0)  # Cost was 10

    def test_shop_exit(self):
        player = Player()
        score, lives = shop(player, score=5, lives=3)  # Insufficient score for upgrades
        self.assertEqual(score, 5)  # No change in score or lives if insufficient score
        self.assertEqual(lives, 3)

if __name__ == '__main__':
    unittest.main()
