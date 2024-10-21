from os import environ


SESSION_CONFIGS = [
    dict(
        name='cpr_partial_baseline',
        display_name='CPR game partial out-put sharing (baseline)',
        num_demo_participants=8,
        app_sequence=['cpr_partial_baseline'],
    ),

dict(
        name='cpr_partial_60',
        display_name='CPR game partial out-put sharing (High Treatment)',
        num_demo_participants=8,
        app_sequence=['cpr_partial_60'],
    ),

dict(
        name='cpr_partial_60_p',
        display_name='CPR game partial out-put sharing (High Treatment) Practice',
        num_demo_participants=2,
        app_sequence=['cpr_partial_60_p'],
    ),


dict(
        name='cpr_partial_baseline_p',
        display_name='CPR game partial out-put sharing (baseline) Practice',
        num_demo_participants=2,
        app_sequence=['cpr_partial_baseline_p'],
    ),


dict(
        name='intro_baseline',
        display_name='baseline_intro',
        num_demo_participants=1,
        app_sequence=['intro_baseline'],
    ),

dict(
        name='intro_baseline_2',
        display_name='baseline_intro_2',
        num_demo_participants=1,
        app_sequence=['intro_baseline_2'],
    ),

dict(
        name='intro_tr60',
        display_name='Tr60_intro',
        num_demo_participants=1,
        app_sequence=['intro_tr60'],
    ),

dict(
        name='cpr_partial_baseline_2',
        display_name='CPR baseline 2',
        num_demo_participants=8,
        app_sequence=['cpr_partial_baseline_2'],
    ),

    dict(
        name='post_survey',
        display_name='post-survey',
        num_demo_participants=1,
        app_sequence=['post_survey'],
    ),

dict(
        name='consent',
        display_name='consent',
        num_demo_participants=2,
        app_sequence=['consent'],
    ),

dict(
        name='instructions',
        display_name='General Instructions',
        num_demo_participants=1,
        app_sequence=[
            'instructions_general',
                      ],
    ),





dict(
        name='Test_session_AA',
        display_name='Test session AA',
        num_demo_participants=8,
        app_sequence=[
            'consent',
            'instructions_general',
            'intro_baseline',
            'cpr_partial_baseline_p',
            'cpr_partial_baseline',
            'intro_baseline_2',
            'cpr_partial_baseline_2',
            'post_survey',
                      ],
    ),
    #
    #
    # dict(
    #     name='cpr_partial_free',
    #     display_name='CPR game partial out-put sharing (free)',
    #     num_demo_participants=4,
    #     app_sequence=['cpr_partial_free'],
    # ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

#Use points in the rounds and exchange rate is 1 points = $0.01
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01,
    participation_fee=0.00,
    doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
#USE_POINTS = True
#Changing points to tokens
#POINTS_CUSTOM_NAME = 'tokens'
#POINTS_DECIMAL_PLACES = 2

ROOMS = [
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),

    dict(
        name='demo',
        display_name='demo',
        participant_label_file='_rooms/econ9942.txt',
        use_secure_urls=True,
    ),

    dict(
        name = 'ECON9940_pilot_25April',
        display_name = 'ECON9940_pilot_25April',
        participant_label_file = '_rooms/ECON9940_pilot_25April.txt',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""



SECRET_KEY = '5128151015026'

INSTALLED_APPS = ['otree']

use_browser_bots = True



