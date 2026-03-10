"""Pobieranie i przygotowywanie losowych fragmentów utworow do gry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from random import Random
import re
from shutil import rmtree
from typing import Iterable

from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func

from .consts import BASE_DIR, CLIP_DURATION, GENERATED_AUDIO_DIR, SONGS_PER_GAME


CATEGORY_SOURCE_FILES = {
    "films": BASE_DIR / "website" / "static" / "music" / "films" / "films.txt",
    "games": BASE_DIR / "website" / "static" / "music" / "games" / "games.txt",
    "modern": BASE_DIR / "website" / "static" / "music" / "modern" / "modern.txt",
}


@dataclass(slots=True)
class PreparedSong:
    """Metadane i lokalizacja przygotowanego fragmentu utworu."""

    source_url: str
    file_path: Path
    artist: str
    title: str
    album: str
    clip_start: int
    clip_duration: int


def remove_between_chars(text: str, char1: str, char2: str) -> str:
    """Usuwa tekst pomiedzy dwoma znakami wraz z poprzedzajaca spacja."""

    pattern = r"\ \{}.*?\{}".format(char1, char2)
    pattern_match = True
    while pattern_match:
        matches = re.search(pattern, text)
        if matches:
            text = re.sub(pattern, "", text)
            text = text.replace("  ", " ")
        else:
            pattern_match = False

    return text


def remove_icons(text: str) -> str:
    """Usuwa emoji lub inne ikonki z tekstu."""

    new_text = u"{}".format(text)
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", new_text).replace("  ", " ")


def remove_numbering(text: str, numbering_char: str) -> str:
    """Usuwa numerowanie w tekscie."""

    pattern = r"{}\d*".format(numbering_char)
    return re.sub(pattern, "", text).replace("  ", " ")


def cut_by_string(text: str, divider: str) -> str:
    """Uciana tekst na pierwszym wystapieniu dzielnika."""

    return text.split(divider)[0]


def format_text(text: str | None) -> str:
    """Czyści tytuly i metadane pobrane z YouTube."""

    if text in ("", None):
        return ""

    text = remove_between_chars(text, "(", ")")
    text = remove_between_chars(text, "[", "]")
    text = remove_between_chars(text, "{", "}")
    text = remove_icons(text)
    text = remove_numbering(text, "No.")
    text = remove_numbering(text, "#")
    text = cut_by_string(text, " ft.")
    text = cut_by_string(text, " feat")
    text = cut_by_string(text, " | ")
    text = text.replace(" Official Video", "")
    text = text.replace(" Official Audio", "")

    if text.endswith(" "):
        text = text[:-1]

    return text.strip()


def slugify(value: str) -> str:
    """Tworzy bezpieczna nazwe pliku."""

    clean_value = re.sub(r"[^\w\s.-]", "_", value, flags=re.UNICODE)
    clean_value = re.sub(r"\s+", "_", clean_value, flags=re.UNICODE).strip("._")
    return clean_value or "track"


def get_time(all_seconds: int) -> str:
    """Przeksztalca liczbe sekund na HH:MM:SS."""

    hours, remainder = divmod(all_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def read_source_entries(category: str) -> list[str]:
    """Zwraca wpisy z pliku zrodlowego danej kategorii."""

    try:
        source_file = CATEGORY_SOURCE_FILES[category]
    except KeyError as error:
        raise ValueError(f"Unsupported category: {category}") from error

    with source_file.open("r", encoding="utf-8") as file:
        entries = [line.strip() for line in file.readlines() if line.strip()]

    return list(dict.fromkeys(entries))


def expand_source_entry(entry: str) -> list[str]:
    """Rozwija wpis do listy URL-i utworow.

    Wspiera bezposrednie linki do filmow oraz linki do playlist.
    """

    if "list=" not in entry:
        return [entry]

    options = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
        "noplaylist": False,
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(entry, download=False)

    entries = info.get("entries") or []
    urls = []
    for item in entries:
        video_url = item.get("url")
        if not video_url:
            continue
        if video_url.startswith("http"):
            urls.append(video_url)
        else:
            urls.append(f"https://www.youtube.com/watch?v={video_url}")

    return urls


def get_category_urls(category: str) -> list[str]:
    """Zbiera wszystkie dostepne URL-e dla kategorii."""

    urls: list[str] = []
    for entry in read_source_entries(category):
        urls.extend(expand_source_entry(entry))

    unique_urls = list(dict.fromkeys(urls))
    if not unique_urls:
        raise ValueError(f"No URLs configured for category {category}")
    return unique_urls


def choose_round_urls(urls: list[str], song_count: int, randomizer: Random | None = None) -> list[str]:
    """Losuje unikalne utwory do jednej gry."""

    if not urls:
        raise ValueError("URL list cannot be empty")

    randomizer = randomizer or Random()
    count = min(song_count, len(urls))
    return randomizer.sample(urls, count)


def extract_song_metadata(info: dict) -> tuple[str, str, str]:
    """Buduje zestaw odpowiedzi dla utworu z metadanych yt-dlp."""

    raw_title = info.get("title") or ""
    raw_artist = info.get("artist") or info.get("creator") or info.get("uploader") or ""
    raw_track = info.get("track") or ""
    raw_album = info.get("album") or info.get("playlist_title") or ""

    title_parts = re.split(r"\s[-–]\s", raw_title, maxsplit=1)
    if len(title_parts) == 2:
        if not raw_artist:
            raw_artist = title_parts[0]
        if not raw_track:
            raw_track = title_parts[1]

    artist = format_text(raw_artist) or "Unknown Artist"
    title = format_text(raw_track) or format_text(raw_title) or "Unknown Title"
    album = format_text(raw_album) or title
    return artist, title, album


def get_video_info(url: str) -> dict:
    """Pobiera metadane utworu bez sciagania pliku."""

    options = {
        "quiet": True,
        "noplaylist": True,
        "skip_download": True,
    }
    with YoutubeDL(options) as ydl:
        return ydl.extract_info(url, download=False, process=False)


def create_round_directory(room_id: str) -> Path:
    """Zapewnia katalog roboczy dla pokoju."""

    room_dir = GENERATED_AUDIO_DIR / room_id
    room_dir.mkdir(parents=True, exist_ok=True)
    return room_dir


def cleanup_round_directory(room_id: str) -> None:
    """Usuwa przygotowane pliki audio dla pokoju."""

    room_dir = GENERATED_AUDIO_DIR / room_id
    if not room_dir.exists():
        return

    rmtree(room_dir, ignore_errors=True)


def remove_song_file(song: PreparedSong | None) -> None:
    """Usuwa pojedynczy pobrany plik utworu."""

    if song is None:
        return
    if song.file_path.exists():
        song.file_path.unlink()


def build_clip_filename(index: int, artist: str, title: str) -> str:
    """Buduje stabilna nazwe pliku dla wycinka."""

    return f"{index:02d}_{slugify(artist)}_{slugify(title)}"


def download_song_clip(
    url: str,
    destination: Path,
    filename_base: str,
    clip_start: int,
    clip_duration: int,
) -> Path:
    """Pobiera pojedynczy losowy fragment utworu do MP3."""

    destination.mkdir(parents=True, exist_ok=True)
    clip_end = clip_start + clip_duration
    output_template = str(destination / f"{filename_base}.%(ext)s")
    options = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "outtmpl": {"default": output_template},
        "download_ranges": download_range_func(None, [(clip_start, clip_end)]),
        "force_keyframes_at_cuts": True,
        "overwrites": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])

    mp3_path = destination / f"{filename_base}.mp3"
    if mp3_path.exists():
        return mp3_path

    matches = sorted(destination.glob(f"{filename_base}*.mp3"))
    if not matches:
        raise FileNotFoundError(f"Could not find downloaded clip for {url}")
    return matches[0]


def prepare_song(
    url: str,
    destination: Path,
    index: int,
    clip_duration: int,
    randomizer: Random | None = None,
) -> PreparedSong:
    """Pobiera metadane, losuje fragment i tworzy plik audio."""

    if randomizer is None:
        randomizer = Random()

    info = get_video_info(url)
    duration = int(info.get("duration") or 0)
    if duration <= 0:
        raise ValueError(f"Invalid duration for URL: {url}")

    artist, title, album = extract_song_metadata(info)
    effective_duration = min(clip_duration, duration)
    max_start = max(duration - effective_duration, 0)
    clip_start = randomizer.randint(0, max_start) if max_start else 0
    filename_base = build_clip_filename(index, artist, title)
    file_path = download_song_clip(url, destination, filename_base, clip_start, effective_duration)

    return PreparedSong(
        source_url=url,
        file_path=file_path,
        artist=artist,
        title=title,
        album=album,
        clip_start=clip_start,
        clip_duration=effective_duration,
    )


def prepare_game_songs(
    room_id: str,
    category: str,
    song_count: int = SONGS_PER_GAME,
    clip_duration: int = CLIP_DURATION,
    randomizer: Random | None = None,
) -> list[PreparedSong]:
    """Przygotowuje losowa kolejke utworow dla jednej rozgrywki."""

    randomizer = randomizer or Random()
    room_dir = create_round_directory(room_id)
    category_urls = get_category_urls(category)
    round_urls = choose_round_urls(category_urls, song_count, randomizer=randomizer)

    songs = [
        prepare_song(
            url=url,
            destination=room_dir,
            index=index,
            clip_duration=clip_duration,
            randomizer=randomizer,
        )
        for index, url in enumerate(round_urls, start=1)
    ]
    return songs


def select_round_urls(
    category: str,
    song_count: int = SONGS_PER_GAME,
    randomizer: Random | None = None,
) -> list[str]:
    """Losuje URL-e do jednej rozgrywki bez pobierania audio."""

    urls = get_category_urls(category)
    return choose_round_urls(urls, song_count, randomizer=randomizer)


def get_links(path_file: str | Path) -> list[str]:
    """Odczytuje linki z pliku tekstowego."""

    with Path(path_file).open("r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def download_music(urls: Iterable[str], extension: str, dest_path: str, duration: int = CLIP_DURATION) -> list[str]:
    """Zachowana zgodnosc wsteczna dla starego API pobierania."""

    if extension != "mp3":
        raise ValueError("Only mp3 extension is supported")

    destination = Path(dest_path)
    destination.mkdir(parents=True, exist_ok=True)
    randomizer = Random()
    titles = []
    for index, url in enumerate(urls, start=1):
        prepared_song = prepare_song(url, destination, index, duration, randomizer)
        titles.append(prepared_song.title)
    return titles
