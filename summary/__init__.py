from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'summary'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def collect_results(self):
        for p in self.get_players():        
            # p.earnings_contest = p.participant.vars.get('earnings_contest', 0)
            # p.eanrnings_encrypt = p.participant.vars.get('earnings_encrypt', 0)
            
            p.earnings_contest = Currency(5)
            p.earnings_encrypt = Currency(3)

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    earnings_contest = models.CurrencyField()
    earnings_encrypt = models.CurrencyField()


# PAGES
class CollectResults(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.collect_results()

class Summary(Page):
    pass



page_sequence = [CollectResults, Summary]
