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

doc = """
This is the Decision app for Part 2 High Treatment (Tr60) of 
the project "Managing the Tragedy of the Commons: A Partial Output-Sharing Approach"
This will include practice, Harvest, Results, PaymentInfo, rules.
"""


class Constants(BaseConstants):
    name_in_url = 'cpr_tr60'
    players_per_group = 8
    num_rounds = 2
    instructions_template = 'cpr_partial_60/rules.html'
    endowment = 25
    conversion = 0.0025
    share = 0.6


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_effort_act_b = models.IntegerField()


class Player(BasePlayer):
    # Decision for Activity 2
    effort_act_b = models.IntegerField(
        min=0,
        max=Constants.endowment,
        label="How much effort do you want to allocate to Activity 2?"
    )

    # Guess on others' average decision
    guess_act_b = models.IntegerField(
        min=0,
        max=Constants.endowment,
        label="Your guess on others' average effort allocation to Activity 2"
    )

    others_effort_act_b = models.IntegerField()
    others_avg_effort_act_b = models.FloatField()
    history_accumulated_earnings = models.FloatField()
    period_payoff = models.FloatField()
    period_payoff_int = models.IntegerField()


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
    g.total_effort_act_b = sum([p.effort_act_b for p in g.get_players()])

    for p in g.get_players():
        individual_effort = p.effort_act_b
        group_total_effort = g.total_effort_act_b

        # Logically break down the payoff calculation
        base_endowment_value = 5 * Constants.endowment
        individual_extraction = 20 * individual_effort
        group_extraction = 20 * group_total_effort
        group_externality_cost = 0.1171 * group_total_effort * group_total_effort
        externality_cost = 0.1171 * group_total_effort * individual_effort

        earning_act_a = base_endowment_value - (5 * individual_effort)
        earning_act_b = (1 - Constants.share) * (individual_extraction - externality_cost)
        earning_group = (Constants.share/Constants.players_per_group) * (group_extraction - group_externality_cost)

        p.period_payoff = float( earning_act_a +
                                 earning_act_b +
                                 earning_group
                                )

        p.period_payoff_int = round(p.period_payoff)

        # --- For testing purpose, after testing please delete this line ----
        p.participant.vars['totalEarnings_a'] = 0
        #--------------------------------------------------------------------

        p.participant.vars['totalEarnings_b'] += p.period_payoff_int
        p.history_accumulated_earnings = p.participant.vars['totalEarnings_b']

        p.participant.vars['totalEarnings'] = p.participant.vars['totalEarnings_a'] + p.participant.vars['totalEarnings_b']
        p.participant.vars['totalCash'] = round(p.participant.vars['totalEarnings'] * Constants.conversion, 2)
        p.participant.vars['finalCash'] = p.participant.vars['totalCash'] + 3

        # Log effort of others
        p.others_effort_act_b = group_total_effort - individual_effort
        p.others_avg_effort_act_b =round((group_total_effort - individual_effort) / (Constants.players_per_group - 1),1)


# Admin report
def vars_for_admin_report(subsession):
    info = []
    for p in subsession.get_players():
        if p.participant.label is not None:
            total_earnings = 0
            for i in p.in_all_rounds():
                total_earnings += i.period_payoff_int
            info.append((p.participant.label, total_earnings))  # Corrected
    return dict(info=info)


# ------------------------------ Old Version ------------------------------
#Payoffs
# def set_payoffs(g: Group):
#     #setup group total harvest
#     g.total_harvest = 0
#
#     for p in g.get_players():
#         #Total harvest
#         g.total_harvest += p.harvest
#
#     #Earnings for each round
#     for p in g.get_players():
#         print('endowment', Constants.endowment)
#         print('harvest', p.harvest)
#         print('total harvest', g.total_harvest)
#
#         p.period_payoff = float(5*(Constants.endowment - p.harvest)
#                                 + (1-Constants.share)*(23*p.harvest - 0.25*g.total_harvest*p.harvest)
#                                 + (Constants.share / Constants.players_per_group)*((23 - 0.25*g.total_harvest)*g.total_harvest)
#                                 )
#         print('payoff', p.period_payoff)
#         p.period_payoff_int = round(p.period_payoff)
#
#         #Cumulative earnings for each participant
#         p.participant.vars['totalEarnings_b'] += p.period_payoff_int
#         print('total earnings', p.participant.vars['totalEarnings_b'])
#
#         #storing history of cumulative earnings
#         p.history_accumulated_earnings = p.participant.vars['totalEarnings_b']
#         print('accumulated earnings tracking', p.history_accumulated_earnings )
#
#         #Cash amount
#         p.participant.vars['totalCash_b'] = round(p.participant.vars['totalEarnings_b'] * Constants.conversion, 2)
#
#     #others harvest
#     for p in g.get_players():
#         p.others_harvest = g.total_harvest - p.harvest




# PAGES
class Harvest(Page):
    form_model = 'player'
    form_fields = ['effort_act_b', 'guess_act_b']



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'



class Results(Page):
    """Players payoff: How much each has earned"""


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