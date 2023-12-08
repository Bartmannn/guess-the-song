## importing socket module
from socket import gethostbyname, gethostname

# HOSTING #
HOST_ADDR = f"{gethostbyname(gethostname())}"
HOST_PORT = 5000
HOST_URL = f"http://{HOST_ADDR}:{HOST_PORT}/"


# DATABASE #
DB_USER = "postgres"
DB_PSWD = "Bohdziewicz3"
DB_ADDRESS = "localhost"
DB_PORT = 5432
DB_NAME = "guess_the_song"
URI = f"postgresql://{DB_USER}:{DB_PSWD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"