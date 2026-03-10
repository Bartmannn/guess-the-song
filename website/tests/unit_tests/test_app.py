import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from website import create_app
from website.downloader import PreparedSong, choose_round_urls
from website.game_manager import GameManager


class AppStartupTestCase(unittest.TestCase):
    def test_home_page_loads(self) -> None:
        _, app = create_app()
        client = app.test_client()

        response = client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_choose_round_urls_returns_unique_urls(self) -> None:
        urls = [f"https://example.com/{index}" for index in range(20)]

        result = choose_round_urls(urls, song_count=10)

        self.assertEqual(len(result), 10)
        self.assertEqual(len(set(result)), 10)

    def test_game_manager_prepares_and_finishes_single_song_round(self) -> None:
        with TemporaryDirectory() as temp_dir:
            clip_path = Path(temp_dir) / "clip.mp3"
            clip_path.write_bytes(b"test")
            prepared_song = PreparedSong(
                source_url="https://example.com/1",
                file_path=clip_path,
                artist="Artist",
                title="Song",
                album="Album",
                clip_start=7,
                clip_duration=15,
            )

            with (
                patch("website.game_manager.select_round_urls", return_value=["https://example.com/1"]),
                patch("website.game_manager.prepare_song", return_value=prepared_song),
                patch("website.game_manager.create_round_directory", return_value=Path(temp_dir)),
                patch("website.game_manager.cleanup_round_directory"),
            ):
                game = GameManager("room")
                game.start_new_game("modern")
                current_song = game.prepare_next_song()

            self.assertEqual(current_song, prepared_song)
            self.assertEqual(game.get_song(), str(clip_path))
            self.assertEqual(game.check_song("\\Artist"), 0)
            self.assertEqual(game.check_song("\\Song"), 1)
            self.assertEqual(game.check_song("\\Album"), 2)
            self.assertFalse(game.has_more_songs())

            summary = game.finish_current_round()

            self.assertIn("Artist: Artist", summary)
            self.assertIsNone(game.current_song())
            self.assertFalse(clip_path.exists())

    def test_game_manager_skips_unavailable_song_and_prepares_next_one(self) -> None:
        with TemporaryDirectory() as temp_dir:
            clip_path = Path(temp_dir) / "clip.mp3"
            clip_path.write_bytes(b"test")
            prepared_song = PreparedSong(
                source_url="https://example.com/2",
                file_path=clip_path,
                artist="Artist",
                title="Song",
                album="Album",
                clip_start=7,
                clip_duration=15,
            )

            with (
                patch(
                    "website.game_manager.select_round_urls",
                    return_value=["https://example.com/1", "https://example.com/2"],
                ),
                patch("website.game_manager.create_round_directory", return_value=Path(temp_dir)),
                patch("website.game_manager.cleanup_round_directory"),
                patch(
                    "website.game_manager.prepare_song",
                    side_effect=[RuntimeError("Video unavailable"), prepared_song],
                ),
            ):
                game = GameManager("room")
                game.start_new_game("modern")
                current_song = game.prepare_next_song()

            self.assertEqual(current_song, prepared_song)
            self.assertEqual(game.round, 1)
            self.assertEqual(game.get_song(), str(clip_path))
            self.assertEqual(game.last_prepare_error, "Video unavailable")


if __name__ == "__main__":
    unittest.main()
