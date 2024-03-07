# -*- coding: utf-8 -*-
{
    'name': 'NEOKingdom Project Management',
    'version': '16.0.1.0.0',
    'sequence': 31,
    'category': 'NEOKingdom',
    'author': 'NEOKingdom Odoo Team (https://www.neokingdom.org)',
    'description': "Adding new tagging, filtering and other ways to track, configure project management to fit NEOKingdom's needs.",
    'depends': ['base', 'project'],
    'data': [
        'data/tags.xml',
        'views/project_project.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
