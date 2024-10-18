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
    name_in_url = 'cpr_baseline_practice'
    players_per_group = None
    num_rounds = 3
    instructions_template = 'cpr_partial_baseline/rules.html'
    endowment = 25
    conversion = 0.01
    fixed_others_effort_1 = 70
    fixed_others_effort_2 = 140
    fixed_others_effort_3 = 56


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

    period_payoff = models.FloatField()
    period_payoff_int = models.IntegerField()

    group_total_effort = models.IntegerField()


#FUNCTIONS

#Payoffs
def set_payoffs(player: Player):
    # Assign different values based on the round number
    if player.round_number == 1:
        fixed_others_effort = Constants.fixed_others_effort_1
    elif player.round_number == 2:
        fixed_others_effort = Constants.fixed_others_effort_2
    elif player.round_number == 3:
        fixed_others_effort = Constants.fixed_others_effort_3

    player.others_effort_act_b = fixed_others_effort

    # Total group effort is the sum of the player's effort and fixed others' effort
    group_total_effort = player.effort_act_b + fixed_others_effort
    player.group_total_effort = group_total_effort

    # Payoff calculation
    base_endowment_value = 5 * Constants.endowment
    individual_contribution = 20 * player.effort_act_b
    externality_cost = 0.1171 * group_total_effort * player.effort_act_b

    player.period_payoff = float(base_endowment_value - 5 * player.effort_act_b + individual_contribution - externality_cost)
    player.period_payoff_int = round(player.period_payoff)


#Payoffs
# def set_payoffs(g: Group):
#     for p in g.get_players():
#         # Assign different values based on the round number
#         if g.round_number == 1:
#             g.total_effort_act_b = Constants.fixed_others_effort_1 + p.effort_act_b
#         elif g.round_number == 2:
#             g.total_effort_act_b = Constants.fixed_others_effort_2 + p.effort_act_b
#         elif g.round_number == 3:
#             g.total_effort_act_b = Constants.fixed_others_effort_3 + p.effort_act_b
#
#         if g.round_number == 1:
#             p.others_effort_act_b = Constants.fixed_others_effort_1
#         elif g.round_number == 2:
#             p.others_effort_act_b = Constants.fixed_others_effort_2
#         elif g.round_number == 3:
#             p.others_effort_act_b = Constants.fixed_others_effort_3
#
#     for p in g.get_players():
#         individual_effort = p.effort_act_b
#         group_total_effort = g.total_effort_act_b
#
#         # Logically break down the payoff calculation
#         base_endowment_value = 5 * Constants.endowment
#         individual_contribution = 20 * individual_effort
#         externality_cost = 0.1171 * group_total_effort * individual_effort
#
#         p.period_payoff = float(base_endowment_value - 5 * individual_effort + individual_contribution - externality_cost)
#         p.period_payoff_int = round(p.period_payoff)

        # Log effort of others
        #p.others_effort_act_b = g.total_effort_act_b - p.effort_act_b





# PAGES
class Harvest(Page):
    form_model = 'player'
    form_fields = ['effort_act_b', 'guess_act_b']

    def before_next_page(player: Player, timeout_happened):
        # Calculate payoffs after the player submits their decision
        set_payoffs(player)

class Results(Page):
    """Players payoff: How much each has earned"""
    pass



class End(Page):
    @staticmethod
    def is_displayed(group):
        return group.round_number == Constants.num_rounds



page_sequence = [
    Harvest,
    Results,
    End,
]