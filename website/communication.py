"""Komunikacja serwer <-> uzytkownik."""

from __future__ import annotations

from threading import Lock

from flask_login import current_user, logout_user
from flask_socketio import SocketIO, emit, join_room, leave_room, send

from .consts import SONGS_PER_GAME
from .game_manager import GameManager
from .models import Room, User, User_Room, db


socketio = SocketIO(async_mode="threading")
game_states: dict[str, GameManager] = {}
preparing_rooms: set[str] = set()
state_lock = Lock()


def cleanup_room_state(room_code: str) -> None:
    """Czyści stan gry i pliki audio przypisane do pokoju."""

    game_manager = game_states.pop(room_code, None)
    if game_manager is not None:
        game_manager.cleanup()
    preparing_rooms.discard(room_code)


def get_room_player_names(room_code: str) -> list[str]:
    """Pobiera nicki graczy aktualnie przypisanych do pokoju."""

    room = Room.query.filter_by(invitation_link=room_code).first()
    if room is None:
        return []

    connections = User_Room.query.filter_by(room_id=room.id).all()
    players_ids = [connection.user_id for connection in connections]
    return [User.query.filter_by(id=user_id).first().username for user_id in players_ids]


def emit_preparing_message(room_code: str, message: str) -> None:
    """Wysyła komunikat o przygotowywaniu utworu."""

    socketio.emit("preparing_game", {"msg": message}, room=room_code)
    socketio.emit("server_info", {"msg": message}, room=room_code)


def emit_current_song(room_code: str) -> None:
    """Wysyła aktualnie przygotowany utwór do pokoju."""

    game_manager = game_states.get(room_code)
    if game_manager is None:
        socketio.emit("server_info", {"msg": "Game has not been started yet."}, room=room_code)
        return

    current_song = game_manager.get_song()
    if current_song is None:
        socketio.emit("server_info", {"msg": "No song is ready right now."}, room=room_code)
        return

    socketio.emit("server_info", {"msg": f"Round {game_manager.round}/{game_manager.total_rounds}."}, room=room_code)
    with open(current_song, "rb") as audio_file:
        audio_data = audio_file.read()
        socketio.emit("stream_audio", {"audio_data": audio_data}, room=room_code)


def prepare_initial_song_for_room(room_code: str, category: str, player_names: list[str]) -> None:
    """Przygotowuje pierwszy utwór dla nowej gry."""

    try:
        game_manager = GameManager(room_code)
        for player_name in player_names:
            game_manager.add_player(player_name)
        game_manager.start_new_game(category)
        prepared_song = game_manager.prepare_next_song()
        if prepared_song is None:
            if game_manager.last_prepare_error is not None:
                raise ValueError(f"No playable songs could be prepared. Last error: {game_manager.last_prepare_error}")
            raise ValueError("No songs could be prepared for this room.")
    except Exception as error:
        cleanup_room_state(room_code)
        socketio.emit("prepare_failed", {"msg": f"Could not prepare songs: {error}"}, room=room_code)
        socketio.emit("server_info", {"msg": f"Could not prepare songs: {error}"}, room=room_code)
        return

    with state_lock:
        game_states[room_code] = game_manager
        preparing_rooms.discard(room_code)

    socketio.emit("start_game", room=room_code)
    emit_current_song(room_code)


def advance_round_for_room(room_code: str) -> None:
    """Kończy bieżącą rundę i przygotowuje kolejną."""

    game_manager = game_states.get(room_code)
    if game_manager is None:
        preparing_rooms.discard(room_code)
        socketio.emit("prepare_failed", {"msg": "Game has not been started yet."}, room=room_code)
        socketio.emit("server_info", {"msg": "Game has not been started yet."}, room=room_code)
        return

    try:
        round_summary = game_manager.finish_current_round()
        if round_summary is not None:
            socketio.emit("server_info", {"msg": round_summary}, room=room_code)

        if not game_manager.has_more_songs():
            socketio.emit("game_over", room=room_code)
            socketio.emit("server_info", {"msg": game_manager.get_points()}, room=room_code)
            cleanup_room_state(room_code)
            return

        prepared_song = game_manager.prepare_next_song()
        if prepared_song is None:
            if game_manager.last_prepare_error is not None:
                socketio.emit(
                    "server_info",
                    {"msg": "The remaining songs could not be played. Ending the game with the current score."},
                    room=room_code,
                )
                socketio.emit("game_over", room=room_code)
                socketio.emit("server_info", {"msg": game_manager.get_points()}, room=room_code)
                cleanup_room_state(room_code)
                return
            socketio.emit("game_over", room=room_code)
            socketio.emit("server_info", {"msg": game_manager.get_points()}, room=room_code)
            cleanup_room_state(room_code)
            return
    except Exception as error:
        cleanup_room_state(room_code)
        socketio.emit("prepare_failed", {"msg": f"Could not prepare the next song: {error}"}, room=room_code)
        socketio.emit("server_info", {"msg": f"Could not prepare the next song: {error}"}, room=room_code)
        return

    with state_lock:
        preparing_rooms.discard(room_code)

    emit_current_song(room_code)


@socketio.on("message")
def message(data: dict) -> None:
    """Przyjmuje wysyłane wiadomości na czacie i je przetwarza."""

    if data["msg"][0] != "\\":
        send({"msg": data["msg"], "username": data["username"]}, room=data["room"])
        return

    game_manager = game_states.get(data["room"])
    if game_manager is None:
        if data["room"] in preparing_rooms:
            emit("server_info", {"msg": "Song is being prepared. Wait a moment."}, room=data["room"])
        else:
            emit("server_info", {"msg": "Game has not been started yet. Do not guess yet."}, room=data["room"])
        return

    match game_manager.check_song(data["msg"]):
        case 0:
            game_manager.add_point(data["username"])
            emit("server_info", {"msg": f"{data['username']} guessed the artist."}, room=data["room"])
        case 1:
            game_manager.add_point(data["username"])
            emit("server_info", {"msg": f"{data['username']} guessed the title."}, room=data["room"])
        case 2:
            game_manager.add_point(data["username"])
            emit(
                "server_info",
                {"msg": f"{data['username']} guessed the album or source title."},
                room=data["room"],
            )
        case 3:
            info = game_manager.check_similarity(data["msg"])
            if info is not None:
                emit("server_info", {"msg": info}, room=data["room"])


@socketio.on("join")
def join(data: dict) -> None:
    """Dolacza gracza do pokoju."""

    join_room(data["room"])
    send({"msg": data["username"] + " has joined the room."}, room=data["room"])


@socketio.on("leave")
def leave(data: dict) -> None:
    """Obsluguje wyjscie gracza z pokoju."""

    leave_room(data["room"])
    User_Room.query.filter_by(user_id=current_user.id).delete()
    User.query.filter_by(id=current_user.id).delete()
    logout_user()
    db.session.commit()
    send({"msg": data["username"] + " has left the room."}, room=data["room"])
    list_players(data["room"])


@socketio.on("start")
def start(data: dict) -> None:
    """Rozpoczyna przygotowanie nowej gry w pokoju."""

    room_code = data["room"]
    category = data["cathegory"]

    with state_lock:
        if room_code in preparing_rooms:
            emit("server_info", {"msg": "Song is already being prepared."}, room=room_code)
            return
        cleanup_room_state(room_code)
        preparing_rooms.add(room_code)

    player_names = get_room_player_names(room_code)
    emit_preparing_message(
        room_code,
        f"Preparing first song for a {SONGS_PER_GAME}-round game. This may take a moment.",
    )
    socketio.start_background_task(prepare_initial_song_for_room, room_code, category, player_names)


@socketio.on("request_audio")
def request_audio(data: dict) -> None:
    """Kończy bieżącą rundę i rozpoczyna przygotowanie kolejnej."""

    room_code = data["room"]
    with state_lock:
        if room_code in preparing_rooms:
            emit("server_info", {"msg": "Wait for the next song to finish preparing."}, room=room_code)
            return
        if room_code not in game_states:
            emit("server_info", {"msg": "Game has not been started yet."}, room=room_code)
            return
        preparing_rooms.add(room_code)

    emit_preparing_message(room_code, "Closing current round and preparing the next song.")
    socketio.start_background_task(advance_round_for_room, room_code)


@socketio.on("repeat_audio")
def repeat_audio(data: dict) -> None:
    """Powtarza aktualny utwór w pokoju."""

    game_manager = game_states.get(data["room"])
    if game_manager is None:
        emit("server_info", {"msg": "Game has not been started yet."}, room=data["room"])
        return

    curr_song = game_manager.get_song()
    if curr_song is None:
        emit("server_info", {"msg": "No song is active yet."}, room=data["room"])
        return

    socketio.emit("server_info", {"msg": "Repeating the current song."}, room=data["room"])
    with open(curr_song, "rb") as audio_file:
        audio_data = audio_file.read()
        socketio.emit("stream_audio", {"audio_data": audio_data}, room=data["room"])


@socketio.on("list_players")
def list_players(code: str) -> None:
    """Odswieza listę graczy w pokoju."""

    game = Room.query.filter_by(invitation_link=code).first()
    if game is None:
        cleanup_room_state(code)
        return

    users_room = User_Room.query.filter_by(room_id=game.id).all()
    ids = [connection.user_id for connection in users_room]
    usernames = [User.query.filter_by(id=user_id).first().username for user_id in ids]
    socketio.emit("list_players", {"players": usernames}, room=code)

    if len(usernames) == 0:
        Room.query.filter_by(invitation_link=code).delete()
        db.session.commit()
        cleanup_room_state(code)


@socketio.on("update_state")
def update_state(data: dict) -> None:
    """Synchronizuje stan gry po dołączeniu nowego gracza."""

    room_code = data["room"]
    if room_code in preparing_rooms:
        socketio.emit(
            "preparing_game",
            {"msg": "Song is still being prepared for this room."},
            room=room_code,
        )
        return

    if room_code not in game_states:
        return

    socketio.emit("update_state", room=room_code)
    repeat_audio(data)
