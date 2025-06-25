from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    ENDOWMENT = Currency(10)
    COST_PER_TICKET = Currency(0.5)
    PRIZE = Currency(8)



class Subsession(BaseSubsession):
    is_paid = models.BooleanField()
    csf = models.StringField(choices=['share', 'allpay'])
    def setup_round(self):
        self.is_paid=True
        for group in self.get_groups():
            group.setup_round()

    def compute_outcome(self):
        for group in self.get_groups():
            group.compute_outcome()

class Group(BaseGroup):
    prize = models.CurrencyField()
    def setup_round(self):
        self.prize = C.PRIZE
        self.subsession.csf = 'allpay'
        self.subsession.is_paid = self.round_number % 2
        for player in self.get_players():
            player.setup_round()

    def compute_outcome_share(self):
        total =sum(player.tickets_purchased for player in self.get_players())

        for player in self.get_players():
            try:
                player.prize_won = player.tickets_purchased / total
            except ZeroDivisionError:
                player.prize_won = 0.0
            
            
    def compute_outcome_allpay(self):
        max_tickets = max(player.tickets_purchased for player in self.get_players())
        num_tied = len([player for player in self.get_players() if player.tickets_purchased == max_tickets])
        for player in self.get_players():
            if player.tickets_purchased == max_tickets:
                player.prize_won = 1/num_tied
            else:
                player.prize_won = 0.0

    def compute_outcome(self):
        self.player.earnings = player.endowment - (player.tickets_purchased * player.cost_per_ticket) + (player.prize_won * self.prize)
        if self.subsession.is_paid:
            self.player.payoff = player.earnings
        if self.subsession.csf == 'share':
            self.compute_outcome_share()
        elif self.subsession.csf == 'allpay':
            self.compute_outcome_allpay()




class Player(BasePlayer):
    endowment = models.CurrencyField()
    cost_per_ticket = models.CurrencyField()
    tickets_purchased = models.IntegerField() # simplest way to enforce budget constraint
    prize_won = models.FloatField()
    earnings= models.CurrencyField()
    
    def setup_round(self):
        self.endowment = C.ENDOWMENT
        self.cost_per_ticket = C.COST_PER_TICKET
      #  self.tickets_purchased = 0
    
    @property
    def coplayers(self):
        """Returns the other player in the group."""
        return self.get_others_in_group()
    
    @property
    def max_tickets(self):
        """Returns the maximum number of tickets a player can purchase."""
        return int(self.endowment / self.cost_per_ticket)

# def creating_session(subsession):
#     subsession.setup_round()
# PAGES
class SetupRound(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.setup_round()

class DecisionWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.compute_outcome()



class Intro(Page):
    pass


class Decision(Page):
    form_model = 'player'
    form_fields = ['tickets_purchased']

    #staticmethod
    def error_message(player, values):
        if values['tickets_purchased'] < 0:
            return 'You cannot purchase a negative number of tickets.'
        if values['tickets_purchased'] > player.max_tickets:
            return (
            f"Purchasing {values['tickets_purchased']} would "
            f"cost more than your endowment of {player.endowment}."
            )

class Results(Page):
    @staticmethod
    def vars_for_template(player):        
        return{
            'coplayer_purchase': player.get_others_in_group()[0].tickets_purchased
            }

class EndBlock(Page):
    pass

page_sequence = [SetupRound,
                Intro, 
                Decision, 
                DecisionWaitPage,
                Results,
                EndBlock,]
