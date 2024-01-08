from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_login import logout_user, current_user
from .models import User, User_Room, db
from flask import url_for
from .models import *
from .game_manager import GameManager

socketio = SocketIO()
game_states = {}


@socketio.on("message")
def message(data):
    if data["msg"][0] != "\\":
        send({"msg": data["msg"], "username": data["username"]}, room=data["room"])
    else:
        try:
            game_manager = game_states[data["room"]]
        except KeyError:
            emit("server_info", {"msg": "Game has not been started! Do not guess yet."}, room=data["room"])
        else:
            match game_manager.check_song(data["msg"]):
                case 0:
                    game_manager.add_point(data["username"])
                    emit("server_info", {"msg": f"{data['username']} zgadł/zgadła autora!"}, room=data["room"])
                case 1:
                    game_manager.add_point(data["username"])
                    emit("server_info", {"msg": f"{data['username']} zgadł/zgadła tytuł!"}, room=data["room"])
                case 2:
                    game_manager.add_point(data["username"])
                    emit("server_info", {"msg": f"{data['username']} zgadł/zgadła tytuł dzieła, z którego jest utwór!"}, room=data["room"])
                case 3:
                    info = game_manager.check_similarity(data["msg"])
                    if info != None:
                        emit("server_info", {"msg": info}, room=data["room"])


@socketio.on("join")
def join(data):
    join_room(data["room"])
    send({"msg": data["username"] + " has joined the room."}, room=data["room"])
 
@socketio.on("leave")
def leave(data):
    leave_room(data["room"])
    User_Room.query.filter_by(user_id=current_user.id).delete()
    User.query.filter_by(id=current_user.id).delete()
    logout_user()
    db.session.commit()
    send({"msg": data["username"] + " has left the room."}, room=data["room"])
    list_players(data["room"])

@socketio.on("start")
def start(data):
    game_states[data['room']] = GameManager(data["room"])
    game_states[data['room']].set_cathegory(data["cathegory"])

    room_id = Room.query.filter_by(invitation_link=data["room"]).first().id
    connections = User_Room.query.filter_by(room_id=room_id).all()
    players_ids = [con.user_id for con in connections]
    players_nicknames = [User.query.filter_by(id=id).first().username for id in players_ids]

    for nickname in players_nicknames:
        game_states[data["room"]].add_player(nickname)

    emit("start_game", room=data["room"])
    emit("server_info", {"msg": "Gra rozpoczęta!"}, room=data["room"])
    request_audio(data)

@socketio.on('request_audio')
def request_audio(data):
    next_song = game_states[data['room']].next_song()
    if next_song == None:
        emit("game_over", room=data["room"])
        emit("server_info", {"msg":game_states[data["room"]].get_points()})
    else:
        socketio.emit("server_info", {"msg": f"Runda: {game_states[data['room']].round+1}"}, room=data["room"])
        with open(next_song, 'rb') as audio_file:
            audio_data = audio_file.read()  
            socketio.emit('stream_audio', {'audio_data': audio_data}, room=data["room"])

@socketio.on("repeat_audio")
def repeat_audio(data):
    curr_song = game_states[data["room"]].get_song()
    socketio.emit("server_info", {"msg": f"Repeating song"}, room=data["room"])
    with open(curr_song, 'rb') as audio_file:
            audio_data = audio_file.read()  
            socketio.emit('stream_audio', {'audio_data': audio_data}, room=data["room"])

@socketio.on("list_players")
def list_players(code):
    game = Room.query.filter_by(invitation_link=code).first()
    users_room = User_Room.query.filter_by(room_id=game.id).all()
    ids = [con.user_id for con in users_room]
    usernames = [User.query.filter_by(id=id).first().username for id in ids]
    socketio.emit("list_players", {"players": usernames}, room=code)

    if len(usernames) == 0:
        Room.query.filter_by(invitation_link=code).delete()
        db.session.commit()

@socketio.on("update_state")
def update_state(data):
    state: list
    try:
        state = game_states[data["room"]]
    except KeyError:
        print("\nGame did not start\n")
    else:
        # state.add_player(data["nickname"])
        socketio.emit("update_state", room=data["room"])
        repeat_audio(data)
