from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_login import logout_user, current_user
from .models import User, User_Room, db
from flask import url_for
from .models import *
from views import game_states
socketio = SocketIO()

def get_titles(path: str) -> list:
    from os import listdir
    res = listdir(path)
    titles = []
    print(res)
    for title in res:
        print(title, " ", title.split("."))
        if "mp3" in title.split("."):
            titles.append(title)
    # titles = [title in title in res]
    return titles


@socketio.on("message")
def message(data):
    print(f"\n\n{data}\n\n")
    if game_states[data["room"]].check_song(int(data["round"]), data["msg"]):
        print("zgadłes!!!!!")
    else:
        print("niezgadles ;((")
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
def handle_request_audio(data):
    musics_folder = f"./website/static/music/{data['cathegory']}/"
    # songs_titles = ["Armaty.mp3", "Enough.mp3", "Początek.mp3", "Świt.mp3", "Venger.mp3", "Write This Down.mp3", "Wroclove.mp3"]
    
    songs_titles = get_titles(musics_folder.replace("/", "\\")) # Auto branie utworów z pliq
    audio_path = "{0}{1}".format(musics_folder, songs_titles[data["round"]%len(songs_titles)]) # TODO: TYMCZASOWE ROZWIĄZANIE!
    with open(audio_path, 'rb') as audio_file:
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
