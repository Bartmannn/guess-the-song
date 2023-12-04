from flask_socketio import SocketIO, send, emit, join_room, leave_room

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
    send({"msg": data["username"] + " has left the room."}, room=data["room"])

