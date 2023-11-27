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
    submit_button = SubmitField("Start")



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
    submit_button = SubmitField("Join game")


        