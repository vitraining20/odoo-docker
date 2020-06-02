{
    'name': "Bureaucrat Helpdesk Lite",

    'summary': """
        Help desk
    """,

    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'version': '13.0.1.0.14',
    'category': 'Helpdesk',

    # any module necessary for this one to work correctly
    'depends': [
        'generic_request',
        'crnd_service_desk',
        'crnd_wsd',
    ],

    # always loaded
    'data': [
    ],
    'images': ['static/description/banner.gif'],
    'demo': [],

    'installable': True,
    'application': True,
    'license': 'OPL-1',

    'price': 0.0,
    'currency': 'EUR',
    "live_test_url": "https://yodoo.systems/saas/"
                     "template/helpdesk-lite-demo-data-69",
}
