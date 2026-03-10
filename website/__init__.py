from flask import Flask
from .consts import SECRET_KEY, URI
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
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    socketio.init_app(app)
    login.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    with app.app_context():
        db.create_all()

    return socketio, app
