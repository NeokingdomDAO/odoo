{
    'name': 'Auth Disable Password Login',
    'version': '16.0.1.0.0',
    'summary': """
        Allowing to disable password login for certain users in odoo.
    """,
    'category': 'Hidden/Tools',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'maintainer': 'Peter Schwarz (info@peter-schwarz.it)',
    'website': 'https://www.peter-schwarz.it/',
    'license': 'OPL-1',
    'depends': [
        'auth_signup',
        'base'
    ],
    'data': [
        'views/res_users_views.xml'
    ],
    'demo': [
    ],
}
