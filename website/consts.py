"""Stałe i konfiguracja aplikacji.

Moduł nie wykonuje już operacji sieciowych podczas importu, dzięki czemu
aplikacja uruchamia się poprawnie lokalnie i w kontenerze.
"""

from os import getenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def get_bool_env(name: str, default: bool) -> bool:
    """Parsuje zmienną środowiskową do wartości logicznej."""

    value = getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# HOSTING #
HOST_ADDR = getenv("APP_HOST", "0.0.0.0")
HOST_PORT = int(getenv("APP_PORT", "5002"))
PUBLIC_HOST = getenv("PUBLIC_HOST", "localhost")
PUBLIC_PORT = int(getenv("PUBLIC_PORT", str(HOST_PORT)))
USE_SSL = get_bool_env("APP_USE_SSL", False)
PUBLIC_SCHEME = getenv("PUBLIC_SCHEME", "https" if USE_SSL else "http")
HOST_URL = getenv("HOST_URL", f"{PUBLIC_SCHEME}://{PUBLIC_HOST}:{PUBLIC_PORT}/")
DEBUG = get_bool_env("APP_DEBUG", False)
ALLOW_UNSAFE_WERKZEUG = get_bool_env("ALLOW_UNSAFE_WERKZEUG", True)
SECRET_KEY = getenv("SECRET_KEY", "change-me-in-production")

# DATABASE #
DEFAULT_SQLITE_PATH = BASE_DIR / "data" / "guess_the_song.db"
DEFAULT_SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
GENERATED_AUDIO_DIR = BASE_DIR / "data" / "game_audio"
GENERATED_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

DB_USER = getenv("DB_USER", "postgres")
DB_PSWD = getenv("DB_PSWD", "postgres")
DB_ADDRESS = getenv("DB_ADDRESS", "localhost")
DB_PORT = int(getenv("DB_PORT", "5432"))
DB_NAME = getenv("DB_NAME", "guess_the_song")
SONGS_PER_GAME = int(getenv("SONGS_PER_GAME", "10"))
CLIP_DURATION = int(getenv("CLIP_DURATION", "15"))
URI = getenv(
    "DATABASE_URL",
    f"sqlite:///{DEFAULT_SQLITE_PATH}",
)
