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
    name_in_url = 'cpr_baseline_2'
    players_per_group = 8
    num_rounds = 10
    instructions_template = 'cpr_partial_baseline/rules.html'
    endowment = 25
    conversion = 0.01


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
            p.participant.vars['totalEarnings_a'] = 0

#Payoffs
def set_payoffs(g: Group):
    g.total_effort_act_b = sum([p.effort_act_b for p in g.get_players()])

    for p in g.get_players():
        individual_effort = p.effort_act_b
        group_total_effort = g.total_effort_act_b

        # Logically break down the payoff calculation
        base_endowment_value = 5 * Constants.endowment
        individual_contribution = 20 * individual_effort
        externality_cost = 0.1171 * group_total_effort * individual_effort

        p.period_payoff = float(base_endowment_value - 5 * individual_effort + individual_contribution - externality_cost)
        p.period_payoff_int = round(p.period_payoff)

        p.participant.vars['totalEarnings_a'] += p.period_payoff_int
        p.history_accumulated_earnings = p.participant.vars['totalEarnings_a']
        p.participant.vars['totalCash_a'] = round(p.participant.vars['totalEarnings_a'] * Constants.conversion, 2)

        # Log effort of others
        p.others_effort_act_b = group_total_effort - individual_effort

# Old version
# def set_payoffs(g: Group):
#     #setup group total harvest
#     g.total_effort_act2 = 0
#
#     for p in g.get_players():
#         #Total harvest
#         g.total_effort_act2 += p.effort_act2
#
#     #Earnings for each round
#     for p in g.get_players():
#         print('Endowment', Constants.endowment)
#         print('Effort spent in Activity 2', p.effort_act2)
#         print('Group Total effort spent in Activity 2', g.total_effort_act2)
#
#         p.period_payoff = float(5*Constants.endowment - 5*p.effort_act2 + 20*p.effort_act2 - 0.1171*g.total_effort_act2*p.effort_act2)
#         print('payoff', p.period_payoff)
#
#         p.period_payoff_int = round(p.period_payoff)
#
#         #Cumulative earnings for each participant
#         p.participant.vars['totalEarnings_a'] += p.period_payoff_int
#         print('total earnings', p.participant.vars['totalEarnings_a'])
#
#         #storing history of cumulative earnings
#         p.history_accumulated_earnings = p.participant.vars['totalEarnings_a']
#         print('accumulated earnings tracking', p.history_accumulated_earnings )
#
#         #Cash amount
#         p.participant.vars['totalCash_a'] = round(p.participant.vars['totalEarnings_a'] * Constants.conversion, 2)
#
#     #others effort in activity 2 (extract cpr)
#     for p in g.get_players():
#         p.others_effort_act2 = g.total_effort_act2 - p.effort_act2

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

# Old version
# def vars_for_admin_report(subsession):
#     info = []
#     for p in subsession.get_players():
#         if p.participant.label is not None:
#             total_earnings = 0
#             for i in p.in_all_rounds():
#                 total_earnings += i.period_payoff_int
#             paymentInfo.append(p.participant.label, total_earnings)
#     return dict(info=info)


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