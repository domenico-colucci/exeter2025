from os import environ

SESSION_CONFIGS = [
    dict(
        name="splash_demo",
        app_sequence=[
            "splash"
        ],
        num_demo_participants=3,
    ),
    dict(
        name="quiz_demo",
        app_sequence=[
            "quiz"
        ],
        num_demo_participants=3,
    ),
    dict(
        name="contest_share",
        csf='share',
        random_groups=False,
        contest_endowment=9,
        app_sequence=[
            "contest"
        ],
        num_demo_participants=2,
    ),
    dict(
        name="contest_allpay",
        csf='allpay',
        contest_endowment=9,
        random_groups=False,
        app_sequence=[
            "contest"
        ],
        num_demo_participants=2,
    ),
    dict(
        name="contest_lottery",
        csf='lottery',
        random_groups=False,
        contest_endowment=9,
        app_sequence=[
            "contest"
        ],
        num_demo_participants=2,
    ),
    dict(
        name="encrypt_demo",
        app_sequence=[
            "encrypt"
        ],
        num_demo_participants=1,
    ),
    dict(
        name="summary_demo",
        app_sequence=[
            "summary"
        ],
        num_demo_participants=1,        
    ),
    dict(
        name="full_exp",
        app_sequence=[
            "contest",
            "encrypt",
            "summary"
        ],
        csf='share',
        contest_endowment=9,
        num_demo_participants=2,
    ), 
    dict(
        name="confidence_quiz",
        app_sequence=[
            "confidence_quiz"
        ],
        num_demo_participants=2,
        exam_name="Computational Economics",
        exam_date="July 11, 2025",
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "GBP"
USE_POINTS = False

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = "8668690891855"
