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
    print(f"\n\n{data}\n\n")
    send({"msg": data["msg"], "username": data["username"]}, room=data["room"])
    info = ""
    match game_states[data["room"]].check_song(data["msg"]):
        case 0:
            emit("server_info", {"msg": "Zgadłeś autora!"}, room=data["room"])
        case 1:
            emit("server_info", {"msg": "Zgadłeś tytuł!"}, room=data["room"])
        case 2:
            emit("server_info", {"msg": "Zgadłeś wystąpienie utworu!"}, room=data["room"])

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
    emit("start_game", room=data["room"])
    emit("server_info", {"msg": "Gra rozpoczęta!"}, room=data["room"])
    request_audio(data)

@socketio.on('request_audio')
def request_audio(data):
    next_song = game_states[data['room']].next_song()
    if next_song == None:
        emit("game_over", room=data["room"])
    else:
        socketio.emit("server_info", {"msg": f"Runda: {game_states[data['room']].round+1}"}, room=data["room"])
        with open(next_song, 'rb') as audio_file:
            audio_data = audio_file.read()  
            socketio.emit('stream_audio', {'audio_data': audio_data}, room=data["room"])

@socketio.on("list_players")
def list_players(code):
    game = Room.query.filter_by(invitation_link=code).first()
    users_room = User_Room.query.filter_by(room_id=game.id).all()
    ids = [con.user_id for con in users_room]
    usernames = [User.query.filter_by(id=id).first().username for id in ids]
    socketio.emit("list_players", {"players": usernames}, room=code)

    print(f"\n{code}\n{game}\n{users_room}\n{ids}\n{usernames}\n")

    if len(usernames) == 0:
        Room.query.filter_by(invitation_link=code).delete()
        db.session.commit()
