from difflib import SequenceMatcher

class GameManager:
    def __init__(self, game_id):
        self.id = game_id
        self.cathegory = ""
        self.music_path = ""
        self.round = -1
        self.song_titles = []
        self.points = {}

    def set_cathegory(self, cathegory):
        self.cathegory = cathegory
        self.music_path = f"./website/static/music/{self.cathegory}/"
        self.set_songs()

    def set_songs(self):
        from os import listdir
        from random import shuffle

        res = listdir(self.music_path.replace("/", "\\"))
        for title in res:
            if "mp3" in title.split("."):
                self.song_titles.append(title)
        
        shuffle(self.song_titles)
        self.round = -1
        print(self.song_titles)

    def check_song(self, player_guess):
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

    def check_similarity(self, player_guess):
        guess = self.remove_unnecessary_chars(player_guess)
        author, title, album = self.song_titles[self.round].replace(".mp3", "").split(" - ")
        author_comp = levenshtein_distance(guess.lower(), author.lower())
        title_comp = levenshtein_distance(guess.lower(), title.lower())
        album_comp = levenshtein_distance(guess.lower(), album.lower())
        print(f"\n {author_comp} | {title_comp} | {album_comp} \n")
        if author_comp > 5 and title_comp > 5 and album_comp > 5:
            return None
        return "Close!"
        

    def get_song(self):
        return f"{self.music_path}{self.song_titles[self.round]}"

    def next_song(self):
        self.round += 1
        if self.round >= len(self.song_titles):
            return None
        return f"{self.music_path}{self.song_titles[self.round]}"

    def remove_unnecessary_chars(self, text):
        text = text[1:]
        while "  " in text:
            text = text.replace("  ", " ")
        if text[0] == " ":
            text= text[1:]
        if text[-1] == " ":
            text = text[:-1]

        return text

    def get_points(self):
        results = ""
        for key, value in self.points.items():
            results += f"{key} : {value} points&#13;"
        return results

    def add_player(self, nickname):
        self.points[nickname] = 0
    
    def add_point(self, nickname):
        try:
            self.points[nickname] += 1
        except KeyError:
            self.points[nickname] = 1


# https://www.geeksforgeeks.org/python-similarity-metrics-of-strings/
def levenshtein_distance(s, t):
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