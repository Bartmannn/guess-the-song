from flask import Blueprint, render_template, redirect, url_for, Response, request
from .downloader import download_music
from .wtform_fields import *
from .models import *
from .consts import HOST_URL
from random import randint
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import sys

views = Blueprint("views", __name__)
login  = LoginManager()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@views.route("/", methods=["GET", "POST"])
def home():

    new_game_form = CreatingGameForm()
    joining_form = JoiningGameForm()

    if new_game_form.submit_new_game.data and new_game_form.validate():
        print("New Game", file=sys.stderr)
        username = new_game_form.username.data

        user = User(username=username, is_admin=True)
        db.session.add(user)

        invitation_link = HOST_URL
        server_id = ""
        for i in range(15):
            match randint(0, 2):
                case 0:
                    server_id += f"{randint(0, 9)}"
                case 1:
                    server_id += f"{chr(randint(65, 90))}"
                case 2:
                    server_id += f"{chr(randint(65, 90))}".lower()
        new_game = Room(invitation_link=invitation_link+server_id)
        db.session.add(new_game)

        relation = User_Room(room_id=new_game.id, user_id=user.id)
        db.session.add(relation)

        db.session.commit()

        login_user(user)
        return redirect(url_for("views.new_game", game_id=server_id))

    if joining_form.submit_joining_game.data and joining_form.validate():
        print("Joining Game", file=sys.stderr)
        username = joining_form.username.data
        link = joining_form.link.data

        user = User(username=username, is_admin=False)
        db.session.add(user)

        room = Room.query.filter_by(invitation_link=link).first()
        print(room.id, link)
        if room == None:
            return "Game does not exist"

        relation = User_Room(room_id=room.id, user_id=user.id)
        db.session.add(relation)
        db.session.commit()

        login_user(user)
        return redirect(url_for("views.new_game", game_id=link[-15::]))

    return render_template("index.html", creating_game=new_game_form, joining_game=joining_form)

@views.route("/<game_id>", methods=["GET", "POST"])
def new_game(game_id):
    return render_template("game_room.html", room_name=game_id, invite_link=HOST_URL+game_id, username=current_user.username)


# @views.route("/mp3")
# def streamp3():

#     links = request.args["link"]
#     links = links.replace(" ", "").split(",")
#     dest_path = "./website/static/music/"
#     ext = "mp3"
#     titles = download_music(links, ext, dest_path, 15)
    
#     def generate(path=dest_path, titles=titles, ext=ext):
#         for title in titles:
#             with open(f"{path}{title}.{ext}", "rb") as fmp3:
#                 data = fmp3.read(1024)
#                 while data:
#                     yield data
#                     data = fmp3.read(1024)
#     return Response(generate(), mimetype="audio/mp3")