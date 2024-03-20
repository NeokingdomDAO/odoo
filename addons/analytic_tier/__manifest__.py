{
    'name': 'Analytic Tier',
    'version': '16.0.1.0.0',
    'sequence': 1,
    'category': 'NEOKingdom',
    'author': 'NEOKingdom Odoo Team (https://www.neokingdom.org)',
    'description': """This module provides a tier model which can be used to calculate the amount of tokens.""",
    'depends': ['analytic', 'project', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_views.xml',
        'views/analytic_line_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
