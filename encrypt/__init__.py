from otree.api import *
import random
import string
import time

doc = """
Encryption game where players must decrypt messages.
"""


class C(BaseConstants):
    NAME_IN_URL = 'encrypt'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    LOOKUP_TABLES=[
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBA",
        "ZBCDEFGHIJKLMNOPQRSTUVWXYA",
    ]
    time_for_TASK= 40  # seconds

class Subsession(BaseSubsession):
    pay_per_word = models.CurrencyField()
    word = models.StringField()
    lookup_table = models.StringField()
    time_for_task = models.IntegerField()
    random_seed = models.IntegerField()

    def setup_round(self):
        if self.round_number == 1:
            self.random_seed=(self.session.config.get('random_seed', 12345678))
            random.seed(self.random_seed)
        self.pay_per_word=Currency(0.10)
        self.lookup_table= C.LOOKUP_TABLES[self.round_number-1 % 3]
        self.word="".join(random.choices(
            string.ascii_uppercase, k=5
        ))
        self.time_for_task = C.time_for_TASK

    @property
    def lookup_dict(self):
        out ={}
        for letter in string.ascii_uppercase:
            out[letter]= self.lookup_table.index(letter)
        
        return out
    @property
    def correct_response(self):
        return [self.lookup_dict[letter] for letter in self.word]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()

    is_correct=models.BooleanField()
    lookup_table = models.StringField()
    started_task_at = models.FloatField()

    @property
    def response(self):
        return [f'response_{i}' for i in range(1, len(self.subsession.word)+1)]
    
    @property
    def form_fields(self):
        return [f'response_{i}' for i in range(1, len(self.subsession.word)+1)]


    def check_response(self):

        #answer=[f'response_{i}' for i in range(1, len(self.subsession.word)+1)]
        # Check if the responses match the lookup dictionary for the word
        #correct = [self.subsession.lookup_dict[self.subsession.word[i]] for i in range(len(self.subsession.word))]
        self.is_correct = self.response ==self.subsession.correct_response
        # self.is_correct=(
        #     self.response_1==self.subsession.lookup_dict[self.subsession.word[0]]
        #     and
        #     self.response_2==self.subsession.lookup_dict[self.subsession.word[1]]
        # )
        if self.is_correct:
            self.payoff = self.subsession.pay_per_word
            
    def start_task(self):
        self.started_task_at = time.time()

    def get_time_elapsed(self):
        return time.time() - self.in_round(1).started_task_at


    def get_time_remaining(self):
        return self.subsession.in_round(1).time_for_task - self.get_time_elapsed()


def creating_session(subsession: Subsession):
    # This function is called at the start of each session.
    # You can use it to set up initial values or perform any setup tasks.
    subsession.setup_round()


    

# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number==1
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.start_task()


class Play(Page):
    form_model='player'
    @staticmethod
    def get_timeout_seconds(player):
        return player.get_time_remaining()
    
    #get the form fields from the player class
    @staticmethod
    def get_form_fields(player):
        return player.form_fields
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.check_response()
        



class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number==C.NUM_ROUNDS



page_sequence = [Intro, Play, Results]
