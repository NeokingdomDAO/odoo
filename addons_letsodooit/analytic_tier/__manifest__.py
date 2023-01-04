{
    'name' : 'Analytic Tier',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'sequence': 1,
    'description': """This module provides a tier model which can be used to calculate the amount of tokens.""",
    'license': 'OPL-1',
    'depends': ['analytic'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_views.xml',
        'views/analytic_line_views.xml'
      ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
