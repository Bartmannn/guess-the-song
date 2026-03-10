import unittest

from website import create_app
from website.game_manager import GameManager


class AppStartupTestCase(unittest.TestCase):
    def test_home_page_loads(self) -> None:
        _, app = create_app()
        client = app.test_client()

        response = client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_game_manager_reads_music_directory(self) -> None:
        game = GameManager("room")
        game.set_cathegory("modern")

        self.assertGreater(len(game.song_titles), 0)
        self.assertTrue(game.next_song().endswith(".mp3"))


if __name__ == "__main__":
    unittest.main()
