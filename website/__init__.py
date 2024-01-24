from flask import Flask
from .consts import URI
from .models import *
from flask_socketio import SocketIO
from .communication import *
from .views import login

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "DowolnyKluczPRYWATNY561835818356"
    app.config["SQLALCHEMY_DATABASE_URI"] = URI
    db.init_app(app)
    socketio.init_app(app)
    login.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return socketio, app
