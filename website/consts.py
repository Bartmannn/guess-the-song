"""Stałe wykorzystywane w module.

    :HOST_ADDR: (str) Adres IP serwera.
    :HOST_PORT: (int) Port, na którym została udostępniona gra.
    :HOST_URL: (str) Link, pod którym działa strona.
    :DB_USER: (str) Nazwa użytkownika do bazy danych.
    :DB_PSWD: (str) Hasło użytkownika bazy danych.
    :DB_ADDRESS: (str) Adres IP, na którym działa baza danych.
    :DB_PORT: (int) Port, na którym działa baza danych.
    :DB_NAME: (str) Nazwa bazy danych.
    :URI: (str) Link dostępu do bazy danych.

"""

## importing socket module
from socket import gethostbyname, gethostname

# HOSTING #
HOST_ADDR = f"{gethostbyname(gethostname())}"
HOST_PORT = 5002
HOST_URL = f"https://{HOST_ADDR}:{HOST_PORT}/"

# DATABASE #
DB_USER = "postgres"
DB_PSWD = "Bohdziewicz3"
DB_ADDRESS = "localhost"
DB_PORT = 5432
DB_NAME = "guess_the_song"
URI = f"postgresql://{DB_USER}:{DB_PSWD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"
