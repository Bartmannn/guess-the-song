from website import create_app
from website.consts import HOST_PORT

socketio, app = create_app()
if __name__ == "__main__":
    # wymagana biblioteka pyopenssl 
    socketio.run(app, debug=True, host="0.0.0.0", port=HOST_PORT, ssl_context="adhoc")