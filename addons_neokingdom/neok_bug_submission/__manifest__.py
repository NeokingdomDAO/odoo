# -*- coding: utf-8 -*-
{
    'name': 'NEOKingdom Bug Submission',
    'version': '16.0.1.0.0',
    'sequence': 22,
    'category': 'NEOKingdom',
    'author': 'NEOKingdom Odoo Team (https://www.neokingdom.org)',
    'description': "Creates the backend, frontend possibility to report bugs to NEOKingdom team. (This module is designed to work without the website module, so resources are injected the regular way instead of the odoo way.)",
    'depends': ['base', 'mail', 'google_recaptcha'],
    'data': [
        'data/groups.xml',
        'security/ir.model.access.csv',
        'views/action.xml',
        'views/menu.xml',
        'views/bug_submission.xml',
        'views/issue_page.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
