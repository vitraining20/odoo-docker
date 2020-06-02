{
    'name': 'Service Desk',
    'category': 'Service Desk',
    'summary': """
        Process addon for the Website Service Desk application.
    """,
    'author': "Center of Research and Development",
    'website': "https://crnd.pro",
    'license': 'OPL-1',
    'version': '13.0.0.1.0',
    'depends': [
        'generic_request',
    ],
    'data': [
        'data/init_data.xml',
        'data/request_type_incident.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
