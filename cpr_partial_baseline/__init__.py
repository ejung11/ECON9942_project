from otree.api import (
    Page,
    WaitPage,
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random



class Constants(BaseConstants):
    name_in_url = 'ian_cpr_baseline'
    players_per_group = 4
    num_rounds = 3
    endowment = 25


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_harvest = models.CurrencyField()


class Player(BasePlayer):
    harvest = models.CurrencyField(
        min=0, max=Constants.endowment, label="How much will you harvest?"
    )


#FUNCTIONS
#Round setup
def creating_session(subsession):
    # random matching at the beginning of each games
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)
    #check print, comment out after checking
    print('in creating session')
    print('round', subsession.round_number, 'group matrix is', subsession.get_group_matrix())

    #set individual var: total earnings for each participant
    for p in subsession.get_players():
        if subsession.round_number == 1:
            p.participant.vars['totalEarnings'] = 0

#Payoffs
def set_payoffs(g: Group):
    #setup group total harvest
    g.total_harvest = 0
    for p in g.get_players():
        g.total_harvest += p.harvest

    #Earnings for each round
    for p in g.get_players():
        print('payoff', p.participant.payoff)
        print('endowment', Constants.endowment)
        print('harvest', p.harvest)
        print('total harvest', g.total_harvest)

        p.participant.payoff = float(5*(Constants.endowment - p.harvest) + (23*p.harvest - 0.25*g.total_harvest*p.harvest) )

        #Cumulative earnings for each participant
        p.participant.vars['totalEarnings'] += p.participant.payoff
        print('total earnings', p.participant.vars['totalEarnings'])

        #Cash amount
        p.participant.vars['totalCash'] = p.participant.vars['totalEarnings'] / 10




#premature ending of the game (want to make a lottery wheel)
#group.draw = random.uniform(0,100)
#if group.draw <= g.total_harvest:
#   game finishes.
#else:
#   game continues.






# PAGES
class Harvest(Page):
    form_model = 'player'
    form_fields = ['harvest']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    """Players payoff: How much each has earned"""

#class RandomDraw(Page):
#    pass

class PaymentInfo(Page):
    @staticmethod
    def is_displayed(group):
        return group.round_number == Constants.num_rounds

    def vars_for_template(player: Player):
        participant = player.participant
        return dict(redemption_code=participant.label or participant.code)



page_sequence = [
    Harvest,
    ResultsWaitPage,
    Results,
    PaymentInfo,
]