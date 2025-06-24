from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    is_paid = models.BooleanField()
    


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class SetupRound(WaitPage):
    pass

class DecisionWaitPage(WaitPage):
    pass

class Intro(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Decision(Page):
    pass

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
