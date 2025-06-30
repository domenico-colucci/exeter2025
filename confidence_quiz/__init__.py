from otree.api import *


doc = """
Measuring students' expectations about their exam performance.
"""


class C(BaseConstants):
    NAME_IN_URL = 'expectations_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    exam_name = models.StringField()
    exam_date = models.StringField()

    def setup_quiz(self):
        self.exam_name = self.session.config.get('exam_name', 'Computational Economics')
        self.exam_date = self.session.config.get('exam_date', '2025-01-01')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    is_returning = models.BooleanField(
        label="Have you taken this exam before?",
        choices=[
            [True, "Yes"],
            [False, "No, it's my first time"]
        ],
        widget=widgets.RadioSelectHorizontal)
    exp_mark = models.IntegerField(
        label="What mark do you expect to get in this exam?",
        choices=[
            [17, "Fail"],
            [18, "18"],
            [19, "19"],
            [20, "20"],
            [21, "21"],
            [22, "22"],
            [23, "23"],
            [24, "24"],
            [25, "25"],
            [26, "26"],
            [27, "27"],
            [28, "28"],
            [29, "29"],
            [30, "30"],
            [31, "30+L"]
        ],
        widget=widgets.RadioSelectHorizontal,
    )
    matricola= models.IntegerField(
        label="What is your student matricola number?",
        min=1000000,
        max=9999999,
        blank=True)
    #is_IT = models.BooleanField(label="Are you an Italian student?")

# PAGES

class Setup_Quiz(WaitPage):
    """
    This page is used to set up the quiz before players arrive.
    It initializes the exam name and date from the session config.
    """
    @staticmethod
    def after_all_players_arrive(group):
        group.subsession.setup_quiz()

class Intro(Page):
    pass
    # form_model = 'player'
    # form_fields = ['is_IT']



class Predict(Page):
    form_model = 'player'
    form_fields = ['is_returning', 'exp_mark', 'matricola']



class Thanks(Page):
    pass


page_sequence = [Setup_Quiz, Intro, Predict, Thanks]
