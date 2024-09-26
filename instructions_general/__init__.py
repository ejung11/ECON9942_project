from otree.api import *


doc = """
This is the general instructions app for the project "Managing the Tragedy of the Commons: A Partial Output-Sharing Approach"
This will include instructions for the whole session.
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
    pass



# PAGES
class Introduction(Page):
    pass


page_sequence = [
    Introduction,
]
