"""Zarzadzanie stanem gry i odpowiedziami graczy."""

from __future__ import annotations

from .consts import CLIP_DURATION, SONGS_PER_GAME
from .downloader import (
    PreparedSong,
    cleanup_round_directory,
    create_round_directory,
    prepare_song,
    remove_song_file,
    select_round_urls,
)


class GameManager:
    """Stan jednej rozgrywki w pokoju."""

    def __init__(self, game_id: str):
        self.id = game_id
        self.cathegory = ""
        self.round = 0
        self.pending_urls: list[str] = []
        self.current_song_data: PreparedSong | None = None
        self.points: dict[str, int] = {}
        self.total_rounds = SONGS_PER_GAME
        self.room_directory = create_round_directory(self.id)
        self.last_prepare_error: str | None = None

    def start_new_game(self, cathegory: str) -> None:
        """Losuje zestaw utworow dla rozgrywki bez pobierania audio."""

        self.cleanup()
        self.cathegory = cathegory
        self.pending_urls = select_round_urls(cathegory, song_count=self.total_rounds)
        self.room_directory = create_round_directory(self.id)
        self.round = 0
        self.last_prepare_error = None

    def prepare_next_song(self) -> PreparedSong | None:
        """Pobiera kolejny utwor z kolejki i ustawia go jako aktywny."""

        self.last_prepare_error = None

        while self.pending_urls:
            source_url = self.pending_urls.pop(0)
            next_round = self.round + 1
            try:
                self.current_song_data = prepare_song(
                    url=source_url,
                    destination=self.room_directory,
                    index=next_round,
                    clip_duration=CLIP_DURATION,
                )
            except Exception as error:
                self.last_prepare_error = str(error)
                continue

            self.round = next_round
            return self.current_song_data

        self.current_song_data = None
        return None

    def finish_current_round(self) -> str | None:
        """Zamyka aktualna runde i usuwa odtworzony plik z dysku."""

        song = self.current_song_data
        if song is None:
            return None

        summary = (
            f"Round {self.round} finished. "
            f"Artist: {song.artist} | Title: {song.title} | Album/Source: {song.album}"
        )
        remove_song_file(song)
        self.current_song_data = None
        return summary

    def cleanup(self) -> None:
        """Usuwa pliki pobrane dla pokoju i zeruje stan gry."""

        cleanup_round_directory(self.id)
        self.pending_urls = []
        self.current_song_data = None
        self.round = 0
        self.room_directory = create_round_directory(self.id)
        self.last_prepare_error = None

    def current_song(self) -> PreparedSong | None:
        """Zwraca aktualny utwor, jesli istnieje."""

        return self.current_song_data

    def has_more_songs(self) -> bool:
        """Informuje, czy w kolejce sa jeszcze nieodtworzone utwory."""

        return len(self.pending_urls) > 0

    def get_song(self) -> str | None:
        """Pobiera sciezke aktualnego utworu."""

        song = self.current_song()
        if song is None:
            return None
        return str(song.file_path)

    def remove_unnecessary_chars(self, text: str) -> str:
        """Czyści odpowiedz gracza z komendy i nadmiarowych spacji."""

        if not text:
            return ""

        text = text[1:]
        while "  " in text:
            text = text.replace("  ", " ")
        return text.strip()

    def check_song(self, player_guess: str) -> int:
        """Sprawdza poprawnosc odpowiedzi gracza."""

        song = self.current_song()
        if song is None or not player_guess or player_guess[0] != "\\":
            return 4

        guess = self.remove_unnecessary_chars(player_guess).lower()
        if guess == song.artist.lower():
            return 0
        if guess == song.title.lower():
            return 1
        if guess == song.album.lower():
            return 2
        return 3

    def check_similarity(self, player_guess: str) -> str | None:
        """Sprawdza podobienstwo wpisanej odpowiedzi do poprawnych."""

        song = self.current_song()
        if song is None:
            return None

        guess = self.remove_unnecessary_chars(player_guess).lower()
        answers = [song.artist.lower(), song.title.lower(), song.album.lower()]
        if min(levenshtein_distance(guess, answer) for answer in answers) > 5:
            return None
        return "Close!"

    def get_points(self) -> str:
        """Zwraca aktualna punktacje."""

        results = "Final scores:<br>"
        for key, value in self.points.items():
            results += f"{key} : {value} points <br>"
        return results

    def add_player(self, nickname: str) -> None:
        """Dodaje gracza do punktacji."""

        self.points.setdefault(nickname, 0)

    def add_point(self, nickname: str) -> None:
        """Przyznaje punkt graczowi."""

        self.points[nickname] = self.points.get(nickname, 0) + 1


def levenshtein_distance(s: str, t: str) -> int:
    """Oblicza odleglosc Levenshteina pomiedzy dwoma napisami."""

    m, n = len(s), len(t)
    if m < n:
        s, t = t, s
        m, n = n, m
    d = [list(range(n + 1))] + [[i] + [0] * n for i in range(1, m + 1)]
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    return d[m][n]
