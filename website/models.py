from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):

    """ User model """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    is_admin = db.Column(db.Boolean)


class User_Room(db.Model):

    """ User-Room relation model """

    __tablename__ = "user_room"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer) # , db.ForeignKey("rooms.id")
    user_id = db.Column(db.Integer) # , db.ForeignKey("users.id")


class Room(db.Model):

    """ Room model """

    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    # chat_id = db.Column(db.Integer, db.ForeignKey("messages.id"))
    invitation_link = db.Column(db.String(100), unique=True)

class Room_Message(db.Model):

    """ Room-Messages relation model """

    __tablename__ = "room_message"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer) # db.ForeignKey("rooms.is")
    message_id = db.Column(db.Integer) # db.ForeignKey("messages.id")


class Message(db.Model):

    """ Chat model """
    
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(30))
    message = db.Column(db.Text)

class Song_Room(db.Model):

    """ Song-Server relation model """

    __tablename__ = "song_room"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer) # , db.ForeignKey("rooms.id")
    song_id = db.Column(db.Integer) # , db.ForeignKey("songs.id")
    
class Songs(db.Model):

    """ Songs model """

    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(150))
    category = db.Column(db.String(10))

