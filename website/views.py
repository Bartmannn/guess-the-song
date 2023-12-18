from flask import Blueprint, render_template, redirect, url_for, Response, request
from .downloader import download_music
from .wtform_fields import *
from .models import *
from .consts import HOST_URL
from random import randint
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import sys
from game_manager import Game_manager
views = Blueprint("views", __name__)
login  = LoginManager()

game_states = {}

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@views.route("/", methods=["GET", "POST"])
def home():

    new_game_form = CreatingGameForm()

    if new_game_form.submit_new_game.data and new_game_form.validate():
        print("New Game", file=sys.stderr)
        username = new_game_form.username.data

        user = User(username=username, is_admin=True)
        db.session.add(user)

        server_id = ""
        for i in range(15):
            match randint(0, 2):
                case 0:
                    server_id += f"{randint(0, 9)}"
                case 1:
                    server_id += f"{chr(randint(65, 90))}"
                case 2:
                    server_id += f"{chr(randint(65, 90))}".lower()
        new_game = Room(invitation_link=server_id)
        db.session.add(new_game)

        test = Room.query.filter_by(invitation_link=server_id).first()

        print("\n\n", new_game.id, " ", user.id)
        relation = User_Room(room_id=new_game.id, user_id=user.id)
        db.session.add(relation)

        db.session.commit()
        
        game_states[server_id] = Game_manager(server_id)

        login_user(user)
        return redirect(url_for("views.new_game", game_id=server_id, is_admin=True))

    return render_template("index.html", creating_game=new_game_form)

@views.route("/<game_id>", methods=["GET", "POST"])
def new_game(game_id):
    if current_user.is_authenticated:
        is_admin = User.query.filter_by(id=current_user.id).first().is_admin
        print(is_admin)
        return render_template("game_room.html", room_name=game_id, invite_link=HOST_URL+game_id, code=game_id, username=current_user.username, is_admin=is_admin)

    joining_form = JoiningGameForm()
    if joining_form.submit_joining_game.data and joining_form.validate():
        username = joining_form.username.data
        code = joining_form.link.data

        user = User(username=username, is_admin=False)
        db.session.add(user)

        room = Room.query.filter_by(invitation_link=code).first()
        if room == None:
            return "Game does not exist"

        relation = User_Room(room_id=room.id, user_id=user.id)
        db.session.add(relation)
        db.session.commit()

        login_user(user)
        return redirect(url_for("views.new_game", game_id=code))

    return render_template("log_to_room.html", room_name=game_id, joining_game=joining_form)
    
