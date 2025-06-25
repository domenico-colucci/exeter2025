from otree.api import *
from random import *

doc = """
Encryption game where players must decrypt messages.
"""


class C(BaseConstants):
    NAME_IN_URL = 'encrypt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3


class Subsession(BaseSubsession):
    pay_per_word = models.CurrencyField()
    word = models.StringField()

    def setup_round(self):
        self.pay_per_word=Currency(0.10)
        self.word="AB"



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

def creating_session(subsession: Subsession):
    # This function is called at the start of each session.
    # You can use it to set up initial values or perform any setup tasks.
    subsession.setup_round()


    

# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number==1


class Play(Page):
    pass


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number==C.NUM_ROUNDS



page_sequence = [Intro, Play, Results]
