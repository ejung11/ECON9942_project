from otree.api import *


doc = """
This is the intro app for Game 1 of 
the project "Managing the Tragedy of the Commons: A Partial Output-Sharing Approach"
This will include Instructions, Example, KnowledgeCheck Pages.
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro_baseline'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # KnowledgeCheck questions
    kc1 = models.StringField(
        choices=[['False', 'A.  2'], ['False', 'B.  4'], ['False', 'C.  6'], ['True', 'D.  8'], ],
        label='1. How many people are in your group during the experiment?',
        widget=widgets.RadioSelect,
    )

    kc2 = models.StringField(
        choices=[['True', 'A.  Remain the same'], ['False', 'B.  Mixed'],],
        label='2. Will your group remain the same or be mixed between games?',
        widget=widgets.RadioSelect,
    )

    kc3 = models.StringField(
        choices=[['False', 'A.  5'], ['True', 'B.  10'], ['False', 'C.  15'], ['False', 'D.  20'], ],
        label='3. How many rounds will you play in the game?',
        widget=widgets.RadioSelect,
    )

    kc4 = models.StringField(
        choices=[['False', 'A.  10 efforts'],
                 ['False', 'B.  15 efforts'],
                 ['False', 'C.  20 efforts'],
                 ['True', 'D.  25 efforts'],
                 ],
        label='4. How many efforts are you given each round to allocate between activities?',
        widget=widgets.RadioSelect,
    )

    kc5 = models.StringField(
        choices=[['False', 'A.  2 ECUs per effort'],
                 ['False', 'B.  3 ECUs per effort'],
                 ['True', 'C.  5 ECUs per effort'],
                 ['False', 'D.  10 ECUs per effort'],
                 ],
        label='5. What is the return for each effort you allocate to Activity A?',
        widget=widgets.RadioSelect,
    )

    kc6 = models.StringField(
        choices=[['False', 'A.  Your own allocation only'],
                 ['False', 'B.  Others effort allocated to Activity B only'],
                 ['True', 'C.  The total effort allocated to Activity B by the entire group'],
                 ['False', 'D.  The number of rounds played'],
                 ],
        label='6. What affects the return for each effort allocated to Activity B?',
        widget=widgets.RadioSelect,
    )

    kc7 = models.StringField(
        choices=[['True', 'A.  The sum of your earnings from all rounds.'],
                 ['False', 'B.  The earnings from just the final round.'],
                 ['False', 'C.  A random round will be selected, and only the earnings from that round.'],
                 ['False', 'D.  A fixed amount of money, regardless of your performance.'],
                 ],
        label='7. How will your final payoff in the experiment be calculated?',
        widget=widgets.RadioSelect,
    )


# PAGES
class Instructions(Page):
    pass


class Example(WaitPage):
    pass


class KnowledgeCheck(Page):
    form_model = 'player'
    form_fields = [
        'kc1',
        'kc2',
        'kc3',
        'kc4',
        'kc5',
        'kc6',
        'kc7',
                   ]

    @staticmethod
    def error_message(player, values):
        solution = dict(
            kc1='True',
            kc2='True',
            kc3='True',
            kc4='True',
            kc5='True',
            kc6='True',
            kc7='True',
        )

        # Define specific error messages for each question
        error_messages = dict(
            kc1="You will be randomly assigned to a group of 8 people.",
            kc2="Your group will remain the same throughout the games.",
            kc3="There are 10 rounds in the game.",
            kc4="You are given 25 efforts in every round to allocate between activities.",
            kc5="The return for each effort in Activity A is 5 ECUs.",
            kc6="The return for Activity B is affected by the total effort allocated by the entire group.",
            kc7="Your final payoff will be the sum of your earnings from all rounds."
        )

        # Prepare the final error messages for display if a wrong answer is selected
        final_errors = {}
        for field_name, correct_value in solution.items():
            if values[field_name] != correct_value:
                final_errors[field_name] = error_messages[field_name]

        return final_errors


page_sequence = [
    Instructions,
    Example,
    KnowledgeCheck,
]
