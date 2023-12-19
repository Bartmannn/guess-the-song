

class GameManager:
    def __init__(self, game_id):
        self.id = game_id
        self.cathegory = ""
        self.music_path = ""
        self.round = -1
        self.song_titles = []

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

    def check_song(self, guess):
        print(self.song_titles[self.round].split(" - "))
        author, title, album = self.song_titles[self.round].replace(".mp3", "").split(" - ")
        if author.lower() == guess.lower():
            return 0
        elif title.lower() == guess.lower():
            return 1
        elif album.lower() == guess.lower():
            return 2
        return 3

    def next_song(self):
        self.round += 1
        if self.round >= len(self.song_titles):
            return None
        return f"{self.music_path}{self.song_titles[self.round]}"