from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length
from .models import User
    

class CreatingGameForm(FlaskForm):

    """Registration form"""

    username = StringField("username_label",
        validators = [
            InputRequired(message="Username required"),
            Length(min=4, max=25, message="Username must be between 4 and 25 characters")
        ]
    )
    submit_new_game = SubmitField("Start")



class JoiningGameForm(FlaskForm):
    """ Login form """

    username = StringField("username_label",
        validators = [
            InputRequired(message="Username required"),
            Length(min=4, max=25, message="Username must be between 4 and 25 characters")
        ]
    )
    link = StringField("link",
        validators = [
            InputRequired(message="Invitation link required")
        ]
    )
    submit_joining_game = SubmitField("Join game")


class JoiningGameFromLinkForm(FlaskForm):

    username = StringField("username_label",
        validators = [
            InputRequired(message="Username required"),
            Length(min=4, max=25, message="Username must be between 4 and 25 characters")
        ]
    )
    submit_joining_game_from_link = SubmitField("Join game")


        