from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Model użytkownika

        :id: Id użytkownika.
        :username: Nazwa użytkownika.
        :is_admin: Czy użytkownika jest administratorem gry.
    
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    is_admin = db.Column(db.Boolean)


class User_Room(db.Model):
    """Model Użytkownik-Pokój (dla relacji)
    
        :id: Id relacji.
        :room_id: Id pokoju.
        :user_id: Id użytkownika.
    
    """

    __tablename__ = "user_room"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id")) # 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id")) # 


class Room(db.Model):
    """Model pokoju
    
        :id: Id pokoju.
        :invitation_link: Nazwa pokoju.
    
    """

    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    # chat_id = db.Column(db.Integer, db.ForeignKey("messages.id"))
    invitation_link = db.Column(db.String(100), unique=True)
