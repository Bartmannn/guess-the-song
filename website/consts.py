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

"""
DB_USER = "00888236_guess_the_song"
DB_PSWD = "A84Pp_nH"
DB_ADDRESS = "hosting2353503.online.pro"
DB_PORT = 5432
DB_NAME = "00888236_guess_the_song"
URI = f"postgresql://{DB_USER}:{DB_PSWD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"
"""
