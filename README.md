# Guess The Song

Multiplayer browser quiz game built with Flask and Socket.IO.

Players join a shared room, pick a music category, and try to identify the currently playing song by artist, title, or source. The game streams short audio clips prepared on demand from YouTube with `yt-dlp`, so the project does not rely on a large pre-generated local music library.


## Demo

https://github.com/user-attachments/assets/b09ab11e-1dab-485c-a847-a068de9837d7

## What Makes This Project Different

- Dynamic song preparation with `yt-dlp` and `ffmpeg`
- Multiplayer rooms with invite links
- Real-time communication over Socket.IO
- Round-based gameplay with score tracking
- Automatic cleanup of downloaded audio files after each round
- Docker support for reproducible setup

## How It Works

1. The host creates a room and shares the invite link.
2. Players join the room in the browser.
3. The host selects a category: `Modern`, `Films`, or `Games`.
4. On `Start`, the app pulls a list of songs from a configured YouTube playlist.
5. A single random clip is downloaded for the current round.
6. On `Next`, the round is closed, the correct answer is revealed, the old clip is deleted, and the next one is prepared.

This keeps the game responsive and limits disk usage on the server.

## Tech Stack

- Python 3.12
- Flask
- Flask-SocketIO
- Flask-SQLAlchemy
- WTForms
- yt-dlp
- ffmpeg
- Docker / Docker Compose

## Project Structure

```text
.
|-- main.py
|-- docker-compose.yml
|-- Dockerfile
|-- requirements.txt
|-- website/
|   |-- communication.py
|   |-- downloader.py
|   |-- game_manager.py
|   |-- models.py
|   |-- templates/
|   |-- static/
|   `-- tests/
```

## Categories and Playlists

Music sources are configured in category files:

- `website/static/music/modern/modern.txt`
- `website/static/music/films/films.txt`
- `website/static/music/games/games.txt`

Each file can contain direct YouTube links or a playlist URL. The current version uses playlist-based sources for all three categories.

## Running with Docker

The fastest way to start the project is with Docker:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:5002
```

## Running Locally

Requirements:

- Python 3.12
- `ffmpeg`
- `nodejs` or another JS runtime supported by `yt-dlp`

Install dependencies:

```bash
python -m venv virtual
source virtual/bin/activate
python -m pip install -r requirements.txt
```

Start the app:

```bash
python main.py
```

## Configuration

The app can be configured with environment variables.

Important variables:

- `APP_HOST`
- `APP_PORT`
- `APP_DEBUG`
- `APP_USE_SSL`
- `SECRET_KEY`
- `DATABASE_URL`
- `SONGS_PER_GAME`
- `CLIP_DURATION`

Default local setup uses SQLite stored in `data/guess_the_song.db`.

## Testing

Run unit tests with:

```bash
python -m unittest discover -s website/tests -p 'test*.py' -v
```

## Notes

- The game downloads audio clips on demand, so network access is required during gameplay.
- Some videos on YouTube may become unavailable. The game is designed to skip broken entries and continue when possible.
- Rebuilding the Docker image is recommended after dependency changes:

```bash
docker compose up --build
```
