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
    name_in_url = 'ian_cpr_forced'
    players_per_group = 8
    num_rounds = 20
    instructions_template = 'cpr_partial_60/Instructions.html'
    endowment = 25
    conversion = 0.01
    safe = 0.50
    share = 0.7


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_harvest = models.IntegerField()
    prob_ending = models.IntegerField()
    destruction = models.IntegerField()
    end = models.BooleanField(
        initial = False, doc = """Indicates whether the game will continue or end. Stay True after triggered"""
    )
    end_temp = models.BooleanField(
        initial = False, doc = """Turn True only for the round"""
    )
    end_prev = models.BooleanField(
        initial = False, doc = """Stay True after triggered but +1 round """
    )
    safety = models.FloatField()


class Player(BasePlayer):
    harvest = models.IntegerField(
        min=0, max=Constants.endowment, label="How much will you harvest?",
    )
    others_harvest = models.IntegerField()
    history_accumulated_earnings = models.FloatField()
    period_payoff = models.FloatField()
    period_payoff_int = models.IntegerField()
    end = models.BooleanField(
        initial = False, doc = """Indicates whether the game will continue or end. Stay True after triggered"""
    )
    end_temp = models.BooleanField(
        initial = False, doc = """Turn True only for the round"""
    )
    end_prev = models.BooleanField(
        initial = False, doc = """Stay True after triggered but +1 round """
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
            p.participant.vars['totalEarnings_b'] = 0

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

        #group safety line
        g.safety = (Constants.players_per_group * Constants.endowment) * Constants.safe
        print ('safety', g.safety)

        # Probability of ending
        if g.total_harvest <= g.safety:
            g.prob_ending = 0
        else:
            g.prob_ending = round((g.total_harvest / (Constants.endowment * Constants.players_per_group)) * 100)
            print('prob of ending', g.prob_ending)

        # end or continue?
        # var 'end' == False initially but stay True when triggered
        if g.destruction <= g.total_harvest and g.total_harvest > g.safety:
            for group_to_modify in g.in_rounds(g.round_number, Constants.num_rounds):
                group_to_modify.end = True
                print('end variable in round', group_to_modify.round_number, group_to_modify.end)

            # Create end_prev var to indicate previous 'end' state
            for group_to_modify in g.in_rounds(g.round_number+1, Constants.num_rounds):
                group_to_modify.end_prev = True

        # Create temporary var that will only be True for the destruction round. and stay False
        if g.destruction <= g.total_harvest and g.total_harvest > g.safety:
            p.group.end_temp = True
        else:
            p.group.end_temp = False
        print('end_tepm?', g.destruction, p.group.end_temp)

    #Earnings for each round
    for p in g.get_players():
        print('endowment', Constants.endowment)
        print('harvest', p.harvest)
        print('total harvest', g.total_harvest)

        p.period_payoff = float(5*(Constants.endowment - p.harvest)
                                + (1-Constants.share)*(23*p.harvest - 0.25*g.total_harvest*p.harvest)
                                + (Constants.share / Constants.players_per_group)*((23 - 0.25*g.total_harvest)*g.total_harvest)
                                )
        print('payoff', p.period_payoff)
        p.period_payoff_int = round(p.period_payoff)

        #Cumulative earnings for each participant
        p.participant.vars['totalEarnings_b'] += p.period_payoff_int
        print('total earnings', p.participant.vars['totalEarnings_b'])

        #storing history of cumulative earnings
        p.history_accumulated_earnings = p.participant.vars['totalEarnings_b']
        print('accumulated earnings tracking', p.history_accumulated_earnings )

        #Cash amount
        p.participant.vars['totalCash_b'] = round(p.participant.vars['totalEarnings_b'] * Constants.conversion, 2)

    #others harvest
    for p in g.get_players():
        p.others_harvest = g.total_harvest - p.harvest




# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(group):
        return group.round_number == 1


class Harvest(Page):
    form_model = 'player'
    form_fields = ['harvest']

    @staticmethod
    def is_displayed(player):
        return player.group.end == False


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

    @staticmethod
    def is_displayed(player):
        return player.group.end_prev == False


class Results(Page):
    """Players payoff: How much each has earned"""

    @staticmethod
    def is_displayed(player):
        return player.group.end_prev == False


class Destruction(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.end_temp

class PaymentInfo(Page):
    @staticmethod
    def is_displayed(group):
        return group.round_number == Constants.num_rounds

    def vars_for_template(player: Player):
        participant = player.participant
        return dict(redemption_code=participant.label or participant.code)


page_sequence = [
    Introduction,
    Harvest,
    ResultsWaitPage,
    Results,
    Destruction,
    PaymentInfo,
]