from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length
from .models import User
    

class CreatingGameForm(FlaskForm):

    """Formularz do zainicjowania nowej gry.
    
        :username: (wtforms.fields.core.UnboundField) Obiekt pola tekstowego do wprowadzania nazwy użytkownika.
        :submit_new_game: (wtforms.fields.core.UnboundField) Obiekt przycisku do zatwierdzania nazwy i stworzenia nowej gry.

    """

    username = StringField("username_label",
        validators = [
            InputRequired(message="Username required"),
            Length(min=4, max=25, message="Username must be between 4 and 25 characters")
        ]
    )
    submit_new_game = SubmitField("Start")
    # print(f"\n\nInput: {type(username)} | Przycisk: {type(submit_new_game)} | Creating Game Form")



# class JoiningGameForm(FlaskForm):
#     """ Login form """

#     username = StringField("username_label",
#         validators = [
#             InputRequired(message="Username required"),
#             Length(min=4, max=25, message="Username must be between 4 and 25 characters")
#         ]
#     )
#     link = StringField("link",
#         validators = [
#             InputRequired(message="Invitation link required")
#         ]
#     )
#     submit_joining_game = SubmitField("Join game")

#     print(f"\n\nInput: {type(username)} | Przycisk: {type(submit_new_game)} | Creating Game Form")

class JoiningGameFromLinkForm(FlaskForm):

    """Formularz do dołączania do istniejących gier.
    
        :username: (wtforms.fields.core.UnboundField) Obiekt pola tekstowego do wprowadzania nazwy użytkownika.
        :submit_joining_game: (wtforms.fields.core.UnboundField) Obiekt przycisku do zatwierdzania nazwy i dołączenia.

    """
    
    username = StringField("username_label",
        validators = [
            InputRequired(message="Username required"),
            Length(min=4, max=25, message="Username must be between 4 and 25 characters")
        ]
    )
    submit_joining_game = SubmitField("Join game")
    # print(f"\n\nInput: {type(username)} | Przycisk: {type(submit_joining_game_from_link)} | Joining Game Form")



# class JoiningGameFromLinkForm(FlaskForm):

#     username = StringField("username_label",
#         validators = [
#             InputRequired(message="Username required"),
#             Length(min=4, max=25, message="Username must be between 4 and 25 characters")
#         ]
#     )
#     submit_joining_game_from_link = SubmitField("Join game")

#     print(f"\n\nInput: {type(username)} | Przycisk: {type(submit_new_game)} | Creating Game Form")


        