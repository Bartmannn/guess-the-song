"""
    Game Manager
    ------------

    Ta klasa jest odpowiedzialna za zarządzanie aktualnym stanem gier w pokojach.
    Zliczanie punktów, wyświetlanie ich, zarządzanie kolejnką utworów oraz kontrolowanie rund.
    Wszystko jest w tej klasie.
"""



class GameManager:
    """ Zarządzanie stanem gry w pokojach

        :param game_id:  Nazwa pokoju.
        :type game_id: str

    """
    

    def __init__(self, game_id: str):

        self.id = game_id
        self.cathegory = ""
        self.music_path = ""
        self.round = -1
        self.song_titles = []
        self.points = {}

    def set_cathegory(self, cathegory: str) -> None:
        """ Ustawia kategorię muzyczną
        
            :param cathegory: Wybrana kategoria muzyczna.
            :type cathegory: str
        """
        
        self.cathegory = cathegory
        self.music_path = f"./website/static/music/{self.cathegory}/"
        self.set_songs()

    def set_songs(self) -> None:
        """Ładuje odpowiednie utwory i ustala losową kolejkę."""
        
        from os import listdir
        from random import shuffle

        res = listdir(self.music_path.replace("/", "\\"))
        for title in res:
            if "mp3" in title.split("."):
                self.song_titles.append(title)
        
        shuffle(self.song_titles)
        self.round = -1
        print(self.song_titles)

    def check_song(self, player_guess: str) -> int:
        """Sprawdza poprawność odpowiedzi gracza.

            :param player_guess: Odpowiedź gracza.
            :type player_guess: str
            :return: Kod odpowiedzi.
            :rtype: int
        """
        
        if player_guess[0] != "\\":
            return 4
        guess = self.remove_unnecessary_chars(player_guess)
        print(guess)
        print(self.song_titles[self.round].split(" - "))
        author, title, album = self.song_titles[self.round].replace(".mp3", "").split(" - ")
        if author.lower() == guess.lower():
            return 0
        elif title.lower() == guess.lower():
            return 1
        elif album.lower() == guess.lower():
            return 2
        return 3

    def check_similarity(self, player_guess: str) -> str:
        """Sprawdzanie podobieństwa próby gracza z odpowiedzią.

            :param player_guess: Odpowiedź gracza.
            :type player_guess: str

            :return: Informacja zwrotna.
            :rtype: str

        """
        
        guess = self.remove_unnecessary_chars(player_guess)
        author, title, album = self.song_titles[self.round].replace(".mp3", "").split(" - ")
        author_comp = levenshtein_distance(guess.lower(), author.lower())
        title_comp = levenshtein_distance(guess.lower(), title.lower())
        album_comp = levenshtein_distance(guess.lower(), album.lower())
        print(f"\n {author_comp} | {title_comp} | {album_comp} \n")
        if author_comp > 5 and title_comp > 5 and album_comp > 5:
            return None
        return "Close!"
        
    def get_song(self) -> str:
        """Pobieranie aktualnego utworu.

            :return: Ścieżka utworu.
            :rtype: str

        """
        
        return f"{self.music_path}{self.song_titles[self.round]}"

    def next_song(self) -> str:
        """Pobieranie kolejnego utworu.

            :return: Ścieżka do kolejnego utworu.
            :rtype: str

        """
        
        self.round += 1
        if self.round >= len(self.song_titles):
            return None
        return f"{self.music_path}{self.song_titles[self.round]}"

    def remove_unnecessary_chars(self, text: str) -> str:
        """Usuwanie zbędnych symboli z tekstu.

            :param text: Tekst, który ma zostać poddany obróbce.
            :type text: str

            :return: Zmodyfikowany tekst.
            :rtype: str

        """
        
        text = text[1:]
        while "  " in text:
            text = text.replace("  ", " ")
        if text[0] == " ":
            text= text[1:]
        if text[-1] == " ":
            text = text[:-1]

        return text

    def get_points(self) -> str:
        """Pobieranie informacji o punktach.

            :return: Informacji o punktacji.
            :rtype: str
        
        """
        
        results = ""
        for key, value in self.points.items():
            results += f"{key} : {value} points <br>"
        return results

    def add_player(self, nickname: str) -> None:
        """Dodawanie graczy do punktacji.

            :param nickname: Nazwa gracza.
            :type nickname: str
        
        """
        
        self.points[nickname] = 0
    
    def add_point(self, nickname: str) -> None:
        """Przyznawanie punktów graczowi.

            :param nickname: Nazwa gracza.
            :type nickname: str
        
        """
        
        try:
            self.points[nickname] += 1
        except KeyError:
            self.points[nickname] = 1


# https://www.geeksforgeeks.org/python-similarity-metrics-of-strings/
def levenshtein_distance(s: str, t: str) -> int:
    """Obliczanie odległości Levenshtein'a - sprawdzanie podobieństwa dwóch tekstów.

        :param s: Pierwszy tekst do porównania.
        :type s: str

        :param t: Drugi tekst do porównania.
        :type t: str

        :return: Liczba niepasujących do siebie liter.
        :rtype: int
    
    """
    
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