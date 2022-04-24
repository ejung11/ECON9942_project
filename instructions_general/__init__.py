from otree.api import *


doc = """
Instructions for the whole session
"""


class Constants(BaseConstants):
    name_in_url = 'instructions_general'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gq1 = models.StringField(
        choices=[['False', 'A.  100'], ['False', 'B.  150'], ['True', 'C.  200'], ['False', 'D.  250'], ],
        label='1. What is the maximum group total harvest?: (8 players in the group, given 25 efforts each)',
        widget=widgets.RadioSelect,
    )

    gq2 = models.StringField(
        choices=[['False', 'A.  5'], ['False', 'B.  10'], ['False', 'C.  15'], ['True', 'D.  20'], ],
        label='2. What is the maximum number of rounds you can play in the game:',
        widget=widgets.RadioSelect,
    )

    gq3 = models.StringField(
        choices=[['False', 'A.  50'], ['True', 'B.  100'], ['False', 'C.  150'], ['False', 'D.  200'], ],
        label='3. What is the safeline of group total harvest that makes groups automatically play next round:',
        widget=widgets.RadioSelect,
    )

    gq4 = models.StringField(
        choices=[['False', 'A.  Both Practice CPR game A and Practice CPR Game B'],
                 ['False', 'B.  Both Real CPR game A and Real CPR Game B'],
                 ['False', 'C.  One random between Practice CPR game A and Practice CPR Game B'],
                 ['True', 'D.   One random between Real CPR game A and Real CPR Game B'],
                 ],
        label='4. Which game is going to be paid to you at the end of the experiment?:',
        widget=widgets.RadioSelect,
    )


# PAGES
class Page1(Page):
    pass


class Page2(Page):
    pass


class Page3(Page):
    pass


class Page4(Page):
    pass


class Example(Page):
    pass


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['gq1']

    @staticmethod
    def error_message(player, values):
        solution = dict( gq1 = 'True')

        error_messages = dict()

        for field_name in solution:
            if values[field_name] != solution[field_name]:
                error_messages[field_name] = 'Answer is 8 * 25 = C. 200'

        return error_messages


class Quiz2(Page):
    form_model = 'player'
    form_fields = ['gq2']

    @staticmethod
    def error_message(player, values):
        solution = dict( gq2 = 'True')

        error_messages = dict()

        for field_name in solution:
            if values[field_name] != solution[field_name]:
                error_messages[field_name] = 'Answer is D. 20 Rounds. You can play upto 20 rounds.'

        return error_messages


class Quiz3(Page):
    form_model = 'player'
    form_fields = ['gq3']

    @staticmethod
    def error_message(player, values):
        solution = dict(gq3 ='True')

        error_messages = dict()

        for field_name in solution:
            if values[field_name] != solution[field_name]:
                error_messages[field_name] = 'Answer is B. 100.'

        return error_messages


class Quiz4(Page):
    form_model = 'player'
    form_fields = ['gq4']

    @staticmethod
    def error_message(player, values):
        solution = dict(gq4='True')

        error_messages = dict()

        for field_name in solution:
            if values[field_name] != solution[field_name]:
                error_messages[
                    field_name] = 'Answer is D. One random between Real CPR game A and Real CPR Game B.'

        return error_messages


class End(Page):
    pass


page_sequence = [
    Page1,
    Page2,
    Page3,
    Page4,
    Example,
    Quiz1,
    Quiz2,
    Quiz3,
    Quiz4,
    End
]
