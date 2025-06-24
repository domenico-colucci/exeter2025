from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = Currency(10)
    COST_PER_TICKET = Currency(0.5)
    PRIZE = Currency(8)



class Subsession(BaseSubsession):
    is_paid = models.BooleanField()

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
        for player in self.get_players():
            player.setup_round()

    def compute_outcome(self):
        total =sum(player.tickets_purchased for player in self.get_players())

        for player in self.get_players():
            try:
                player.prize_won = player.tickets_purchased / total
            except ZeroDivisionError:
                player.prize_won = 0.0
            player.earnings = player.endowment - (player.tickets_purchased * player.cost_per_ticket) + (player.prize_won * self.prize)
            #print(player.earnings)


class Player(BasePlayer):
    endowment = models.CurrencyField()
    cost_per_ticket = models.CurrencyField()
    tickets_purchased = models.IntegerField()
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
