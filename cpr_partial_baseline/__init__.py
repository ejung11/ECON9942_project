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
    players_per_group = 2
    num_rounds = 3
    endowment = 25
    conversion = 0.01


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_harvest = models.IntegerField()
    prob_ending = models.IntegerField()
    #need to implement function
    destruction = models.IntegerField()
    end = models.BooleanField(
        initial = False, doc = """Indicates whether the game will continue or end"""
    )


class Player(BasePlayer):
    harvest = models.IntegerField(
        min=0, max=Constants.endowment, label="How much will you harvest?",
    )
    history_accumulated_earnings = models.FloatField()
    period_payoff = models.FloatField()
    end = models.BooleanField(
        initial = False, doc = """Indicates whether the game will continue or end"""
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
    #print('in creating session')
    #print('round', subsession.round_number, 'group matrix is', subsession.get_group_matrix())

    #set individual var: total earnings for each participant
    for p in subsession.get_players():
        if subsession.round_number == 1:
            p.participant.vars['totalEarnings'] = 0

#Payoffs
def set_payoffs(g: Group):
    #setup group total harvest
    g.total_harvest = 0

    # setup group random draw
    g.destruction = random.randint(0, Constants.players_per_group * Constants.endowment)

    for p in g.get_players():
        #Total harvest
        g.total_harvest += p.harvest

        # group level binary var of end T/F
        # if hit T then you can set to skip  ->
        # static method in each page (havest, resultwait, result) to skip if certain condition is met.
        # add another page that shows the game ended (destruction of resource)

        # Probability of ending
        g.prob_ending = round((g.total_harvest / (Constants.endowment * Constants.players_per_group)) * 100)
        print('prob of ending', g.prob_ending)

        # end or continue?(Prof's recommendation)
        if g.destruction <= g.total_harvest:
            for group_to_modify in g.in_rounds(g.round_number, Constants.num_rounds):
                group_to_modify.end = True
                print('end variable in round', group_to_modify.round_number, group_to_modify.end)

        #end or continue?
        # if g.destruction <= g.total_harvest:
        #     p.group.end = True
        # else:
        #     p.group.end = False
        # print('end?', g.destruction, p.group.end)

        #testing the idea of getting previous value of p.group.end
        # if p.round_number == 1:
        #     prev_player = p.round_number(1)
        # else:
        #     prev_player = p.in_round(p.round_number - 1)
        #     print('prev end?', prev_player.group.end)

    #Earnings for each round
    for p in g.get_players():
        print('endowment', Constants.endowment)
        print('harvest', p.harvest)
        print('total harvest', g.total_harvest)

        p.period_payoff = float(5*Constants.endowment - 5*p.harvest + 23*p.harvest - 0.25*g.total_harvest*p.harvest)
        print('payoff', p.period_payoff)

        #Cumulative earnings for each participant
        p.participant.vars['totalEarnings'] += p.period_payoff
        print('total earnings', p.participant.vars['totalEarnings'])

        #storing history of cumulative earnings
        p.history_accumulated_earnings = p.participant.vars['totalEarnings']
        print('accumulated earnings tracking', p.history_accumulated_earnings )

        #Cash amount
        p.participant.vars['totalCash'] = round(p.participant.vars['totalEarnings'] * Constants.conversion, 2)


# PAGES
class Harvest(Page):
    form_model = 'player'
    form_fields = ['harvest']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    """Players payoff: How much each has earned"""


class Destruction(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.end

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
    Destruction,
    PaymentInfo,
]