from otree.api import *
from random import *
import string

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
    lookup_table = models.StringField()

    def setup_round(self):
        self.pay_per_word=Currency(0.10)
        self.lookup_table= string.ascii_uppercase
        self.word="AB"

    @property
    def lookup_dict(self):
        out ={}
        for letter in string.ascii_uppercase:
            out[letter]= self.lookup_table.index(letter)
        
        return out



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    is_correct=models.BooleanField()
    lookup_table = models.StringField()

    def check_response(self):

        answer=[f'response_{i}' for i in range(1, len(self.subsession.word)+1)]
        # Check if the responses match the lookup dictionary for the word
        correct = [self.subsession.lookup_dict[self.subsession.word[i]] for i in range(len(self.subsession.word))]
        self.is_correct = answer==correct
        # self.is_correct=(
        #     self.response_1==self.subsession.lookup_dict[self.subsession.word[0]]
        #     and
        #     self.response_2==self.subsession.lookup_dict[self.subsession.word[1]]
        # )
        if self.is_correct:
            self.payoff = self.subsession.pay_per_word
            


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
    form_model='player'
    form_fields=['response_1','response_2']
    #staticmethod
    def before_next_page(player, timeout_happened):
        player.check_response()
        


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number==C.NUM_ROUNDS



page_sequence = [Intro, Play, Results]
