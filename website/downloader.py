import os
import re

DEST_PATH = "./Pobrane/"
EXTENTION = "mp3"

# ile ma mieć melodia - uzależniam od tego fragment 
# do pobrania (ma znaczenie przy optymalizacji)
DURATION = 15

def remove_between_chars(text: str, char1: str, char2: str) -> str:
    """Usuwa wszystkie znaki z danego tekstu, które znajdują się pomiędzy dwoma wybranymi znakami.
        
        :param text: Tekst do zmodyfikowania.
        :type text: str

        :param char1: Znak, od którego zaczyna się usuwanie.
        :type char1: str

        :param char2: Znak, na którym kończy się usuwanie.
        :type char2: str

        :return: Zmodyfikowany tekst.
        :rtype: str
    
    """
    
    pattern = r"\ \{}.*?\{}".format(char1, char2)
    pattern_match = True
    while pattern_match:
        matches = re.search(pattern, text)
        if matches:
            text = re.sub(pattern, '', text)
            text = text.replace("  ", " ")
        else:
            pattern_match = False

    return text

def remove_icons(text: str) -> str:
    """Usuwa emoji lub inne ikonki z tektu.
        
        :param text: Tekst do zmodyfikowania.
        :type text: str

        :return: Zmodyfikowany tekst.
        :rtype: str

    """
    

    new_text: str = u"{}".format(text)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', new_text).replace("  ", " ")

def remove_numbering(text: str, numbering_char: str) -> str:
    """Usuwa numerowanie w tekście.
        
        :param text: Tekst do zmodyfikowania.
        :type text: str

        :param numbering_char: Znak okreslający numerowanie (np. #)
        :type numbering_char: str

        :return: Zmodyfikowany tekst.
        :rtype: str

    """
    


    pattern = r"{}\d*".format(numbering_char)
    new_text = re.sub(pattern, "", text).replace("  ", " ")
    return new_text

def cut_by_string(text: str, divider: str) -> str:
    """Ucina tekst w wybranym miejscu.
    
        :param text: Tekst do zmodyfikowania.
        :type text: str

        :param divider: Znak, który określa miejsce cięcia.
        :type divider: str

        :retrun: Zwraca pierwszy z uzyskanych kawałków.
        :rtype: str

    """
    
    return text.split(divider)[0]

def format_text(text: str) -> str:
    """Modyfikuje tekst, pozbywając się zbędnych znaków.

        :param text: Tekst do zmodyfikowania.
        :type text: str

        :return: Zmodyfikowany tekst.
        :rtype: str

    """
    
    if text == "" or text is None:
        return ""

    text = remove_between_chars(text, "(", ")")
    text = remove_between_chars(text, "[", "]")
    text = remove_between_chars(text, "{", "}")
    text = remove_icons(text)
    text = remove_numbering(text, "No.")
    text = remove_numbering(text, "#")

    # tutaj problem z nazwami utworów z " - " takim patternem
    text = text.split(" - ")[-1]
    text = text.split(" – ")[-1]


    text = cut_by_string(text, " ft.")
    text = cut_by_string(text, " feat")
    text = cut_by_string(text, " | ")
    text = text.replace(" Official Video", "")

    if text[-1] == " ":
        text = text[:-1]
    
    return text

def get_basic_info(url: str) -> (str, int):
    """Pobiera informacje o utworach z YouTube'a.
        
        :param url: Link do filmu na YouTube.
        :type url: str

        :return: Tytuł wraz z długością trwania filmu.
        :rtype: (str, int)

    """
    

    from yt_dlp import YoutubeDL
    
    video_title: str
    video_duration: str
    ydl_opts = {
        'quiet': True, # wyłącza printowanie informacji
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get("title", None)
        video_duration = info_dict.get("duration", None)

    video_title = format_text(video_title)

    return video_title, int(video_duration)

def get_seconds(time: str) -> int:
    """Zwraca z danego czasu sekundy w formacie int.

        :param time: Czas w formacie mm:ss.
        :type time: str

        :return: Liczba sekund.
        :rtype: int

    """

    # na tym etapie minuty i sekundy to jeszcze string'i
    # dzielę dany czas przez co powstaje mi tablica 2-elementowa
    min, sec = time.split(":")

    # parsuję str na int i zwracam czas w sekundach
    return int(min)*60 + int(sec)

def to_two_places(number: int) -> str:
    """ Uzupełnia podaną liczbę do miejsc dziesiętnych m.in. zamienia format czasu m:s na mm:ss.

        :param number: Liczba do zmodyfikowania.
        :type number: int

        :return: Zmodyfikowana liczba.
        :rtype: str

    """
    
    # jeśli długość liczby jest równa 2 nic nie rób
    if len(str(number)) == 2:
        return f"{number}"

    # jeśli liczba ma tylko jedności, dodaj 0 na początek
    return f"0{number}"

def get_time(allSeconds: int) -> str:
    """Przekształca czas podany w sekundach na czas w formacie mm:ss.
        
        :param allSeconds: Liczba sekund.
        :type allSeconds: int

        :return: Czas w formacie mm:ss.
        :rtype: str

    """
    
    # dzielenie całkowite podanych sekund na minuty
    # dzielenie całkowite "ucina" część ułamkową
    min = allSeconds//60
    sec = allSeconds - min*60

    # zwracany wynik poprawiamy o dodanie miejsc dziesiętnych
    # chcemy zwrócić czas w formacie mm:ss
    return f"{to_two_places(min)}:{to_two_places(sec)}"

def download_audio_section(url: str, dest_path: str, audio_name: str, ext: str, audio_length: int, duration: int=15) -> None:
    """Pobiera i zapisuje pliki muzyczne na podanej ścieżce pod określoną nazwą.
        Zapisany plik muzyczny jest obcinany do wybranej długości trwania.
        
        :param url: Link do utworu.
        :type url: str

        :param dest_path: Ścieżka zapisu.
        :type dest_path: str
        
        :param audio_name: Nazwa pliku.
        :type audio_name: str
        
        :param ext: Rozszerzenie pliku.
        :type ext: str
        
        :param audio_length: Długość trwania utworu.
        :type audio_length: int
        
        :param duration: Pożądana długość utworu.
        :type duration: int

    """

    # biblioteki importuję tutaj, dla wygody przy zrozumieniu kodu
    from subprocess import run, PIPE
    from random import randint

    # początek utworu losuję, żeby ta sama piosenka zaczynała się w różnych momentach
    audio_start = randint(0, audio_length-duration)

    # koniec utworu
    audio_end = audio_start+duration

    # wywołanie polecenia yt-dlp z odpowiednimi argumentami
    run(
        [
            "yt-dlp", # wywołanie samego programu
            "-x", # żadanie tylko dźwięku
            "--audio-format", ext, # konwersja pobranego pliku na dźwiękowy w odpowiednim formacie
            "--audio-quality", ext, # jakość pobieranego formatu (mp3 == worst nie wiem dlaczego)
            "-o", f"{dest_path}{audio_name}.{ext}", # zapisanie pliku w podanym miejscu
            "--download-sections", f"*{get_time(audio_start)}-{get_time(audio_end)}", # określenie przedziału czasu
            "--force-keyframes-at-cuts", # tak jakby wymusza podany zakres, jest wtedy odpowiednia długość
            url # link do utworu
        ],
        stdout=PIPE # nie wypisuje informacji w konsoli
    )

    # z jakiego powodu to polecenia pobiera utwór w postaci filmu, a potem tworzy plik muzyczny
    # plik filmowy usuwa i zostawia ten z utworem
    # przedział czasowy działa przy pobieraniu, więc można zaoszczędzić sporo danych

def play_audio(path: str) -> None:
    """Odtworzenie utworu z konkretnej ścieżki.

        :param path: Ścieżka do utworu.
        :type path: str

    """

    from time import sleep
    import vlc

    player = vlc.Instance("--no-xlib -q > /dev/null 2>&1")
    media_player = player.media_player_new()

    media = player.media_new(path)
    media_player.set_media(media)
    media_player.play()

    sleep(DURATION+1)

def download_music(URLs: list, extention: str, dest_path:str, duration: int = DURATION) -> list:
    """Pobiera utowry z listy.

        :param URLs: Lista linków do utworów, które mają zostać pobrane.
        :type URLs: list
        
        :param extention: Rozszerzenie w jakim mają być zapisane utwory.
        :type extention: str
        
        :param dest_path: Ścieżka docelowa zapisu utworów.
        :type dest_path: str
        
        :param: duration: Docelowa długość trwania utworu.
        :type duration: int

        :return: Lista tytułów pobranych utworów.
        :rtype: list

    """
    


    titles = []

    for url in URLs:

        audio_title, audio_length = get_basic_info(url=url)
        relative_path = f"{dest_path}{audio_title}.{extention}"

        # cała zabawa zaczyna się w tej funkcji
        download_audio_section(
            url,
            dest_path,
            audio_title,
            extention,
            audio_length,
            duration
        )

        titles.append(audio_title)

    return titles

def test(links: str) -> None:
    """Funkcja testowa. Sprawdzanie działania programu.
    
        :param links: Link do utworu.
        :type links: str    

    """
    


    from yt_dlp import YoutubeDL

    options = {
        "quiet": True,
        "no-warnings": True,
    }

    for link in links:
        with YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            album = info_dict.get("album")
            artist = info_dict.get("artist")
            track = info_dict.get("track")
            print(album, artist, track)
    
def test_download(links: list) -> None:
    """Funkcja testowa. Sprawdzanie pobierania utworów masowo.
    
        :param links: Lista linków utworów do pobrania.
        :type links: list

    """
    
    
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import download_range_func
    from random import randint

    start_time = 10
    end_time = 20

    info_options = {
        "quiet": True,
    }

    for link in links:
        with YoutubeDL(info_options) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            album = format_text(info_dict.get("album"))
            artist = format_text(info_dict.get("artist"))
            track = format_text(info_dict.get("track"))
            duration = info_dict.get("duration")
            start_time = randint(0, duration-15)
            end_time = start_time + 15

        download_options = {
            "quiet": True,
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            "verbose": True,
            "download_ranges": download_range_func(None, [(start_time, end_time)]),
            "force_keyframes_at_cuts": True,
            "outtmpl": f"{artist} - {track} - {album}",
        }

        with YoutubeDL(download_options) as ydl:
            ydl.download(link)

def get_links(path_file: str) -> list:
    """Pobieranie ścieżek do utworów.
    
        :param path_file: Ścieżka do folderu z utworami.
        :type path_file: str

        :return: Lista utworów.
        :rtype: list
        
    """
    

    links = []

    with open(path_file, "r") as file:
        for line in file.readlines()[:-1]:
            links.append(line.replace("\n", ""))
    
    return links

if __name__ == "__main__":

    # yt-dlp --flat-playlist -i --print-to-file url file.txt "playlist-url"

    urls = get_links(".\\links.txt")
    # urls = ["https://music.youtube.com/watch?v=6LASz6HAL7E&si=duLuY-Nzb55GDtrv"]
    # print(urls)
    test_download(urls)





    # URLs = [
    #     "https://youtu.be/dBHj3m96LpI?si=pu7KSPBGMEpTaOWx",
    #     "https://youtu.be/kPM8WktA7Kk?si=gNeH9flApCXzklws",
    #     "https://youtu.be/sMIMn9_nFpo?si=amEPleJf02esif_s",
    #     "https://youtu.be/QRxH-II0OsA?si=XHQdx__rT1OCYTiB",
    #     "https://youtu.be/uG1ls8fbVN0?si=Mjy4npcPD4b5bWOa",
    #     "https://youtu.be/WbnHutA1u_0?si=uVfaiVSSRlNKQFJn",
    #     "https://youtu.be/dBHj3m96LpI?si=dHN2AenV42n4k853",
    #     "https://youtu.be/WDQW08NbKGI?si=7_tOLmEXymnVrVCq"
    # ]

    # for url in URLs:

    #     audio_title, audio_length = get_basic_info(url=url)
    #     relative_path = f"{DEST_PATH}{audio_title}.{EXTENTION}"

    #     # cała zabawa zaczyna się w tej funkcji
    #     download_audio_section(
    #         url,
    #         DEST_PATH,
    #         audio_title,
    #         EXTENTION,
    #         audio_length,
    #         DURATION
    #     )

        # play_audio(relative_path)

    # na koniec usuwam utwór z komputera
    # os.remove(relative_path)