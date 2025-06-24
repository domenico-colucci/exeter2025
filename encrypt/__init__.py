from otree.api import *
from random import *

doc = """
Encryption game where players must decrypt messages.
"""


class C(BaseConstants):
    NAME_IN_URL = 'encrypt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

def creating_session(subsession: Subsession):
    # This function is called at the start of each session.
    # You can use it to set up initial values or perform any setup tasks.
    pass


# PAGES
class Intro(Page):
    pass

class Play(Page):
    pass

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Intro, Play, Results]
