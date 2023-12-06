from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_login import logout_user, current_user
from .models import User, User_Room, db
from flask import url_for
from .models import *

socketio = SocketIO()

@socketio.on("message")
def message(data):
    print(f"\n\n{data}\n\n")
    send({"msg": data["msg"], "username": data["username"]}, room=data["room"])

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

@socketio.on('request_audio')
def handle_request_audio():
    audio_path = "./website/static/music/Armaty.mp3" # url_for("static", "music/Armaty.mp3")
    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()
        socketio.emit('stream_audio', {'audio_data': audio_data})

@socketio.on("list_players")
def list_players(code):
    game = Room.query.filter_by(invitation_link=code).first()
    users_room = User_Room.query.filter_by(room_id=game.id).all()
    ids = [con.user_id for con in users_room]
    usernames = [User.query.filter_by(id=id).first().username for id in ids]
    socketio.emit("list_players", {"players": usernames, "code": code})
    print(f"\n{code}\n{game}\n{users_room}\n{ids}\n{usernames}\n");
    if len(usernames) == 0:
        Room.query.filter_by(invitation_link=code).delete()
        db.session.commit()
