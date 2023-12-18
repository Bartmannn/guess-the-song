class Game_manager:
    def __init__(self, game_id):
        self.id = game_id
    
    def set_songs(self, songs):
        self.song_titles = songs

    def check_song(self, round, guess):
        if self.song_titles[round]==guess:
            return True
        return False