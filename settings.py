from os import environ


SESSION_CONFIGS = [
    dict(
        name='cpr_partial_baseline',
        display_name='CPR game partial out-put sharing (baseline)',
        num_demo_participants=2,
        app_sequence=['cpr_partial_baseline'],
    ),

    # dict(
    #     name='cpr_partial_forced',
    #     display_name='CPR game partial out-put sharing (forced)',
    #     num_demo_participants=4,
    #     app_sequence=['cpr_partial_forced'],
    # ),
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
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
    dict(
        name='econ9942',
        display_name='Econ 9942 class',
        participant_label_file='_rooms/econ9942.txt',
        use_secure_urls=True,
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

# use_browser_bots = True



