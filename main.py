from website import create_app

socketio, app = create_app()
# socketio = get_socketio()

if __name__ == "__main__":
    socketio.run(app, debug=True)