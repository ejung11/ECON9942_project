from otree.api import *


doc = """
This is the Practice app for Part 2 High Treatment (Tr60) of 
the project "Managing the Tragedy of the Commons: A Partial Output-Sharing Approach"
This will include practice, Harvest, Results.
"""


class C(BaseConstants):
    NAME_IN_URL = 'cpr_partial_60_p'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
