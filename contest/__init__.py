from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = Currency(0.50)
    COST_PER_TICKET = Currency(10)
    PRIZE = Currency(8)



class Subsession(BaseSubsession):
    is_paid = models.BooleanField()

    def setup_round(self):
        self.is_paid=True
        for group in self.get_groups():
            group.setup_round()
        



class Group(BaseGroup):
    prize = models.CurrencyField()
    def setup_round(self):
        self.prize = C.PRIZE
        for player in self.get_players():
            player.setup_round()


class Player(BasePlayer):
    endowment = models.CurrencyField()
    cost_per_ticket = models.CurrencyField()
    tickets_purchased = models.IntegerField()
    
    def setup_round(self):
        self.endowment = C.ENDOWMENT
        self.cost_per_ticket = C.COST_PER_TICKET
      #  self.tickets_purchased = 0

# def creating_session(subsession):
#     subsession.setup_round()
# PAGES
class SetupRound(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.setup_round()

class DecisionWaitPage(WaitPage):
    pass

class Intro(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Decision(Page):
    form_model = 'player'
    form_fields = ['tickets_purchased']

class Results(Page):
    pass

class EndBlock(Page):
    pass

page_sequence = [SetupRound,
                Intro, 
                Decision, 
                ResultsWaitPage,
                Results,
                EndBlock,]
