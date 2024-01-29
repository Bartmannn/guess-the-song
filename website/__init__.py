from flask import Flask
from .consts import URI
from .models import *
from flask_socketio import SocketIO
from .communication import *
from .views import login


def create_app() -> set:
    """Inicjowanie aplikacji internetowej.
    
    :return: Obiekt odpowiadający za nasłuchiwanie portów oraz obiekt aplikacji
             internetowej (flask_socketio.SocketIO, flask.app.Flask).
    :rtype: set

    """

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "DowolnyKluczPRYWATNY561835818356"
    app.config["SQLALCHEMY_DATABASE_URI"] = URI

    db.init_app(app)
    socketio.init_app(app)
    login.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    # print(f"\n\nsocketio: {type(socketio)} | app: {type(app)}")

    return socketio, app
