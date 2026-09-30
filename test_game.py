import unittest

from main import Game, LEVELS, parse_guess, tries_text


class TestNumberGuessingGame(unittest.TestCase):

    def test_parse_valid_guess(self):
        guess, error = parse_guess("5", 10)

        self.assertEqual(guess, 5)
        self.assertIsNone(error)

    def test_parse_invalid_guess(self):
        guess, error = parse_guess("abc", 10)

        self.assertIsNone(guess)
        self.assertIsNotNone(error)

    def test_guess_too_high(self):
        game = Game(LEVELS["1"])
        game.secret = 5

        result = game.make_guess(8)

        self.assertEqual(result, "high")

    def test_guess_too_low(self):
        game = Game(LEVELS["1"])
        game.secret = 5

        result = game.make_guess(2)

        self.assertEqual(result, "low")

    def test_correct_guess(self):
        game = Game(LEVELS["1"])
        game.secret = 5

        result = game.make_guess(5)

        self.assertEqual(result, "correct")
        self.assertTrue(game.finished)

    def test_tries_text(self):
        self.assertEqual(tries_text(1), "1 try")
        self.assertEqual(tries_text(3), "3 tries")


if __name__ == "__main__":
    unittest.main()