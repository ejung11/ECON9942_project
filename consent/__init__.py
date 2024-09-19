from otree.api import *


doc = """
This is the consent app for the project "Managing the Tragedy of the Commons: A Partial Output-Sharing Approach"
This will include Informed Consent for IRB approval.
"""


class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Consent(Page):
    form_model = 'player'
    form_fields = []

class ConsentWaitPage(WaitPage):
    pass



page_sequence = [
    Consent,
                 ]
