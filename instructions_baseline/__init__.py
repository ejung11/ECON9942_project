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
    pass


# PAGES
class Page1(Page):
    pass


class Page2(Page):
    pass


class Page3(Page):
    pass


class Page4(Page):
    pass


class Page5(Page):
    pass


class Page6(Page):
    pass


class Page7(Page):
    pass


class Page8(Page):
    pass


class Page9(Page):
    pass


class Page10(Page):
    pass


class Page11(Page):
    pass


page_sequence = [
    Page1,
    Page2,
    Page3,
    Page4,
    Page5,
    Page6,
    Page7,
    Page8,
    Page9,
    Page10,
    Page11
]
